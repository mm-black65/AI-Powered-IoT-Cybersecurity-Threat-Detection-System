import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "iot/telemetry"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected!")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    print("---------------------")
    print("Temperature :", data["temperature"])
    print("Humidity    :", data["humidity"])
    print("LDR         :", data["ldr"])
    print("RSSI        :", data["rssi"])
    print("Heap        :", data["heap"])
    print("---------------------")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()