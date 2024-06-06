#!/usr/bin/env python

import json
from kafka import KafkaConsumer
import pymongo
from pymongo import MongoClient

# Crear el consumidor de Kafka
consumer = KafkaConsumer(
    'step3-agg',
    group_id='grupo_escucha1',
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

consumer.subscribe(['step3-agg'])


for message in consumer:
    # Decodificar el mensaje JSON
    json_message = message.value
    print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={json.dumps(json_message, indent=2)}")

    
    

