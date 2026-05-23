import pyaudio
from sentinel_config import MICROPHONE_NAME

def find_device_index():
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0 and MICROPHONE_NAME in info["name"]:
            audio.terminate()
            return i
    audio.terminate()
    raise RuntimeError(f"Microphone '{MICROPHONE_NAME}' not found")
