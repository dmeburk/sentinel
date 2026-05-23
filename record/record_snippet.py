import sounddevice as sd
import soundfile as sf
import time

def record_audio(filename, duration=4, device_index=0):
    info = sd.query_devices(device_index, 'input')
    samplerate = int(info['default_samplerate'])
    print(f"🎙️ Recording voice command at {samplerate} Hz...")

    sd.default.device = (device_index, None)
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"💾 Saved recording to {filename}")

if __name__ == "__main__":
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"/tmp/command_{timestamp}.wav"
    record_audio(filename)