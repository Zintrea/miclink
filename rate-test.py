"""
Quick test: play sine wave through VB-Cable at different sample rates.
"""
import pyaudio, math, struct, time

p = pyaudio.PyAudio()
volume = 0.5
freq = 440

for rate in [44100, 48000]:
    duration = 2
    num_samples = int(rate * duration)
    samples = []
    for i in range(num_samples):
        v = int(volume * 32767 * math.sin(2 * math.pi * freq * i / rate))
        samples.append(struct.pack('<h', v))
    data = b''.join(samples)
    print(f"Playing {rate} Hz through device 27...")
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, output=True, output_device_index=27)
    stream.write(data)
    stream.close()
p.terminate()
print("Done!")
