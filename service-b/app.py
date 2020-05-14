import pika
import time
from random import randint
import os

SLEEP_TIME = 10
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')


def process_cmd(cmd):
    time.sleep(5)
    number = randint(0, 100)
    if cmd == 20:
        raise Exception("Erro")
    elif number % 2:
        print("[+] Par")
        return True
    else:
        print("[-] Impar")
        return False


def callback(ch, method, properties, body):
    print(f"[*] Recebido: {body}")
    cmd = body.decode()

    try:
        response = process_cmd(cmd)
        if response:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("[x] Precessado")
        else:
            # basic_nack tem o mesmo efeito, diferenca apenas semantica
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as e:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        print("[ ] Rejeitado")
        pass


print('Service B')
print(f"[*] Sleep de {SLEEP_TIME} segundos.")
time.sleep(SLEEP_TIME)

print("[*] Conectando no servidor  ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# neste caso a queue já esta declarada na configuração da exchange do rabbitmq no definitions.json
# channel.queue_declare(queue='task_queue_b', durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue_b', on_message_callback=callback)
channel.start_consuming()
print("[*] Aguardando mensagens")
