import pika
import time


sleepTime = 2

print('Service A')
print(f"[*] Sleep de {sleepTime} segundos.")
time.sleep(sleepTime)

print('[*] Conectando no servidor  ...')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1')
)
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print('[*] Aguardando mensagens')


def send_to_next(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1')
    )

    channel = connection.channel()
    # channel.queue_declare(queue='task_queue_b', durable=True)
    channel.basic_publish(
        exchange='events',
        routing_key='event.calc',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
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


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
