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


def handle_1():

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="sensores")

    sensor = Sensor()

    def callback(ch, method, properties, body):
        # print(" [x] Received %r" % body)
        sensor.ParseFromString(body)
        print(sensor.id, sensor.tipo)
        sensores_status[sensor.id] = copy.copy(sensor)

    channel.basic_consume(
        queue="sensores",
        on_message_callback=callback,
    )
    print(" [*] Waiting for messages. To exit press CTRL+C")
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

    conn.close()


def handle_sensor(conn: socket.socket, id: str):
    connected = True
    nome = ""
    if sensores_status.get(id):
        connected = False
        print("ID já registrado, altere as configurações do seu aparelho")
    else:
        sensores_status[id] = Sensor()
        print("<>Conected to a sensor<>")
    while connected:
        try:
            data = conn.recv(2048)
            if not data:
                sensores_status.pop(id)
                print(f"Dispositivo desconectado - {nome}")
                connected = False
            else:
                sensor = Sensor()
                sensor.ParseFromString(data)
                sensores_status[id] = sensor
                nome = sensor.nome
                print(f"<{sensor.id}-{sensor.nome}>:{sensor.temperatura}")

        except Exception as e:
            print(e)
            connected = False
            sensores_status.pop(id)
    conn.close()


def handle_device(port):
    print("Will try to greet world ...")
    with grpc.insecure_channel(port) as channel:
        stub = sensores_pb2_grpc.RouteDeviceStub(channel)
        device = stub.GetDevice(sensores_pb2.Input(tipo="device", tipo_request="get"))
    devices_status[device.id] = device
    devices_conn[device.id] = port


def update_device(input):
    print("Will try to greet world ...")
    with grpc.insecure_channel(devices_conn[input.dest_id]) as channel:
        stub = sensores_pb2_grpc.RouteDeviceStub(channel)
        device = stub.UpdateDevice(input)
    devices_status[device.id] = device


def start_server():
    thread = threading.Thread(target=handle_1)
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

        if start_input.tipo == "sensor":
            thread = threading.Thread(
                target=handle_sensor, args=(conn, start_input.dest_id)
            )
            thread.start()
        elif start_input.tipo == "device":
            thread = threading.Thread(
                target=handle_device, args=(conn, start_input.dest_id)
            )
            thread.start()
        elif start_input.tipo == "client":
            thread = threading.Thread(target=handle_client, args=(conn, start_input))
            thread.start()
        else:
            continue


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
