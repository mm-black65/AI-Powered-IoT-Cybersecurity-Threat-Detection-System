import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/device01/telemetry"

data = {
    "device": "ESP32_Device01",
    "temperature": 31,
    "humidity": 65,
    "ldr": 420,
    "rssi": -52,
    "heap": 205000,
    "min_heap": 190000,
    "packet_count": 18
}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT)

client.publish(TOPIC, json.dumps(data))

print("Telemetry published successfully!")

client.disconnect()