import json
from flask import Flask, render_template, Response
from kafka import KafkaConsumer
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# Configurar Matplotlib
plt.switch_backend('Agg')

app = Flask(__name__)

# Configuracion Kafka
TOPIC_NAME = "step3-agg"
KAFKA_SERVER = 'localhost:9092'
CONSUMER_GROUP = 'flask-group'

# Consumidor
consumer = KafkaConsumer(
    TOPIC_NAME,
    group_id=CONSUMER_GROUP,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Almacena ultimo mensaje
last_message = {'NEGATIVE_COUNT': 0, 'NEUTRAL_COUNT': 0, 'POSITIVE_COUNT': 0, 'TOTAL_COUNT': 0}

def consume_messages():
    global last_message
    for message in consumer:
        if message.value:
            last_message = message.value
            print(f"Received message: {last_message}")
            break

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

    # Mostrar valores en las barras (no se ve bien)
    # for bar in bars:
    #     height = bar.get_height()
    #     ax.annotate(f'{height}',
    #                 xy=(bar.get_x() + bar.get_width() / 2, height),
    #                 xytext=(0, 3),  
    #                 textcoords="offset points",
    #                 ha='center', va='bottom')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8') # para no tener que guardar plot en un fichero aparte y subirlo
    plt.close(fig)
    return plot_url

@app.route('/')
def index():
    consume_messages()
    plot_url = create_barplot(last_message)
    return render_template('index.html', plot_url=plot_url, data=last_message)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

