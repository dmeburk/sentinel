from wakeword import detect
from audio.record import record_to_wav
from mqtt.send_audio import send_audio_file
import time

def main():
    while True:
        try:
            print("🧠 Waiting for wake word...")
            detect.listen_for_wake_word()
            time.sleep(0.3)  # brief pause to catch the start of the command
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"/tmp/command_{timestamp}.wav"
            record_to_wav(filename, duration=6)
            send_audio_file(filename)
        except KeyboardInterrupt:
            print("🛑 Stopped by user")
            break

if __name__ == "__main__":
    main()