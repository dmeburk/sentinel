import base64
import paho.mqtt.client as mqtt
import tempfile
import os
import subprocess


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
client.connect("192.168.0.119", 1883)
client.subscribe("voice/sentinel-rafa/tts")
print("📡 Listening for TTS messages...")
client.loop_forever()