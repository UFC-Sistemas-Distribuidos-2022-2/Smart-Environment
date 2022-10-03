import time
import socket
from sensores_pb2 import Sensor_Termico_Geladeira
import random


PORT = 1510
HOST = "localhost"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


temp_freezer = random.uniform(-25, -10)
temp_geladeira = random.uniform(0, 15)

sensor = Sensor_Termico_Geladeira(
    nome="Geladeira Home", temperatura=temp_geladeira, temperatura_freezer=temp_freezer
)


def process_sensor(sensor: Sensor_Termico_Geladeira):

    ruido = random.random() / 2
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(0, sensor.temperatura + fator * ruido), 15)

    ruido = random.random() / 2
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura_freezer = min(max(-25, sensor.temperatura_freezer + fator * ruido), 10)


while True:
    process_sensor(sensor)
    print(sensor.temperatura, sensor.temperatura_freezer)
    s.sendall(sensor.SerializeToString())
    time.sleep(10)
