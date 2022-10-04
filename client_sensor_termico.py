import time
import socket
from sensores_pb2 import Sensor, Input
import random
from constants import PORT, HOST

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


temp = random.uniform(20, 32)
nome = "Sensor Térmico"


sensor = Sensor(
    tipo="termico", nome=nome, id="1", temperatura=temp
)
start_input = Input(tipo="sensor", dest_id="1")
conn.sendall(start_input.SerializeToString())


def process_sensor(sensor: Sensor):

    ruido = random.random() / 2
    fator = random.randrange(-1, 2, 1)

    sensor.temperatura = min(max(20, sensor.temperatura + fator * ruido), 32)


while True:
    process_sensor(sensor)
    print(sensor.temperatura)
    conn.sendall(sensor.SerializeToString())
    time.sleep(10)
