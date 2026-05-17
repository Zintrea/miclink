"""
miclink — High-quality mobile microphone audio streaming server
Receives PCM16 audio via WebSocket and outputs to Virtual Audio Cable

Usage:
    python audio-server.py [--device DEVICE_INDEX] [--port PORT]
    python audio-server.py --secure [--device DEVICE_INDEX]

Run with --list-devices to see available audio output devices.
"""

import asyncio
import argparse
import json
import os
import sys
import signal
import ssl
import mimetypes
import wave
from pathlib import Path

from dotenv import load_dotenv

import websockets
from websockets.http11 import Response, Headers
import pyaudio


def list_devices():
    """Print all available audio output devices."""
    p = pyaudio.PyAudio()
    print("Available audio output devices:\n")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        max_channels = int(info["maxOutputChannels"])
        if max_channels > 0:
            print(f"  [{i}] {info['name']} ({max_channels} ch, {int(info['defaultSampleRate'])} Hz)")
    p.terminate()


def find_device_by_name(p, name_substring):
    """Find output device index by name substring."""
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if name_substring.lower() in info["name"].lower() and info["maxOutputChannels"] > 0:
            return i
    return None


def mono_to_stereo(mono_bytes, gain=3.0):
    """Convert mono PCM16 bytes to interleaved stereo PCM16 with gain boost.
    
    VB-Cable (device 27) produces garbled audio with mono output
    at 48000 Hz. Sending native stereo (L/R duplicate) fixes it.
    
    gain: volume multiplier (2.0-4.0). Clamps to prevent clipping.
    """
    result = bytearray(len(mono_bytes) * 2)
    for i in range(0, len(mono_bytes), 2):
        # Read 16-bit signed little-endian sample
        sample = mono_bytes[i] | (mono_bytes[i + 1] << 8)
        # Convert from unsigned to signed (Python treats bytes as 0-255)
        if sample >= 32768:
            sample -= 65536
        
        # Apply gain boost
        sample = int(sample * gain)
        if sample > 32767:
            sample = 32767
        elif sample < -32768:
            sample = -32768
        
        # Convert back to unsigned for byte packing
        if sample < 0:
            sample += 65536
        
        # Duplicate to L and R
        result[i * 2] = sample & 0xFF
        result[i * 2 + 1] = (sample >> 8) & 0xFF
        result[i * 2 + 2] = sample & 0xFF
        result[i * 2 + 3] = (sample >> 8) & 0xFF
    return bytes(result)


# Audio settings
CHUNK = 2048        # Buffer size — higher = more stable, lower = less latency
FORMAT = pyaudio.paInt16
CHANNELS = 1        # Input from client (mono)
OUTPUT_CHANNELS = 2 # Output to device (stereo — VB-Cable needs this!)
RATE = 48000        # Studio quality sample rate


class AudioServer:
    def __init__(self, host="0.0.0.0", port=8765, device_index=None,
                 ssl_context=None, web_dir=None):
        self.host = host
        self.port = port
        self.device_index = device_index
        self.ssl_context = ssl_context
        self.web_dir = Path(web_dir) if web_dir else Path.cwd()
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.rate = RATE
        self.gain = 3.0  # default volume boost; overridden by --gain
        self.record_path = None
        self.record_wav = None  # WAV file for --record diagnostics
        self.clients = set()

    def open_stream(self):
        """Open PyAudio output stream to the selected device."""
        device_name = "Default"
        device_kwargs = {}

        if self.device_index is not None:
            device_kwargs["output_device_index"] = self.device_index
            info = self.p.get_device_info_by_index(self.device_index)
            device_name = info["name"]
            print(f"  Output device: [{self.device_index}] {device_name}")
        else:
            print("  Output device: Default system output")

        self.stream = self.p.open(
            format=FORMAT,
            channels=OUTPUT_CHANNELS,
            rate=self.rate,
            output=True,
            **device_kwargs,
        )
        print(f"  Stream ready — {self.rate} Hz, {OUTPUT_CHANNELS} ch (stereo), PCM16")

    async def handle_client(self, websocket):
        """Handle one connected client (iPad/phone browser)."""
        addr = websocket.remote_address
        print(f"\n📱 Connected: {addr}")
        self.clients.add(websocket)

        metadata_received = False

        try:
            async for message in websocket:
                # First text message: metadata (sample rate, etc.)
                if not metadata_received and isinstance(message, str):
                    try:
                        info = json.loads(message)
                        new_rate = info.get("sample_rate")
                        print(f"  📊 Client reports: {new_rate} Hz")
                        if new_rate and new_rate != self.rate:
                            print(f"  ➡️  Adjusting playback from {self.rate} to {new_rate} Hz")
                            self.stream.close()
                            self.rate = new_rate
                            self.open_stream()
                        else:
                            print(f"  ✅ Playback at {self.rate} Hz (no change needed)")

                        # Open WAV recording if --record is set (after we know the rate)
                        if self.record_wav is None and hasattr(self, 'record_path') and self.record_path:
                            self.record_wav = wave.open(self.record_path, 'wb')
                            self.record_wav.setnchannels(CHANNELS)
                            self.record_wav.setsampwidth(2)  # 16-bit = 2 bytes
                            self.record_wav.setframerate(self.rate)
                            print(f"  🎙️  Recording to {self.record_path} ({self.rate} Hz)")
                    except json.JSONDecodeError:
                        pass
                    metadata_received = True
                    continue

                # Binary message: PCM16 audio data
                if isinstance(message, bytes):
                    # Convert mono → stereo (VB-Cable needs native stereo)
                    stereo_data = mono_to_stereo(message, gain=self.gain)
                    self.stream.write(stereo_data)
                    if self.record_wav is not None:
                        self.record_wav.writeframes(message)  # save original mono
        except websockets.exceptions.ConnectionClosed:
            print(f"❌ Disconnected: {addr}")
        finally:
            if self.record_wav is not None:
                self.record_wav.close()
                print(f"  💾 Recording saved: {self.record_path}")
                self.record_wav = None
            self.clients.discard(websocket)

    async def handle_http_request(self, connection, request):
        """Serve static files for non-WebSocket requests (e.g. web-client.html).

        Returns None for WebSocket upgrade requests so the library handles them.
        """
        # CRITICAL: let WebSocket upgrade requests pass through
        if request.headers.get("Upgrade", "").lower() == "websocket":
            return None

        path = request.path
        # Normalize path — serve index at / or /web-client.html
        path = path.lstrip("/")
        if path == "" or path == "/":
            path = "web-client.html"

        # Security: resolve and verify path is within web_dir
        full_path = (self.web_dir / path).resolve()
        try:
            full_path.relative_to(self.web_dir.resolve())
        except ValueError:
            return Response(403, "Forbidden", Headers(), b"Forbidden")

        if not full_path.exists() or not full_path.is_file():
            return Response(404, "Not Found", Headers(), b"Not found")

        body = full_path.read_bytes()
        mime_type, _ = mimetypes.guess_type(str(full_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        headers = Headers()
        headers["Content-Type"] = mime_type
        headers["Content-Length"] = str(len(body))
        headers["Cache-Control"] = "no-cache"
        return Response(200, "OK", headers, body)

    async def start(self):
        """Start the server — serves both HTTP (static files) and WebSocket on the same port."""
        proto = "wss" if self.ssl_context else "ws"
        print("\n" + "=" * 50)
        print("  🎙️  miclink — High-Quality Audio Server")
        print("=" * 50)
        print(f"  Host: {self.host}")
        print(f"  Port: {self.port} ({proto})")
        print(f"  Audio: {RATE} Hz, {OUTPUT_CHANNELS} ch (stereo), PCM16")
        print(f"  Gain: {self.gain}x")
        self.open_stream()

        stop = asyncio.Future()

        async def server():
            kwargs = {}
            if self.ssl_context:
                kwargs["ssl"] = self.ssl_context
                kwargs["process_request"] = self.handle_http_request
            async with websockets.serve(self.handle_client, self.host, self.port, **kwargs):
                web_url = f"https://{self.host}:{self.port}/web-client.html"
                print(f"\n  🌍 All-in-one: {web_url}")
                if self.ssl_context:
                    print("  🔒 Secure mode — everything on one port (cert trust stays consistent)")
                print("  💡 Open the URL above on your iPad/phone and connect!\n")
                await stop  # run forever

        # Handle Ctrl+C gracefully
        loop = asyncio.get_running_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, lambda: stop.set_result(None))
            loop.add_signal_handler(signal.SIGTERM, lambda: stop.set_result(None))
        except NotImplementedError:
            # Windows: fall back to KeyboardInterrupt from main()
            pass

        await server()

    def cleanup(self):
        """Clean up resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()


def main():
    load_dotenv()

    host_default = os.getenv("HOST", "0.0.0.0")
    port_default = int(os.getenv("PORT", "8765"))
    device_index_default = (
        int(os.getenv("DEVICE_INDEX")) if os.getenv("DEVICE_INDEX") else None
    )
    device_name_default = os.getenv("DEVICE_NAME", "")

    parser = argparse.ArgumentParser(description="miclink — mobile mic audio server")
    parser.add_argument("--host", type=str, default=host_default,
                        help=f"Host interface (default: {host_default})")
    parser.add_argument("--port", type=int, default=port_default,
                        help=f"Port for WebSocket (non-secure) or all-in-one (secure) (default: {port_default})")
    parser.add_argument("--device", type=int, default=device_index_default,
                        help="Output device index")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available output devices and exit")
    parser.add_argument("--find-device", type=str, default=None,
                        help="Find device by name substring")
    parser.add_argument("--secure", action="store_true",
                        help="Enable HTTPS/WSS (generate cert first via certs/gen-cert.py)")
    parser.add_argument("--cert", type=str, default=None,
                        help="Path to SSL cert PEM file (default: certs/server.pem)")
    parser.add_argument("--key", type=str, default=None,
                        help="Path to SSL key file (default: certs/server.key)")
    parser.add_argument("--https-port", type=int, default=8443,
                        help="Port for HTTPS/WSS in --secure mode (default: 8443)")
    parser.add_argument("--record", type=str, default=None,
                        help="Save incoming audio to WAV file for diagnostics (e.g. diag.wav)")
    parser.add_argument("--gain", type=float, default=3.0,
                        help="Volume boost for quiet mics (default: 3.0, range 1.0-5.0)")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    # Handle --find-device (explicit CLI request)
    if args.find_device:
        p = pyaudio.PyAudio()
        idx = find_device_by_name(p, args.find_device)
        if idx is not None:
            print(f"Found: [{idx}] {p.get_device_info_by_index(idx)['name']}")
        else:
            print(f"No output device matching '{args.find_device}' found.")
        p.terminate()
        return

    # Setup SSL if --secure is used
    ssl_context = None
    final_port = args.port          # non-secure: use --port (default 8765)
    web_dir = None

    if args.secure:
        script_dir = Path(__file__).parent
        cert_path = Path(args.cert) if args.cert else script_dir / "certs" / "server.pem"
        key_path = Path(args.key) if args.key else script_dir / "certs" / "server.key"

        if not cert_path.exists():
            print(f"❌ Certificate not found: {cert_path}")
            print("   Run: python certs/gen-cert.py")
            return

        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(str(cert_path), str(key_path))
        print(f"  🔒 SSL: {cert_path}")

        # In secure mode: use --https-port as the single unified port
        final_port = args.https_port
        web_dir = script_dir

        print(f"  🌍 Unified server: https://{args.host}:{final_port}")
        print(f"  📱 iPad: https://172.20.10.2:{final_port}/web-client.html")
        print()

    device_index = args.device
    if device_index is None and device_name_default:
        p = pyaudio.PyAudio()
        idx = find_device_by_name(p, device_name_default)
        p.terminate()
        if idx is not None:
            device_index = idx
            print(f"  🔍 Auto-detected device [{idx}]: {device_name_default}")
        else:
            print(f"  ⚠️  Device '{device_name_default}' not found — using default output")

    server = AudioServer(
        host=args.host,
        port=final_port,
        device_index=device_index,
        ssl_context=ssl_context,
        web_dir=web_dir,
    )
    server.record_path = args.record
    server.gain = args.gain
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        pass
    finally:
        server.cleanup()
        print("\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    main()
