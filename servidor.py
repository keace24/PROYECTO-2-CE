import socket
from _thread import *
import pickle
import time

global nivel, posx_1, posx_2, posy_1, posy_2
posx_1 = 603
posy_1 = 550
posx_2 = 690
posy_2 = 550


ip = "localhost"

puerto = 9797
dataConection = (ip,puerto)
conexionesMaximas = 3

socket_servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

socket_servidor.bind (dataConection)
socket_servidor.listen(conexionesMaximas)


print ("Esperando conexion en %s:%s" % (ip, puerto))
conn, direccion = socket_servidor.accept()
print ("Conexion establecida con %s:%s" %(direccion[0], direccion[1]))    


with conn:

    while True:
        
        
        
        
        
        data = conn.recv(1024)
        data_arr = pickle.loads(data)
        if not data:
            break
        x = list(data_arr)
        posx_1 = x[0]
        posy_1 = x[2]
        posx_2 = x[1]
        posy_2 = x[3]
                
        

        conn.sendall(data)
            
            
