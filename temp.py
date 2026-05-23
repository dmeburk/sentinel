from pvrecorder import PvRecorder

devices = PvRecorder.get_available_devices()
for i, device in enumerate(devices):
    print(f"[{i}] {device}")