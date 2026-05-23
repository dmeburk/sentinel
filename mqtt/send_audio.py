import paho.mqtt.publish as publish
import base64
from sentinel_config import SENTINEL_NAME, MQTT_BROKER, MQTT_PORT

def send_audio_file(file_path="command.wav"):
    topic = f"voice/{SENTINEL_NAME}/audio"
    with open(file_path, "rb") as f:
        audio_data = base64.b64encode(f.read())
    publish.single(topic, payload=audio_data, hostname=MQTT_BROKER, port=MQTT_PORT)
    print(f"📡 Sent audio to {MQTT_BROKER}:{MQTT_PORT} on topic '{topic}'")
