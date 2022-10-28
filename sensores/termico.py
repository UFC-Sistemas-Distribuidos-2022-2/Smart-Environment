import time
from proto.sensores_pb2 import Sensor
import random
import pika


def process_sensor(sensor: Sensor):

    ruido = random.random()
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(22, sensor.temperatura + fator * ruido), 33)


temp = random.uniform(23, 30)


sensor = Sensor(
    tipo="termico",
    nome="Home",
    id=str(random.randrange(5000)),
    temperatura=temp,
)


def start_client():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # create a hello queue
    channel.queue_declare(queue='sensores')
    print(f"[STARTING] Client is conected")

    while True:
        process_sensor(sensor)

        #conn.sendall(sensor.SerializeToString())
        channel.basic_publish(exchange='',
                      routing_key='sensores',
                      body=sensor.SerializeToString())
        time.sleep(5)


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
