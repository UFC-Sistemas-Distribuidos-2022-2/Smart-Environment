import socket
import threading
from sensores_pb2 import Sensor, Input, Device , Sensor_List , Device_List
from constants import PORT, HOST
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(HOST), int(PORT)))
sensores_list = []
sensores_conn = {}
sensores_status = {}
devices_status = {}


def handle_client(conn: socket.socket, msg: str, tipo=None):
    if msg == "get":
        if tipo =="sensors":
            print("conectei um cliente")
            sensores_list = Sensor_List()
            sensores_list.sensores.extend([sensores_status[key] for key in sensores_status])
            conn.sendall(sensores_list.SerializeToString())
        elif tipo =="devices":
            print("conectei um cliente")
            devices_list = Device_List()
            devices_list.devices.extend([devices_status[key] for key in devices_status])
            conn.sendall(devices_list.SerializeToString())
    elif msg == "execute":
        sensores_conn["id"].send("execute")
        msg = conn.recv(2048).decode("utf-8")
    conn.close()


def handle_sensor(conn: socket.socket, id: str):
    connected = True
    nome = ""
    if sensores_status.get(id):
        connected = False
        print("ID já registrado, altere as configurações do seu aparelho")
    else:
        sensores_status[id] = Sensor()
        print("conectei um sensor")
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
            del sensores_conn[id]
            sensores_status.pop(id)
    conn.close()


def handle_device(conn: socket.socket, id: str):
    connected = True
    nome = ""
    if devices_status.get(id):
        print("ID já registrado, altere as configurações do seu aparelho")
    else:
        devices_status[id] = Device()
        print("conectei um dispositivo")
    while connected:
        try:
            data = conn.recv(2048)
            if not data:
                conn.close()
                devices_status.pop(id)
                print(f"Dispositivo desconectado - {nome}")
                connected = False
            else:
                device = Device()
                device.ParseFromString(data)
                devices_status[id] = device
                nome = devices_status[id].nome
                print(f"<{device.id}-{device.nome}>:{device.temperatura}")

        except Exception as e:
            print(e)
            connected = False
            devices_status.pop(id)
    conn.close()


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {PORT}")
    while True:
      
        conn, _ = server.accept()  # wait for a new connection for the server
        data = conn.recv(2048)
        start_input = Input()
        start_input.ParseFromString(data)
        print(start_input.tipo)
 
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
            # handle_device(conn, start_input.dest_id)
        elif start_input.tipo == "client":
            thread = threading.Thread(
                target=handle_client, args=(conn, start_input.tipo_request, start_input.tipo_desejado)
            )
            thread.start()
        else:
            continue
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_server()
