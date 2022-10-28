import time
from proto.sensores_pb2 import Sensor
import random
import pika


def process_sensor(sensor: Sensor):

    ruido = random.random()/20
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(0.35, sensor.temperatura + fator * ruido), 0.65)


umidade = random.uniform(0.5, 0.6)


sensor = Sensor(
    tipo="umidade",
    nome="Home",
    id=str(random.randrange(5000)),
    temperatura=umidade,
)


def start_client():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # create a hello queue
    channel.queue_declare(queue='sensores')
    print(f"[STARTING] Client is conected")

    while True:
        process_sensor(sensor)
        print(sensor.temperatura)
        #conn.sendall(sensor.SerializeToString())
        channel.basic_publish(exchange='',
                      routing_key='sensores',
                      body=sensor.SerializeToString())
        time.sleep(20)


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
