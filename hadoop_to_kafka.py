from hdfs import InsecureClient
from kafka import KafkaProducer
import json
import os

HDFS_URL = "http://localhost:50070"
HDFS_PATH = "/user/hadoop/sensor_data/"
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "sensor_data"

hdfs_client = InsecureClient(HDFS_URL, user='hadoop')
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_to_kafka():
    files = hdfs_client.list(HDFS_PATH)
    for file in files:
        with hdfs_client.read(f"{HDFS_PATH}{file}") as reader:
            data = json.load(reader)
            producer.send(KAFKA_TOPIC, data)
            print(f"Sent {data} to Kafka from {file}")
        hdfs_client.delete(f"{HDFS_PATH}{file}")

if __name__ == "__main__":
    send_to_kafka()
