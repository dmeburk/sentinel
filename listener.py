from wakeword import detect
from audio.record import record_to_wav
from mqtt.send_audio import send_audio_file
import time

def main():
    while True:
        try:
            print("🧠 Waiting for wake word...")
            detect.listen_for_wake_word()
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"/tmp/command_{timestamp}.wav"
            record_to_wav(filename)  # ← no need to specify device index
            send_audio_file(filename)
        except KeyboardInterrupt:
            print("🛑 Stopped by user")
            break

if __name__ == "__main__":
    main()