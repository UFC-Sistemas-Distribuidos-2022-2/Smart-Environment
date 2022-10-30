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
from proto.grpc import sensores_pb2
from proto.grpc import sensores_pb2_grpc

device = sensores_pb2.Device(tipo="lampada", nome="led-100", id="2", ligado=False)


class ArCondicionado(sensores_pb2_grpc.RouteDeviceServicer):
    def GetDevice(self, request, context):
        return device

    def UpdateDevice(self, request, context):
        device.ligado = request.ligado
        return device


def serve():
    port = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensores_pb2_grpc.add_RouteDeviceServicer_to_server(ArCondicionado(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    print("[STARTING] Server-Device is starting...")
    serve()
