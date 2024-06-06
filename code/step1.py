#!/usr/bin/env python

import json
import logging
import pandas as pd
import time
from kafka import KafkaProducer

# logger
log = logging.getLogger(__name__)

# productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def on_send_success(record_metadata):
    print(f"Tópico: {record_metadata.topic}, Partición: {record_metadata.partition}, Offset: {record_metadata.offset}")


def on_send_error(ex):
    log.error('Error en la producción del mensaje', exc_info=ex)

def produce_from_csv():
    csv_file = 'input_csv2.csv'
    
    df = pd.read_csv(csv_file)
    
    for index, row in df.iterrows():
    
        message = row.to_dict()
        producer.send('step1-ingest', value=message).add_callback(on_send_success).add_errback(on_send_error)
        print(f"Enviando mensaje: {json.dumps(message)}")
        
    
        time.sleep(2)
    
    producer.flush()
    producer.close()

produce_from_csv()

