#!/usr/bin/env python

import json
from kafka import KafkaConsumer
import pymongo
from pymongo import MongoClient
from pprint import pprint

# Crear el consumidor de Kafka
consumer = KafkaConsumer(
    'step2-sa',
    group_id='ptest-3',
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

consumer.subscribe(['step2-sa'])



for message in consumer:
     # Decodificar el mensaje JSON
     json_message = message.value
     print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={json.dumps(json_message, indent=2)}")


