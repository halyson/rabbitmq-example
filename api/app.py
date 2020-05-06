from flask import Flask, jsonify
import pika
import os

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/message/<cmd>')
def add(cmd):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    response = {'mensagem': cmd}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
