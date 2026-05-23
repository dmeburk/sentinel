import pyaudio
import numpy as np
import openwakeword
from openwakeword.model import Model
from audio_device import find_device_index

oww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

CHUNK = 1280  # openWakeWord expects 80ms chunks at 16kHz

def listen_for_wake_word():
    audio = pyaudio.PyAudio()
    device_index = find_device_index()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=CHUNK
    )

    print("🎤 Listening for wake word 'hey jarvis'...")
    try:
        while True:
            pcm = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            prediction = oww_model.predict(pcm)
            if prediction.get("hey_jarvis", 0) > 0.5:
                print("🗣️ Wake word detected!")
                break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    listen_for_wake_word()
