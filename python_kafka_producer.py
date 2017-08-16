#!/usr/bin/env python
import threading, logging, time
import multiprocessing

# Kafka Producer imports:
# pip install kafka
from kafka import KafkaProducer
from kafka.errors import KafkaError

'''
To create the 'test' topic in Kafka:
./<kafka_path>/bin/kafka-server-start.sh config/server.propertieskafka-server-start.sh config/server.properties
./<kafka_path>/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

To check that the messages are reaching Kafka:
./<kafka_path>/bin/kafka-console-consumer --zookeeper localhost:2181 --topic test

Note: We assume that you've already run the zookeeper server at localhost:2181. By default:
./<kafka_path>/bin/zookeeper-server-start.sh config/zookeeper.properties
'''

class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while True:
            # producer.send(<topic>, <message>)
            producer.send('test', b"test")
            producer.send('test', b"\xc2Hola, mundo!")
            time.sleep(1)

# This part is to test that the producer works. To test it, just uncomment the
# code and run 'python python_kafka_producer.py' in your terminal
'''
def main():
    tasks = [
        Producer()
        #, Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
'''
