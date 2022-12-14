import socket
import threading
from proto.sensores_pb2 import Sensor, Input, Device, Sensor_List, Device_List
import time
from constants import PORT, HOST, MCAST_GRP, MCAST_PORT
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(HOST), int(PORT)))

sensores_status = {}
devices_status = {}
devices_conn = {}
SERVER_ADDR = HOST+':'+str(PORT)


def handle_connections():
    while True:
        try:
            TTL = 2
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
            sock.sendto(SERVER_ADDR.encode(), (MCAST_GRP, MCAST_PORT))
            sock.close()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            pass


def handle_client(conn: socket.socket, input: Input):
    if input.tipo_request == "get":
        if input.tipo_desejado == "sensors":
            sensores_list = Sensor_List()
            sensores_list.sensores.extend([sensores_status[key]
                                           for key in sensores_status])
            print("[200] POST OK")
            conn.sendall(sensores_list.SerializeToString())
        elif input.tipo_desejado == "devices":
            devices_list = Device_List()
            devices_list.devices.extend([devices_status[key] for key in devices_status])
            conn.sendall(devices_list.SerializeToString())
            print("[200] POST OK")
    elif input.tipo_request == "post":
        if devices_conn.get(input.dest_id):
            devices_conn[input.dest_id].sendall(input.SerializeToString())
            print("[200] POST OK")

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


def handle_device(conn: socket.socket, id: str):
    connected = True

    if devices_status.get(id):
        connected = False
        print("ID já registrado, altere as configurações do seu aparelho")
    else:
        devices_status[id] = Device()
        devices_conn[id] = conn
        print("<>Conected to a Device<>")
    while connected:
        try:
            data = conn.recv(2048)
            if not data:
                conn.close()
                devices_status.pop(id)
                connected = False
            else:
                device = Device()
                device.ParseFromString(data)
                devices_status[id] = device
                print(f"<{device.id}-{device.nome}>: new update")

        except Exception as e:
            print(e)
            connected = False
            devices_status.pop(id)
    conn.close()


def start_server():
    thread = threading.Thread(
        target=handle_connections
    )
    thread.start()
    server.listen()
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
            thread = threading.Thread(
                target=handle_client, args=(conn, start_input)
            )
            thread.start()
        else:
            continue


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
