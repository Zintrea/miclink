"""
Test VB-Cable (device 27) with stereo vs mono output.
"""
import pyaudio, math, struct, time, sys

p = pyaudio.PyAudio()
volume = 0.5
freq = 440
rate = 48000
duration = 3
device_idx = 27

# ---- Test 1: Stereo output (2 channels) ----
num_samples = int(rate * duration)
stereo_data = b''
for i in range(num_samples):
    v = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
    stereo_data += struct.pack('<hh', v, v)  # L and R same

print(f"Stereo ({num_samples*2} samples) through device {device_idx}...")
try:
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=rate,
                    output=True, output_device_index=device_idx)
    stream.write(stereo_data)
    stream.close()
    print("Stereo OK")
except Exception as e:
    print(f"Stereo failed: {e}")

time.sleep(0.5)

# ---- Test 2: Mono output ----
mono_data = b''
for i in range(num_samples):
    v = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
    mono_data += struct.pack('<h', v)

print(f"Mono ({num_samples} samples) through device {device_idx}...")
try:
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                    output=True, output_device_index=device_idx)
    stream.write(mono_data)
    stream.close()
    print("Mono OK")
except Exception as e:
    print(f"Mono failed: {e}")

p.terminate()
print("Done! Which one sounded better?")
