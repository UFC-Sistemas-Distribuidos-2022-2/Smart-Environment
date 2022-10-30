import time
from proto.sensores_pb2 import Sensor
import random
import pika


def process_sensor(sensor: Sensor):
    sensor.presenca = bool(random.getrandbits(1))


temp = random.uniform(23, 30)


sensor = Sensor(
    tipo="presenca", nome="PresencaX", id=str(random.randrange(5000)), presenca=False
)


def start_client():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    # create a hello queue
    channel.queue_declare(queue="sensores")
    print(f"[STARTING] Client is conected")

    while True:
        process_sensor(sensor)

        # conn.sendall(sensor.SerializeToString())
        channel.basic_publish(
            exchange="", routing_key="sensores", body=sensor.SerializeToString()
        )
        time.sleep(5)


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
