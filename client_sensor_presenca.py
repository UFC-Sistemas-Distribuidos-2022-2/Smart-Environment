import time
import socket
from sensores_pb2 import Sensor, Input
import random
from constants import PORT, HOST

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


temp = random.uniform(20, 32)
nome = "Sensor Presenca"


sensor = Sensor(
    tipo="presenca", nome=nome, id="15", presenca=False
)
start_input = Input(tipo="sensor", dest_id="15")
conn.sendall(start_input.SerializeToString())
time.sleep(1)


def process_sensor(sensor: Sensor):
    sensor.presenca = bool(random.getrandbits(1))


while True:
    process_sensor(sensor)
    print(sensor.presenca)
    conn.sendall(sensor.SerializeToString())
    time.sleep(10)