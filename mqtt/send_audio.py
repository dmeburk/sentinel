import paho.mqtt.publish as publish
import base64

def send_audio_file(file_path="command.wav", topic="voice/sentinel-rafa/audio", broker="192.168.0.119", port=1883):
    with open(file_path, "rb") as f:
        audio_data = base64.b64encode(f.read())
    publish.single(topic, payload=audio_data, hostname=broker, port=port)
    print(f"📡 Sent audio to {broker}:{port} on topic '{topic}'")