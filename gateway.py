import socket
import threading
from proto.grpc.sensores_pb2 import Sensor, Input, Device, Sensor_List, Device_List
import pika
from constants import PORT, HOST
from signal import signal, SIGPIPE, SIG_DFL
import copy
import grpc
from proto.grpc import sensores_pb2
from proto.grpc import sensores_pb2_grpc

signal(SIGPIPE, SIG_DFL)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(HOST), int(PORT)))

sensores_status = {}
devices_status = {}
devices_conn = {}
SERVER_ADDR = HOST + ":" + str(PORT)


def handle_sensors():

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="sensores")

    sensor = Sensor()

    def callback(ch, method, properties, body):
        sensor.ParseFromString(body)
        sensores_status[sensor.id] = copy.copy(sensor)

    channel.basic_consume(
        queue="sensores",
        on_message_callback=callback,
    )
    print(" [*] Waiting for messages.")
    channel.start_consuming()


def handle_client(conn: socket.socket, input: Input):
    if input.tipo_request == "get":
        if input.tipo_desejado == "sensors":
            sensores_list = Sensor_List()
            sensores_list.sensores.extend(
                [sensores_status[key] for key in sensores_status]
            )
            print("[200] POST OK")
            conn.sendall(sensores_list.SerializeToString())
        elif input.tipo_desejado == "devices":
            devices_list = Device_List()
            devices_list.devices.extend([devices_status[key] for key in devices_status])
            conn.sendall(devices_list.SerializeToString())
            print("[200] POST OK")
    elif input.tipo_request == "post":
        update_device(input)
        conn.send(b"200 OK")

    conn.close()


def handle_device(port):
    with grpc.insecure_channel(port) as channel:
        stub = sensores_pb2_grpc.RouteDeviceStub(channel)
        device = stub.GetDevice(sensores_pb2.Input(tipo="device", tipo_request="get"))
    devices_status[device.id] = device
    devices_conn[device.id] = port


def update_device(input):
    with grpc.insecure_channel(devices_conn[input.dest_id]) as channel:
        stub = sensores_pb2_grpc.RouteDeviceStub(channel)
        device = stub.UpdateDevice(input)
    devices_status[device.id] = device


def start_server():
    thread = threading.Thread(target=handle_sensors)
    thread.start()
    handle_device("localhost:50051")
    handle_device("localhost:50052")
    handle_device("localhost:50053")
    server.listen()
    print(devices_status)
    print(f"[LISTENING] Server is listening on {PORT}")
    while True:
        conn, _ = server.accept()  # wait for a new connection for the server
        data = conn.recv(2048)
        start_input = Input()
        start_input.ParseFromString(data)

        if start_input.tipo == "client":
            thread = threading.Thread(target=handle_client, args=(conn, start_input))
            thread.start()
        else:
            continue


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
