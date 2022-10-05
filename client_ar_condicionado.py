import socket
from sensores_pb2 import Device, Input
from constants import PORT, HOST
from signal import signal, SIGPIPE, SIG_DFL
import time
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
time.sleep(1)
conn.sendall(device.SerializeToString())
while True:
    data = conn.recv(2048)
    input = Input()
    input.ParseFromString(data)
    print(input)
    if input.tipo_request == "post":
        device.temperatura = max(input.temperatura,17)
        device.ligado = input.ligado
    conn.sendall(device.SerializeToString())
