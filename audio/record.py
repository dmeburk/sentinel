import sounddevice as sd
import soundfile as sf

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
    samplerate = int(info['default_samplerate'])
    print(f"🎙️ Recording voice command at {samplerate} Hz...")

    sd.default.device = (device_index, None)
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"📁 Saved recording to {filename}")