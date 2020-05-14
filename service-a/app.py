import pika
import time
import os

SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def send_to_next(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()
    channel.basic_publish(
        exchange='events',
        routing_key='event.calc',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensagens persistentes
        )
    )
    connection.close()


def callback(ch, method, properties, body):
    print(f"[*] Recebido: {body}")
    cmd = body.decode()

    if cmd == 'entregar':
        send_to_next(cmd)
        print("[+] Entregue")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        print("[ ] Rejeitada")


print('Service A')
print(f"[*] Sleep de {SLEEP_TIME} segundos.")
time.sleep(SLEEP_TIME)

print('[*] Conectando no servidor  ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
print('[*] Aguardando mensagens')
