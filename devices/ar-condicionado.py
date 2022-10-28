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
    tipo="ar_condicionado",
    nome="brastemp-4000",
    id=str(random.randrange(500)),
    temperatura=18,
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
            device.temperatura = max(input.temperatura, 16)
            device.ligado = input.ligado
        conn.sendall(device.SerializeToString())



# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_client()