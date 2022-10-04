import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST

device = Device(
    tipo="device",
    nome="Geladeira",
    id="2",
    temperatura=100,
    temperatura_freezer=100,
)



conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

start_input = Input(tipo="device", dest_id='2')
conn.sendall(start_input.SerializeToString())
temp = 0
while True:
    msg = conn.recv(2048).decode("utf-8")
    if msg == "execute":
        device.temperatura = 5
        device.temperatura_freezer = -20
    conn.sendall(device.SerializeToString())
