import paho.mqtt.client as mqtt
import time
import json
import os

BROKER_ADDRESS = "localhost"
TOPIC = "sensor/data"
DATA_DIR = "/home/segula/Desktop/Project_iot_cloud/gait-in-parkinsons-disease-1.0.0"  

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def publish_data(client):
    for root, _, files in os.walk(DATA_DIR):
        for filename in files:
            if filename.endswith(".txt"):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    for line in file:
                        if line.strip():
                            data = line.strip().split()
                            payload = {
                                "timestamp": float(data[0]),
                                "data": [float(value) for value in data[1:]]
                            }
                            client.publish(TOPIC, json.dumps(payload))
                            print(f"Published {payload} from {filename}")
                            time.sleep(0.1)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_start()
    publish_data(client)
