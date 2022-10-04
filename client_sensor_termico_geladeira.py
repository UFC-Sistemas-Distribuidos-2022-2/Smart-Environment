import time
import socket
from sensores_pb2 import Sensor, Input
import random
from constants import PORT, HOST

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


temp_freezer = random.uniform(-25, -10)
temp_geladeira = random.uniform(1, 7)

sensor = Sensor(
    tipo="geladeira",
    nome="Geladeira Home",
    id="2",
    temperatura=temp_geladeira,
    temperatura_freezer=temp_freezer
)

start_input = Input(tipo="sensor", dest_id="2")
conn.sendall(start_input.SerializeToString())


def process_sensor(sensor: Sensor):

    ruido = random.random()
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(5, sensor.temperatura + fator * ruido), 15)

    ruido = random.random() 
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura_freezer = min(
        max(-25, sensor.temperatura_freezer + fator * ruido), 10
    )


while True:
    process_sensor(sensor)
    print(sensor.temperatura, sensor.temperatura_freezer)
    conn.sendall(sensor.SerializeToString())
    time.sleep(10)
