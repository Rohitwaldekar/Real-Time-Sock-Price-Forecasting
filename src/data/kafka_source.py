import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep
from random import choice


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
        random_values = [1,2,3,4,5,6,7,8,9]

        while True:
            random = choice(random_values)
            data = {
                "random_values": random,
                "timestamp": str(datetime.now()),
                "value_status": "High" if random > 5 else "Low"
            }
            print(data)
            self.producer.send(topic,data)
            self.producer.flush()
            sleep(3)


broker = 'localhost:9092'
topic = 'test-topic'

message_producer = MessageProducer(broker,topic)
message_producer.send_msg()