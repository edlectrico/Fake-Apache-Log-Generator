#!/usr/bin/env python
'''
This Python module, originally forked from https://github.com/kiritbasu/Fake-Apache-Log-Generator,
aims to generate massive log events to Kafka. More concretelly, we will be
writing into two different topics.
'''
import time
import datetime
import pytz
import numpy
import random
import gzip
import zipfile
import sys
import argparse
from random import randrange
import os, ssl

# External imports:
# pip install faker
# pip install tzlocal
from faker import Faker
from tzlocal import get_localzone
local = get_localzone()

import threading, logging, time
# import multiprocessing

# Kafka Producer imports:
# pip install kafka
from kafka import KafkaProducer
from kafka.errors import KafkaError

'''
To create the 'header' and 'ping' topics in Kafka:
./<kafka_path>/bin/kafka-server-start.sh config/server.propertieskafka-server-start.sh config/server.properties
./<kafka_path>/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic header
./<kafka_path>/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ping

To check that the messages are reaching Kafka:
./<kafka_path>/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic header

Note: We assume that you've already run the zookeeper server at localhost:2181. By default:
./<kafka_path>/bin/zookeeper-server-start.sh config/zookeeper.properties
'''

class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while True:
            faker = Faker()

            timestr = time.strftime("%Y%m%d-%H%M%S")
            otime = datetime.datetime.now()

            response=["200","404","500","301"]
            verb=["GET","POST","DELETE","PUT"]
            resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]
            ualist=[faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

            # This field will be used for choosing between topics and, later,
            # for Spark to use them
            headers=["HEADER","PING"]

            ip = faker.ipv4()
            dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
            tz = datetime.datetime.now(local).strftime('%z')
            vrb = numpy.random.choice(verb,p=[0.6,0.1,0.1,0.2])

            #header_agg = random.choice(headers)
            header_agg = numpy.random.choice(headers,p=[0.3,0.7])

            uri = random.choice(resources)
            if uri.find("apps")>0:
                uri += `random.randint(1000,10000)`

        	# resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
            resp = "200"
            byt = int(random.gauss(5000,50))
            referer = faker.uri()
            useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()

            message = '%s - %s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (header_agg,ip,dt,tz,vrb,uri,resp,byt,str(referer),str(useragent))

            if (header_agg=="HEADER"):
                producer.send('header', message)
            else:
                producer.send('ping', message)
            # time between each send action
            time.sleep(0.5)

def main():
    tasks = [
        Producer()
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
