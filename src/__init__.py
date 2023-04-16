# Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

import sys
import os
import subprocess
import threading
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define function to run Kafka producer
def run_kafka_producer():
    logging.info("Starting Kafka producer...")
    os.system("python3 src/data/kafka_source.py")

# Define function to run Spark streaming
def run_spark_streaming():
    logging.info("Starting Spark streaming...")
    os.system("spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 src/data/spark_sink.py")

# Define function to run Dash app
def run_dash_app():
    logging.info("Starting Dash app...")
    os.system("python3  src/app/app.py")

def start_process():
    # Create threads for each process
    dash_thread = threading.Thread(target=run_dash_app)
    kafka_thread = threading.Thread(target=run_kafka_producer)
    spark_thread = threading.Thread(target=run_spark_streaming)
    

    # Start threads
    dash_thread.start()
    kafka_thread.start()
    spark_thread.start()
    

    # Wait for threads to finish
    dash_thread.join()
    kafka_thread.join()
    spark_thread.join()
    


def historic_data():
    start_process()

def live_data():
    pass

if __name__ == '__main__':
    
    if sys.argv[1]=='historic':
        historic_data()
