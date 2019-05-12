import socket
import threading
import pickle
import time
from threading import Thread

global nivel, posx_1, posx_2, posy_1, posy_2, datos
posx_1 = 603
posy_1 = 550
posx_2 = 690
posy_2 = 550
datos = []

ip = "localhost"

puerto = 9797
dataConection = (ip,puerto)
conexionesMaximas = 3



#Clase con el hilo para atender a los clientes.
#En el constructor recibe el socket con el cliente y los datos del
#cliente para escribir por pantalla
class Cliente(Thread):
    def __init__(self,conn, direccion):
        # LLamada al constructor padre, para que se inicialice de forma
        # correcta la clase Thread.
        Thread.__init__(self)
        # Guardamos los parametros recibidos.
        self.socket = conn
        self.datos = direccion
 
    # Bucle para atender al cliente.       
    def run(self):
      # Bucle indefinido hasta que el cliente envie "adios"
      seguir = True
      while seguir:
         # Espera por datos
         peticion = self.socket.recv(1024)
         peticion_ = pickle.loads(peticion)
         # Contestacion
         x = peticion_
         posx_1 = x[0]
         posy_1 = x[2]
         posx_2 = x[1]
         posy_2 = x[3]
                
         datos = [posx_1, posx_2, posy_1, posy_2]
         datos_pickle = pickle.dumps(datos)
         self.socket.send(datos_pickle)



def main():
    socket_servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    socket_servidor.bind (dataConection)
    socket_servidor.listen(conexionesMaximas)

    # bucle para atender clientes
    while 1:
        # Se espera a un cliente
        print ("Esperando conexion en %s:%s" % (ip, puerto))
        conn, direccion = socket_servidor.accept()
        # Se escribe su informacion
        print ("Conexion establecida con %s:%s" %(direccion[0], direccion[1])) 
        # Se crea la clase con el hilo
        hilo = Cliente(conn, direccion)
        # y se arranca el hilo
        hilo.start()

if __name__ == "__main__":
    main()
