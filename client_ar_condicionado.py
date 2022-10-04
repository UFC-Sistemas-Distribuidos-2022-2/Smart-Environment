import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

device = Device(
    tipo="ar_condicionado",
    nome="brastemp-4000",
    id="100",
    temperatura=18,
    ligado=False
)

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

start_input = Input(tipo="device", dest_id='100')
conn.sendall(start_input.SerializeToString())
temp = 0
conn.sendall(device.SerializeToString())
while True:
    msg = conn.recv(2048).decode("utf-8")
    if msg == "execute":
        device.temperatura = 5
        device.temperatura_freezer = -20
    conn.sendall(device.SerializeToString())
