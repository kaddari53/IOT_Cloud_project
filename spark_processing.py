from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType, ArrayType
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "sensor_data"
CASSANDRA_KEYSPACE = "sensor"
CASSANDRA_TABLE = "gait_data"

spark = SparkSession.builder \
    .appName("KafkaSparkCassandra") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

schema = StructType([
    StructField("timestamp", FloatType(), True),
    StructField("data", ArrayType(FloatType()), True)
])

def process_stream(rdd):
    if not rdd.isEmpty():
        df = spark.read.schema(schema).json(rdd)
        df.write \
            .format("org.apache.spark.sql.cassandra") \
            .mode("append") \
            .options(table=CASSANDRA_TABLE, keyspace=CASSANDRA_KEYSPACE) \
            .save()

if __name__ == "__main__":
    ssc = StreamingContext(spark.sparkContext, 10)
    kafkaStream = KafkaUtils.createDirectStream(ssc, [KAFKA_TOPIC], {"metadata.broker.list": KAFKA_BROKER})
    parsed = kafkaStream.map(lambda v: json.loads(v[1]))
    parsed.foreachRDD(process_stream)
    ssc.start()
    ssc.awaitTermination()
