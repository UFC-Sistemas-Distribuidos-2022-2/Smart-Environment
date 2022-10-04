import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

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
conn.sendall(device.SerializeToString())
while True:
    msg = conn.recv(2048).decode("utf-8")
    if msg == "execute":
        device.temperatura = 5
        device.temperatura_freezer = -20
    conn.sendall(device.SerializeToString())
