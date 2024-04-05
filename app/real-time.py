from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder.appName("StocksToHDFS").getOrCreate()

spark.sparkContext.setLogLevel("WARN")

kafka_topic_name = "seisme-real-time"

kafka_bootstrap_servers = 'kafka:9093'

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .option("startingOffsets", "earliest") \
    .load()

df = df.selectExpr("CAST(value AS STRING)")


query = df \
    .writeStream.outputMode("append") \
    .format("console") \
    .start()
query.awaitTermination()
