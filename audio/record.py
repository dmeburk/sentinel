import sounddevice as sd
import soundfile as sf
import numpy as np

TARGET_RATE = 16000

def find_valid_input_device():
    for i, dev in enumerate(sd.query_devices()):
        if dev['max_input_channels'] > 0:
            print(f"🎤 Using input device {i}: {dev['name']}")
            return i
    raise RuntimeError("❌ No valid input device found")

def record_to_wav(filename="command.wav", duration=4, device_index=None):
    if device_index is None:
        device_index = find_valid_input_device()

    info = sd.query_devices(device_index, 'input')
    native_rate = int(info['default_samplerate'])
    print(f"🎙️ Recording voice command at {native_rate} Hz...")

    sd.default.device = (device_index, None)
    recording = sd.rec(int(duration * native_rate), samplerate=native_rate, channels=1, dtype='int16')
    sd.wait()

    if native_rate != TARGET_RATE:
        from scipy.signal import resample_poly
        from math import gcd
        g = gcd(TARGET_RATE, native_rate)
        recording = resample_poly(recording, TARGET_RATE // g, native_rate // g).astype(np.int16)

    sf.write(filename, recording, TARGET_RATE)
    print(f"📁 Saved recording to {filename} at {TARGET_RATE} Hz")
