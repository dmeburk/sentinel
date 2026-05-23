import pyaudio
import webrtcvad
import collections
from audio_device import find_device_index

RATE = 16000
FRAME_MS = 30  # webrtcvad supports 10, 20, or 30ms frames
FRAME_SIZE = int(RATE * FRAME_MS / 1000)
AGGRESSIVENESS = 2  # 0-3, higher = more aggressive filtering
SPEECH_FRAMES_TRIGGER = 5   # frames of speech before activating
SILENCE_FRAMES_TIMEOUT = 30  # frames of silence before giving up

def listen_for_wake_word():
    vad = webrtcvad.Vad(AGGRESSIVENESS)
    audio = pyaudio.PyAudio()
    device_index = find_device_index()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=FRAME_SIZE
    )

    print("🎤 Listening for speech...")
    ring_buffer = collections.deque(maxlen=SPEECH_FRAMES_TRIGGER)
    silence_count = 0

    try:
        while True:
            frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
            is_speech = vad.is_speech(frame, RATE)
            ring_buffer.append(is_speech)

            if sum(ring_buffer) >= SPEECH_FRAMES_TRIGGER:
                print("🗣️ Speech detected!")
                break

            if is_speech:
                silence_count = 0
            else:
                silence_count += 1
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    listen_for_wake_word()
