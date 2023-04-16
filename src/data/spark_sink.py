# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 demo_2.py
import pathlib
import sys

import pandas as pd
import numpy as np
import json
# import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType,TimestampType,StructType,StructField

from pyspark.sql.functions import explode, split, col, from_json

# from lib.logger import Log4j
# import subprocess

# print('CWD :',pathlib.Path.cwd())

# cmd_str = "park-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 src/data/spark_sink.py"
# subprocess.run(cmd_str, shell=False)

schema = StructType([
    StructField("Datetime",TimestampType()),
    StructField("Open",IntegerType()),
    StructField("High",IntegerType()),
    StructField("Low",IntegerType()),
    StructField("Close",IntegerType()),
    StructField("Volume",IntegerType())
])


# spark = SparkSession.builder \
#     .master("local[4]") \
#     .appName("KafkaSpark") \
#     .config("spark.streaming.stopGracefullyOnShutdown", "true") \
#     .config("spark.sql.shuffle.partitions", 3) \
#     .getOrCreate()


spark = SparkSession.builder \
    .master("local[4]") \
    .appName("KafkaSpark") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel('OFF')

# logger = Log4j(spark)

df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test-topic") \
        .option("value_deserializer",lambda m: json.loads(m.decode('utf-8'))) \
        .option("startingOffsets", "earliest") \
        .load()

# df.printSchema()

value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))


# data = df.select(col("key").cast("string"),from_json(col("value").cast("string"),schema).alias("value"))

data = value_df.selectExpr("value.Datetime","value.Close")

# data.printSchema()
# # Generate running word count
# wordCounts = words.groupBy('word').count()

# # Start running the query that prints the running counts to the console
# query = data \
#     .writeStream \
#     .format("json") \
#     .queryName("Flatted Data") \
#     .outputMode("append") \
#     .option("path","output") \
#     .option("checkpointLocation","check-points") \
#     .start()

# query.awaitTermination()


class ForeachWriter:
    def open(self, partition_id, epoch_id):
        # Open connection. This method is optional in Python.
        pass

    def process(self, row):
        # Write row to connection. This method is NOT optional in Python.
        row.write.console.start()
        # pass

    def close(self, error):
        # Close the connection. This method in optional in Python.
        pass

def process_row(row):
    print('A :',row)
    x = list(row)
    print('B :', x)
    df = pd.DataFrame(np.array([list(row)]), columns=['Datetime', 'Close'])
    print('C :',df)
    # df = spark.createDataFrame(row)
    # df.write.format("csv").mode("append").save("./../../data/raw/data.csv")
    df.to_csv('./data/raw/data.csv', mode='a', header=False, index=False)

# query = data.writeStream \
#     .foreach(process_row) \
#     .option('checkpointLocation','check-points') \
#     .outputMode('append') \
#     .start()

def initial_load():
    print('Spark Checking')
    
    # query = data.writeStream \
    #     .foreach(process_row) \
    #     .option('checkpointLocation','check-points') \
    #     .outputMode('append') \
    #     .start()
    
    print('Spark Checking')
    query = data.writeStream \
        .foreach(process_row) \
        .option('checkpointLocation','check-points') \
        .outputMode('append') \
        .start()

    query.awaitTermination()

# query = data \
#     .writeStream \
#     .outputMode('append') \
#     .format('console') \
#     .option('checkpointLocation','check-points') \
#     .start()


# query.awaitTermination()

# logger.info('Listening to Kafka')

if __name__ == '__main__':
    
    initial_load()
    # if sys.argv[1]=='historic':
    #     pass

    # if sys.argv[1]=='live':
    #     pass