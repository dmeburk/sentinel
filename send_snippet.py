import paho.mqtt.client as mqtt
import base64
import sys

AUDIO_TOPIC = "voice/sentinel-rafa/audio"
BROKER_ADDRESS = "192.168.0.119"
BROKER_PORT = 1883

# Load and encode audio file
if len(sys.argv) < 2:
    print("Usage: python send_snippet.py /path/to/audio.wav")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, "rb") as f:
    encoded_audio = base64.b64encode(f.read())

# Callback when client connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to broker, sending audio...")
        client.publish(AUDIO_TOPIC, encoded_audio)
    else:
        print(f"❌ Failed to connect, return code {rc}")

# Callback when message is published
def on_publish(client, userdata, mid):
    print("📤 Audio file published")
    client.disconnect()

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
client.loop_forever()

print(f"📦 Sending file: {file_path}")