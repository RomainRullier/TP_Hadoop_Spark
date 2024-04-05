from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag
from pyspark.sql.window import Window


spark = SparkSession.builder \
    .appName("Analyse temporelle sismique") \
    .getOrCreate()
data = spark.read.csv("hdfs://namenode:9000/data/dataset_sismique_villes.csv", header=True)

data = data.select("ville", "secousse", "magnitude", "tension entre plaque", "date")
data = data.withColumn("date", col("date").cast("timestamp"))

windowSpec = Window.orderBy("date")

data = data.withColumn("previous_magnitude", lag("magnitude", 1).over(windowSpec))
data = data.withColumn("magnitude_difference", col("magnitude") - col("previous_magnitude"))

sequences = data.filter((col("magnitude_difference") > 0) & (col("magnitude_difference") < 1))
sequences.write.format("json").save("hdfs://namenode:9000/results/sequences")

sequences.show()

spark.stop()
