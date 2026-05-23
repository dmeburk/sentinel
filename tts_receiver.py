import base64
import paho.mqtt.client as mqtt
import tempfile
import os
import subprocess
from sentinel_config import SENTINEL_NAME, MQTT_BROKER, MQTT_PORT


def on_message(client, userdata, msg):
    print("📥 Received TTS message")
    audio_data = base64.b64decode(msg.payload)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_data)
        tmp.flush()
        subprocess.run(["aplay", tmp.name], check=False)
        os.remove(tmp.name)

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(f"voice/{SENTINEL_NAME}/tts")
print(f"📡 Listening for TTS messages on voice/{SENTINEL_NAME}/tts...")
client.loop_forever()