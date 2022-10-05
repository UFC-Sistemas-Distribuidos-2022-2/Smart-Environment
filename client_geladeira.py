import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST
import time


device = Device(
    tipo="geladeira",
    nome="Geladeira",
    id="101",
    temperatura=100,
    temperatura_freezer=100,
    ligado=False
)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

start_input = Input(tipo="device", dest_id='101')
conn.sendall(start_input.SerializeToString())
time.sleep(1)
conn.sendall(device.SerializeToString())
while True:
    data = conn.recv(2048)
    input = Input()
    input.ParseFromString(data)
    print(input)
    if input.tipo_request == "post":
        device.temperatura = 5
        device.temperatura_freezer = -20
        device.ligado = input.ligado
    conn.sendall(device.SerializeToString())
