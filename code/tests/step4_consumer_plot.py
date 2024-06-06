#!/usr/bin/env python

import json
from kafka import KafkaConsumer
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

# Crear el consumidor de Kafka
consumer = KafkaConsumer(
    'step3-agg',
    group_id='grupo_plot1',
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def create_barplot(data):
    labels = ['Negative', 'Neutral', 'Positive']
    values = [data['NEGATIVE_COUNT'], data['NEUTRAL_COUNT'], data['POSITIVE_COUNT']]
    colors = ['red', 'yellow', 'green']

    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    bars = ax.bar(x, values, color=colors)

    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    ax.set_title('Sentiment Analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    # Add labels
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

#    plt.show()
    plt.show(block=False)
    plt.pause(2)  # Mostrar el gráfico durante 2 segundos
    plt.close()  # Cerrar el gráfico

# Consumir mensajes de Kafka y generar el barplot
for message in consumer:
    data = message.value
    print(f"Received message: {data}")

    # Crear el barplot con los datos recibidos
    create_barplot(data)
    
    consumer.commit()
    

    
    

