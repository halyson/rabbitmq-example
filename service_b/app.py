import pika
import time
from random import randint

sleepTime = 2


print('Service B')
print(f"[*] Sleep de {sleepTime} segundos.")
time.sleep(sleepTime)

print("[*] Conectando no servidor  ...")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()
channel.queue_declare(queue='task_queue_b', durable=True)

print("[*] Aguardando mensagens")


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
        else:
            # basic_nack tem o mesmo efeito, diferenca apenas semantica
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

    except Exception as e:
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        print("[ ] Rejeitado")
        pass


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue_b', on_message_callback=callback)
channel.start_consuming()
