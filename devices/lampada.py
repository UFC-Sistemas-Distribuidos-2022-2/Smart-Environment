import struct
import socket
import time
from typing import Tuple
import random

from proto.sensores_pb2 import Device, Input
from constants import MCAST_GRP, MCAST_PORT


def get_server() -> Tuple[str, int]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    data, _ = sock.recvfrom(1024)
    sock.close()
    data = data.decode()
    host = data.split(":")[0]
    port = int(data.split(":")[1])
    return (host, port)


device = Device(
    tipo="lampada",
    nome="lamp led 3000",
    id=str(random.randrange(5000)),
    ligado=False
)


def start_client():
    host, port = get_server()
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))
    print(f"[STARTING] Client is conected to {host}:{port}")
    start_input = Input(tipo="device", dest_id=device.id)
    conn.sendall(start_input.SerializeToString())
    time.sleep(1)
    conn.sendall(device.SerializeToString())

    while True:
        data = conn.recv(2048)
        input = Input()
        input.ParseFromString(data)
        if input.tipo_request == "post":
            device.ligado = input.ligado
        conn.sendall(device.SerializeToString())


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
