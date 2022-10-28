from flask import Flask, render_template, request, redirect
from typing import List
import socket
from proto.grpc.sensores_pb2 import Sensor, Input, Sensor_List, Device, Device_List
from constants import PORT, HOST


app = Flask(__name__)



def get_sensores() -> List[Sensor]:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    start_input = Input(tipo="client", tipo_request="get", tipo_desejado="sensors")
    conn.sendall(start_input.SerializeToString())
    data = conn.recv(2048)
    sensores_list = Sensor_List()
    sensores_list.ParseFromString(data)
    return sensores_list


def get_devices() -> List[Device]:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    start_input = Input(tipo="client", tipo_request="get", tipo_desejado="devices")
    conn.sendall(start_input.SerializeToString())
    data = conn.recv(2048)
    devices_list = Device_List()
    devices_list.ParseFromString(data)
    print(devices_list)
    return devices_list


def update_device(input: Input) -> None:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    conn.sendall(input.SerializeToString())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sensores/")
def sensores():
    sensores = get_sensores()
    print(len(sensores.sensores))

    return render_template("sensors.html", sensores=sensores.sensores)


@app.route("/devices/")
def devices():
    devices = get_devices()
    return render_template("devices.html", devices=devices.devices)


@app.route("/devices/<tipo>/<id>")
def lampada(tipo, id):
    return render_template("update.html", tipo=tipo, id=id)


@app.route("/update/<tipo>/<id>", methods=['GET', 'POST'])
def update(tipo, id):
    input = Input()
    if tipo in ["ar_condicionado","tv"] and request.form.get('device_value') is not '':
        input.temperatura = float(request.form.get('device_value'))
    print(request.form.get('ligado'))
    input.ligado = bool(int(request.form.get('ligado')))
    print(input.ligado)
    input.dest_id = str(int(id))
    input.tipo = "client"
    input.tipo_request = 'post'
    update_device(input)
    return redirect('/devices')


if __name__ == "__main__":
    app.run(port=8012, debug=True)
