#!/usr/bin/env python

import json
from kafka import KafkaConsumer
import pymongo
from pymongo import MongoClient
from pprint import pprint

# consumidor
consumer = KafkaConsumer(
    'step2-sa',
    group_id='p3',
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

consumer.subscribe(['step2-sa'])


# Mongodb
try:
    #client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient('mongodb://admin:admin@localhost:27017/') # se llama por localhost, no por nombre de container (usado cuando llama de un container a otro)
    client.drop_database("proyecto_inti")
    db = client["proyecto_inti"]
    maletas_full = db["full_data"]
    print("Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"Error al intentar conectar a MongoDB: {e}")
    exit(1)  # Salir si no se puede conectar a MongoDB

# for message in consumer:
#     # Decodificar el mensaje JSON
#     json_message = message.value
#     print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={json.dumps(json_message, indent=2)}")

for message in consumer:
    
    json_message = message.value
    print(f"{message.topic}:{message.partition}:{message.offset}:value={json.dumps(json_message, indent=2)}")
    try:
        print("Guardando en MongoDB...")
        maletas_full.insert_one(json_message)
        print("Documento guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el mensaje en MongoDB: {e}")
