# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 demo_2.py
# import findspark
# findspark.init() 

import pandas as pd
import json
# import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType,TimestampType,StructType,StructField

from pyspark.sql.functions import explode, split, col, from_json

# from lib.logger import Log4j

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

# logger = Log4j(spark)

df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test-topic") \
        .option("value_deserializer",lambda m: json.loads(m.decode('utf-8'))) \
        .option("startingOffsets", "earliest") \
        .load()

# df.printSchema()

# value_df = df.select(from_json(col("value").cast("string"),schema).alias("value"))


data = df.select(col("key").cast("string"),from_json(col("value").cast("string"),schema).alias("value"))

# data = value_df.selectExpr("value.Datetime","value.Close")

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
    # print('OP :',type(row))
    df = pd.DataFrame(row)
    print('OP :',df)
    # df = spark.createDataFrame(row)
    # df.write.format("csv").mode("append").save("./../../data/raw/data.csv")
    df.to_csv('./data/raw/data.csv', mode='a', header=False)

#     pass
#     df.write \
#         .format('console') \
#         .option('checkpointLocation','check-points') \
#         .start()

# query = data \
#     .writeStream \
#     .foreachBatch(ForeachWriter()) \
#     .queryName("Flatted Data") \
#     .outputMode("append") \
#     .option("checkpointLocation","check-points") \
#     .start()

query = data.writeStream.foreach(process_row).start()

query.awaitTermination()

# query = data \
#     .writeStream \
#     .outputMode('append') \
#     .format('console') \
#     .option('checkpointLocation','check-points') \
#     .start()

# logger.info('Listening to Kafka')
