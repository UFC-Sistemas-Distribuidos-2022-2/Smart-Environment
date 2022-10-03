import socket
import threading
from typing import Tuple

# from constants import *
# from utils_msgs import *

host = "localhost"
port = 1510

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((str(host), int(port)))

# clients = []
# clients_dict = dict()


# def distribute_msg(conn: socket.socket, msg: str):
#     for client in clients_dict:
#         if clients_dict[client] != conn:
#             try:
#                 send_msg(clients_dict[client], msg)
#             except socket.error as e:
#                 print("Error sending data: %s" % e)

def handle_client(conn: socket.socket, addr: Tuple , msg):

    # clients_dict[conn] = 
    if msg == 'get':
        conn.send("lista de sensores").encode("utf-8")
        
    while connected:
        try:
            msg = conn.recv(2048).decode("utf-8")
            print(msg)
        except Exception as e:
            print(e)
            connected = False
    # del clients_dict[username]
    conn.close()
    
def handle_sensor(conn: socket.socket, addr: Tuple):

    # clients_dict[conn] = 
    connected = True

    while connected:
        try:
            msg = conn.recv(2048).decode("utf-8")
            print(msg)
        except Exception as e:
            print(e)
            connected = False
    # del clients_dict[username]
    conn.close()
    
    
def handle_device(conn: socket.socket, addr: Tuple):

    # clients_dict[conn] = 
    connected = True

    while connected:
        try:
            msg = conn.recv(2048).decode("utf-8")
            print(msg)
        except Exception as e:
            print(e)
            connected = False
    # del clients_dict[username]
    conn.close()


def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on 1510")
    
    while True:
        conn, addr = server.accept()  # wait for a new connection for the server
        msg = conn.recv(2048).decode("utf-8")
        if msg == 'sensor':
            thread = threading.Thread(target=handle_sensor, args=(conn, addr))
            thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


if __name__ == "__main__":
    print("[STARTING] Client is starting...")
    start_server()
