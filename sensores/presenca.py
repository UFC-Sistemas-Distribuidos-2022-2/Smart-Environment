
import struct
import socket
import time
from proto.sensores_pb2 import Sensor, Input
from constants import MCAST_GRP, MCAST_PORT
from typing import Tuple
import random


def process_sensor(sensor: Sensor):
    sensor.presenca = bool(random.getrandbits(1))


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


sensor = Sensor(
    tipo="presenca", nome="PresencaX", id=str(random.randrange(5000)), presenca=False
)


def start_client():
    host, port = get_server()
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))
    print(f"[STARTING] Client is conected to {host}:{port}")
    start_input = Input(tipo="sensor", dest_id=sensor.id)
    conn.sendall(start_input.SerializeToString())
    time.sleep(1)
    conn.sendall(sensor.SerializeToString())

    while True:
        process_sensor(sensor)
        conn.sendall(sensor.SerializeToString())
        time.sleep(10)


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()
