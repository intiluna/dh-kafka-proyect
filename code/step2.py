#!/usr/bin/env python

#!/usr/bin/env python

import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# VADER
nltk.download('vader_lexicon')

# Instanciar sentimientos de VADER
sid = SentimentIntensityAnalyzer()

log = logging.getLogger(__name__)

# productor
producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)


def on_send_success(record_metadata):
    print(f"Tópico: {record_metadata.topic}, Partición: {record_metadata.partition}, Offset: {record_metadata.offset}")


def on_send_error(ex):
    log.error('Error en la producción del mensaje', exc_info=ex)

# analisis de sentimiento
def analyze_sentiment(text):
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "Positive"
    elif scores['compound'] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# consumidor
consumer = KafkaConsumer(
    'step1-ingest',
    group_id='p2',
    bootstrap_servers=['127.0.0.1:9092', '127.0.0.1:9093', '127.0.0.1:9094'],
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


for message in consumer:

    json_message = message.value
    text = json_message['text']
    
    sentiment = analyze_sentiment(text)

    print(f"Texto: {text}")
    print(f"Sentimiento: {sentiment}")
    
    json_message['sentiment'] = sentiment
    
    producer.send('step2-sa', value=json_message).add_callback(on_send_success).add_errback(on_send_error)
    print(f"Reenviado al tópico 'step2-sa': {json.dumps(json_message, indent=2)}")

producer.flush()
consumer.close()
producer.close()

