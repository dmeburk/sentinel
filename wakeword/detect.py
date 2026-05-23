import pvporcupine
from pvrecorder import PvRecorder
from audio_device import find_device_index

def listen_for_wake_word(keyword="porcupine"):
    porcupine = pvporcupine.create(
        access_key="jY9OXpqEumzSPY+xsSW8h+v+kp3bsjiGx99+UN4HKa48OU82D8eUXw==",
        keywords=[keyword]
    )

    device_index = find_device_index()
    recorder = PvRecorder(device_index=device_index, frame_length=porcupine.frame_length)

    try:
        recorder.start()
        print(f"🎤 Listening for wake word '{keyword}' on device {device_index}...")
        while True:
            pcm = recorder.read()
            if porcupine.process(pcm) >= 0:
                print(f"🗣️ Wake word '{keyword}' detected!")
                break
    finally:
        recorder.stop()
        porcupine.delete()
        recorder.delete()

if __name__ == "__main__":
    listen_for_wake_word()