import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST
import time

device = Device(
    tipo="lampada",
    nome="lamp led 3000",
    id="102",
    ligado=False
)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

start_input = Input(tipo="device", dest_id='102')
conn.sendall(start_input.SerializeToString())
time.sleep(1)
conn.sendall(device.SerializeToString())

while True:
    data = conn.recv(2048)
    input = Input()
    input.ParseFromString(data)
    print(input)
    if input.tipo_request == "post":
        device.ligado = input.ligado
    conn.sendall(device.SerializeToString())
