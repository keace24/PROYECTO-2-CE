import socket
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

mensaje = [1,2,3]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))
while True:
    mensaje1 = pickle.dumps(mensaje)
    s.sendall(mensaje1)
    data = s.recv(1024)
    data_arr = pickle.loads(data)
    print('Received', repr(type(data_arr[0])))
