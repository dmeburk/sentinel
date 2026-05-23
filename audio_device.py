# audio_device.py

from pvrecorder import PvRecorder
from sentinel_config import MICROPHONE_NAME

def find_device_index():
    devices = PvRecorder.get_available_devices()
    for i, name in enumerate(devices):
        if MICROPHONE_NAME in name:
            return i
    raise RuntimeError(f"Microphone '{MICROPHONE_NAME}' not found in available devices: {devices}")