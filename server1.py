import socket
import pickle
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
global x
x = ""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            data_arr = pickle.loads(data)
            if not data:
                break
            x = list(data_arr)
            print("raw data:", type(data_arr), data_arr)
            print (x[2:-1])

            conn.sendall(data)
