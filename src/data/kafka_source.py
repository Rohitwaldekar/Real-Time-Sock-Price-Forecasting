import sys

import json
from kafka import KafkaProducer
from time import sleep

import yfinance as yf

class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send_msg(self):
        print("Sending message...")
        # random_values = [1,2,3,4,5,6,7,8,9]

        # while True:
            # "^NSEI"

        nifty = yf.Ticker("RELIANCE.NS")
        df = nifty.history(period="2y", interval="1h")
        df.reset_index(inplace=True)
        for a in df.values:
            data = {
                "Datetime": str(a[0]),
                "Open": int(a[1]),
                "High": int(a[2]),
                "Low": int(a[3]),
                "Close": int(a[4]),
                "Volume": int(a[5])
            }
            print(data)
            self.producer.send(self.topic,data)
            self.producer.flush()
            # sleep(60*1)

def initial_data():
    broker = 'localhost:9092'
    topic = 'test-topic'

    message_producer = MessageProducer(broker,topic)
    message_producer.send_msg()


if __name__ == '__main__':
    
    initial_data()
    
    # if sys.argv[1]=='historic':
    #     pass

    # if sys.argv[1]=='live':
    #     pass