#temperatura_quarto
import time
import socket
from sensores_pb2 import Sensor
import random


PORT = 1510
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
ruido = random.random()
fator = random.randrange(-1, 2, 1)
final = ruido*fator
sensor = Sensor()
sensor.nome='lampada'
sensor.status_lampada = 0
print(sensor.nome)
print(sensor.status_lampada)
s.sendall(sensor.SerializeToString())
#print('mensagem enviada')
#time.sleep(15)
    
s.close()