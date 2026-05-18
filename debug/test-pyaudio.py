"""
test-pyaudio.py — ทดสอบ PyAudio playback ว่าเล่น PCM16 ได้ถูกต้องหรือไม่

วิธีใช้:
    python test-pyaudio.py                     # เล่น sine wave 440 Hz ผ่าน default output
    python test-pyaudio.py --device 27          # เล่นผ่าน device index 27 (VB-Cable)
    python test-pyaudio.py --list-devices       # ดู device list
    python test-pyaudio.py --record sine.wav    # บันทึก sine wave ลงไฟล์ WAV
"""

import argparse
import math
import struct
import wave
import pyaudio

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
DURATION = 5  # seconds
FREQUENCY = 440  # Hz (A4 note)


def list_devices():
    p = pyaudio.PyAudio()
    print("Available output devices:\n")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        max_channels = int(info["maxOutputChannels"])
        if max_channels > 0:
            print(f"  [{i}] {info['name']} ({max_channels} ch, {int(info['defaultSampleRate'])} Hz)")
    p.terminate()


def generate_sine_wave(freq, duration, rate, volume=0.5):
    """Generate PCM16 sine wave data."""
    num_samples = int(rate * duration)
    samples = []
    for i in range(num_samples):
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
        # Pack as little-endian 16-bit signed
        samples.append(struct.pack('<h', value))
    return b''.join(samples)


def main():
    parser = argparse.ArgumentParser(description="Test PyAudio playback with sine wave")
    parser.add_argument("--device", type=int, default=None,
                        help="Output device index")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available devices and exit")
    parser.add_argument("--record", type=str, default=None,
                        help="Save sine wave to WAV file")
    parser.add_argument("--play", type=str, default=None,
                        help="Play a WAV file to test PyAudio playback (overrides sine)")
    parser.add_argument("--freq", type=int, default=FREQUENCY,
                        help=f"Sine frequency in Hz (default: {FREQUENCY})")
    parser.add_argument("--duration", type=int, default=DURATION,
                        help=f"Duration in seconds (default: {DURATION})")
    parser.add_argument("--volume", type=float, default=0.5,
                        help="Volume 0.0-1.0 (default: 0.5)")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    # --- WAV playback mode ---
    if args.play:
        print(f"📂 Playing WAV file: {args.play}")
        wf = wave.open(args.play, 'rb')
        print(f"   Format: {wf.getnchannels()} ch, {wf.getframerate()} Hz, {wf.getsampwidth()*8}-bit")
        data = wf.readframes(wf.getnframes())
        wf.close()
        print(f"   Data: {len(data)} bytes ({len(data)//2} samples)")
        use_rate = wf.getframerate()
    else:
        # Generate sine wave data
        print(f"🔊 Generating {args.freq} Hz sine wave, {args.duration}s, volume {args.volume}")
        data = generate_sine_wave(args.freq, args.duration, RATE, args.volume)
        print(f"   Data size: {len(data)} bytes ({len(data)//2} samples @ {RATE} Hz)")
        use_rate = RATE

        # Save to WAV if requested
        if args.record:
            with wave.open(args.record, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(data)
            print(f"   💾 Saved to {args.record}")

    # Play through PyAudio
    p = pyaudio.PyAudio()
    device_name = "Default"

    device_kwargs = {}
    if args.device is not None:
        device_kwargs["output_device_index"] = args.device
        info = p.get_device_info_by_index(args.device)
        device_name = info["name"]
        print(f"   🎯 Output device: [{args.device}] {device_name}")
    else:
        print(f"   🎯 Output device: Default system output")

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=use_rate,
        output=True,
        **device_kwargs,
    )

    print(f"   ▶️  Playing {args.duration} seconds...")

    # Write in chunks (same as audio-server.py does)
    chunk_size = CHUNK * 2  # 2048 samples * 2 bytes = 4096 bytes
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        stream.write(chunk)

    stream.close()
    p.terminate()
    print(f"   ✅ Done!")


if __name__ == "__main__":
    main()
