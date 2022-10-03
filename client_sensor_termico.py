import time
import socket
from sensores_pb2 import Sensor_Temperatura
import random

PORT = 1510
HOST = "localhost"
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


temp = random.uniform(0, 15)

sensor = Sensor_Temperatura(nome="Cozinha", temperatura=temp)


def process_sensor(sensor: Sensor_Temperatura):

    ruido = random.random() / 2 
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(0, sensor.temperatura + fator * ruido), 35)


while True:
    process_sensor(sensor)
    print(sensor.temperatura)
    conn.send(str(sensor.temperatura).encode("utf-8"))
    # s.sendall(sensor.SerializeToString())
    time.sleep(5)
