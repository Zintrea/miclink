"""
miclink — High-quality mobile microphone audio streaming server
Receives PCM16 audio via WebSocket and outputs to Virtual Audio Cable

Usage:
    python audio-server.py [--device DEVICE_INDEX] [--port PORT]

Run with --list-devices to see available audio output devices.
"""

import asyncio
import argparse
import os
import sys
import signal

from dotenv import load_dotenv

import websockets
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


# Audio settings
CHUNK = 2048        # Buffer size — higher = more stable, lower = less latency
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000        # Studio quality sample rate


class AudioServer:
    def __init__(self, host="0.0.0.0", port=8765, device_index=None):
        self.host = host
        self.port = port
        self.device_index = device_index
        self.p = pyaudio.PyAudio()
        self.stream = None
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
            channels=CHANNELS,
            rate=RATE,
            output=True,
            **device_kwargs,
        )
        print("  Stream ready — waiting for connections...")

    async def handle_client(self, websocket):
        """Handle one connected client (iPad/phone browser)."""
        addr = websocket.remote_address
        print(f"\n📱 Connected: {addr}")
        self.clients.add(websocket)

        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    self.stream.write(message)
        except websockets.exceptions.ConnectionClosed:
            print(f"❌ Disconnected: {addr}")
        finally:
            self.clients.discard(websocket)

    async def start(self):
        """Start the WebSocket server."""
        print("\n" + "=" * 50)
        print("  🎙️  miclink — High-Quality Audio Server")
        print("=" * 50)
        print(f"  Host: {self.host}")
        print(f"  Port: {self.port}")
        print(f"  Audio: {RATE} Hz, {CHANNELS} ch, PCM16")
        self.open_stream()

        stop = asyncio.Future()

        async def server():
            async with websockets.serve(self.handle_client, self.host, self.port):
                print(f"\n  🌐 WebSocket: ws://{self.host}:{self.port}")
                print("  💡 Open web-client.html on your iPad/phone and connect!\n")
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
                        help=f"WebSocket port (default: {port_default})")
    parser.add_argument("--device", type=int, default=device_index_default,
                        help="Output device index")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available output devices and exit")
    parser.add_argument("--find-device", type=str, default=None,
                        help="Find device by name substring")
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

    # If --device not given but DEVICE_NAME is set in .env, auto-detect
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

    server = AudioServer(host=args.host, port=args.port, device_index=device_index)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        pass
    finally:
        server.cleanup()
        print("\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    main()
