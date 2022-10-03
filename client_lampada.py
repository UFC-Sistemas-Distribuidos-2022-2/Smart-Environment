import time
import socket

PORT = 1510
HOST = "localhost"
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


ligada = False


while True:
    msg = conn.recv(2048).decode("utf-8")
    if msg == "execute":
        ligada = not ligada
    conn.send(str(ligada)).encode("utf-8")
    time.sleep(10)
