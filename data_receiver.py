import paho.mqtt.client as mqtt
import json
from hdfs import InsecureClient

BROKER_ADDRESS = "localhost"
TOPIC = "sensor/data"
HDFS_URL = "http://localhost:50070"
HDFS_PATH = "/user/hadoop/sensor_data/"

hdfs_client = InsecureClient(HDFS_URL, user='hadoop')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    filename = f"{HDFS_PATH}{data['timestamp']}.json"
    hdfs_client.write(filename, json.dumps(data), overwrite=True)
    print(f"Stored {data} in HDFS at {filename}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_forever()
