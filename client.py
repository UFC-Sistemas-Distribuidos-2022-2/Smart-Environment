from re import S
from flask import Flask, url_for
from flask import render_template
from flask import request
from typing import List
import socket
import pdb
from sensores_pb2 import Sensor, Input, Sensor_List , Device, Device_List
import time
from constants import PORT, HOST

app = Flask(__name__)


sensor = Sensor()
sensor.tipo = "geladeira"
sensor.id = "1"
sensor.temperatura = 30
sensor.temperatura_freezer = -20
sensor2 = Sensor()
sensor2.tipo = "termico"
sensor2.temperatura = 32
sensor2.id = "14"
sensor3 = Sensor()
sensor3.tipo = "presenca"
sensor3.presenca = True
sensor3.id = "14"

device = Device()
device.tipo = 'lampada'
device.id = "1"
device.ligado = True
device.nome = 'lampada'
device2 = Device()
device2.tipo = 'lampada'
device2.id = "2"
device2.ligado = False
device2.nome = 'lampada 2'
#   required string tipo = 1;
#   required string id = 2;
#   optional float temperatura = 3;
#   optional float temperatura_freezer = 4;
#   optional bool ligado = 5;
#   optional string nome = 6;


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

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sensores/")
def comments():
    comments = [sensor, sensor2, sensor3]
    return render_template("sensors.html", sensores=comments)


@app.route("/sensores1/")
def comments1():
    sensores = get_sensores()
    print(len(sensores.sensores))

    return render_template("sensors.html", sensores=sensores.sensores)

@app.route("/devices/")
def devices():
    devices = get_devices()
    #print(len(devices.devices))

    return render_template("devices.html", devices=devices.devices)

@app.route("/create", methods=["POST"])
def create():
    ligada = request.form.get("lampada-ligada")
    # tmp = request.form.get('ar')
    print(ligada)
    # print(tmp)
    server_lampada(ligada)
    teste = Sensor()
    teste.nome = "lampada"
    teste.status_lampada = int(ligada)
    PORT = 1510
    HOST = "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(teste.SerializeToString())
    # server_ar(tmp)
    return render_template("index.html")


def server_lampada(ligada):
    teste = Sensor()
    teste.nome = "lampada"
    teste.status_lampada = int(ligada)
    PORT = 1510
    HOST = "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(teste.SerializeToString())


if __name__ == "__main__":
    app.run(port=8011, debug=True)
