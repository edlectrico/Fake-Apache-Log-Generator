## Python Kafka Fake Log Producer
This Python module, originally forked from https://github.com/kiritbasu/Fake-Apache-Log-Generator,
aims to generate massive log events to Kafka. More concretelly, we will be
writing into two different topics.

### Creating a topic in Kafka:
To create the 'test' topic in Kafka:
```
./<kafka_path>/bin/kafka-server-start.sh config/server.propertieskafka-server-start.sh config/server.properties
```
```
./<kafka_path>/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

### Checking messages:
To check that the messages are reaching Kafka:
```
./<kafka_path>/bin/kafka-console-consumer --zookeeper localhost:2181 --topic test
```
#### Note:
We assume that you've already run the zookeeper server at localhost:2181. By default:
```
./<kafka_path>/bin/zookeeper-server-start.sh config/zookeeper.properties
```
