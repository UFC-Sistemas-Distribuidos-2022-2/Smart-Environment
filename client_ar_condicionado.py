import time
import socket

PORT = 1510
HOST = "localhost"
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))


temp = 0


while True:
    msg = conn.recv(2048).decode("utf-8")
    if msg == "execute":
        temp = 18
    
    conn.send(str(temp)).encode("utf-8")
    time.sleep(10)
