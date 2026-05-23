import pyaudio
import webrtcvad
import collections
import audioop
from audio_device import find_device_index

DEVICE_RATE = 48000   # AIRHUG native rate
VAD_RATE = 16000      # webrtcvad requires 8000, 16000, 32000, or 48000
FRAME_MS = 30
FRAME_SIZE = int(DEVICE_RATE * FRAME_MS / 1000)
AGGRESSIVENESS = 2
SPEECH_FRAMES_TRIGGER = 5
SILENCE_FRAMES_TIMEOUT = 30

def listen_for_wake_word():
    vad = webrtcvad.Vad(AGGRESSIVENESS)
    audio = pyaudio.PyAudio()
    device_index = find_device_index()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=DEVICE_RATE,
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
            downsampled, _ = audioop.ratecv(frame, 2, 1, DEVICE_RATE, VAD_RATE, None)
            is_speech = vad.is_speech(downsampled, VAD_RATE)
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
