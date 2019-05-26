# Se importan las librerias necesarias para ejecutar el juego
import pygame, sys
import socket
import pickle
import tkinter
from random import randint
import threading
import time
from tkinter import *
from tkinter import messagebox

#Se crean las variables globales las cuales en su mayoria seran enviadas al servidor para que llegue al otro cliente

global Num_x, Num_y, contador, mina_indicacion, dibujar_mina,Imagen_Disparo_Jugador, pausado_J2
global minutos, reply_1, tiempo_pausa, segundos, Jugador1, Jugador2, vida_player, vida_player2, disparo_2, puntos_J1, puntos_J2, imagenC, imagenC2, direccion, pausado
Num_x = 0
Num_y = 0
contador = 0
mina_indicacion = 0
dibujar_mina = 0
Imagen_Disparo_Jugador = "proyectil_v2.png"
minutos = 0
segundos = 0
reply_1 = ""
tiempo_pausa = 0
vida_player = 100
vida_player2 = 100
disparo_2 = 0
puntos_J1 = 0
puntos_J2 = 0
imagenC = "carro1.png"
imagenC2 = "carro1.png"
direccion = 0
pausado = False
pausado_J2 = False

#Dimensiones de la ventana de juego

ancho = 1366
alto = 768

#Se inicializa la libreria de pygame

pygame.init()

#Se crea la ventana de tkinter, la pantalla de inicio se le asigna el nombre del juego y se carga el fondo

Ventana = tkinter.Tk()
pygame.init()
Ventana.title ("Pydakardeath") 
Ventana.wm_state('zoomed') 
Ventana.config(bg='white')
img = PhotoImage(file='Fondo.png')
Logo = Label(Ventana, image=img)
Logo.pack()

#Funcion para cerrar la ventana de inicio

def Cerrar():
        if messagebox.askokcancel("Salir", "¿Desea salir del juego?"):
            print ("Ha cerrado la ventana") 
            Ventana.destroy() 
def Salir():
        if messagebox.askyesno("Salir", "¿Desea salir del juego?"):
            Ventana.destroy()

#Se crea la clase que entablara la conexion con el servidor y que enviara y recibira todos los datos            

class Network():
    global reply_1
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Se ingresa la ip donde se ejecuta el servidor
        self.host = "localhost" 
        #"192.168.0.103"                            
        # Se asigna el puerto donde entraran y saldran los datos              
        self.port = 5555            
        self.addr = (self.host, self.port)
        self.id = self.connect()

        # La funcion connect es la que identifica cada cliente en el server
    def connect(self):
        self.client.connect(self.addr)
        recibir = self.client.recv(2048)
        recibir_1 = pickle.loads(recibir)
        
        return recibir_1

        # Esta funcion envia los datos al servidor
    def send(self, data):
        datos = data
        #Con la funcion pickle se codifican los datos a enviar
        datos_1 = pickle.dumps(datos) 
        self.client.send(datos_1)
        reply = self.client.recv(2048)
        #Con pickle se decodifican los datos recibidos
        reply_1 = pickle.loads(reply)        
        if isinstance(reply_1, str):
            return reply_1
        
# Se crea el sprite de las minas que se dibujaran en el juego
class mina(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_mina = pygame.image.load ("mina.png")
                self.imagen_mina = pygame.transform.scale(self.imagen_mina,(40,40))
                self.rect = self.imagen_mina.get_rect()
                global Num_x, Num_y, contador, dibujar_mina
                self.rect.top = Num_x
                self.rect.left = Num_y
                self.aparicion_mina = 5
                self.lista_mina = []
                self.Num_x = 0
            
    
                
                
        # Define los tiempos para llamar las funciones de rango
        def comportamiento(self, tiempo):
                #self.Rango()
                self.Rango_x()

        # Origina numeros al azar para el eje x, y para que las minas aparescan en distintios lugares
        def Rango_x(self):
                global Num_x, Num_y
                Num_x = (randint(0,600))
                Num_y = (randint(0,1100))
                
        
                
        #Agrega las minas creadas en una lista        
        def aparicion(self,x,y):
                Aparicion = mina()
                self.lista_mina.append(Aparicion)
        
                 
               
        # Se dibuja en la ventana las minas
        def Dibujar (self, superficie):
                superficie.blit (self.imagen_mina, self.rect)

class Proyectil(pygame.sprite.Sprite):
        def __init__(self,posx,posy, imagen):
                global direccion
                pygame.sprite.Sprite.__init__(self)
                self.imagen_proyectil = pygame.image.load (imagen)
                #self.imagen_proyectil = pygame.transform.scale(self.imagen_proyectil,(50,45))
                self.rect = self.imagen_proyectil.get_rect()
                self.v_disparo = 6
                self.rect.top = posy
                self.rect.left = posx
                

                
                
        # Define el movimiento de los proyectiles
        
        def Trayecto(self):
                if direccion == 0:
                        self.rect.top = self.rect.top - self.v_disparo
        
                elif direccion == 1:
                        self.rect.top = self.rect.top + self.v_disparo
                        
                elif direccion == 3:
                        self.rect.left = self.rect.left + self.v_disparo

                elif direccion == 4:
                        self.rect.left = self.rect.left - self.v_disparo
                        
                 
                        
        #Se crea una superficie para dibujar los proyectiles

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_proyectil, self.rect)

#Se crea la clase donde se maneja las ubicaciones e imagenes de los jugadores
                
class Player(pygame.sprite.Sprite):
    width = height = 50

    def __init__(self, startx, starty, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_Jugador = pygame.image.load (imagen)
        self.imagen_Jugador = pygame.transform.scale(self.imagen_Jugador,(45,45))
        self.rect = self.imagen_Jugador.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.velocity = 8
        self.lista_disparo = []

# La funcion disparar agregara un disparo a la lista disparo para que se dibuje en pantalla
        
    def Disparar (self,x,y):
        
                global Imagen_Disparo_Jugador
                disparo = Proyectil(x,y, Imagen_Disparo_Jugador)
                self.lista_disparo.append(disparo)
    
    def Dibujar(self, superficie):
        superficie.blit (self.imagen_Jugador, self.rect)

    


# La clase principal del juego

class Game:
    ancho = 1366
    alto = 768
    #se llaman todas las las variables globales necesarias
    global Num_x, Num_y, contador, dibujar_mina, minutos, segundos, imagenC, imagenC2
    global tiempo_pausa, segundos, Jugador2
    def __init__(self, w, h):
            # Se crea una funcion de cronometro donde se aumentara la variable segundos y la variable minutos
        def Crono():
            global minutos, segundos
            if segundos == 59:
                segundos = 0
                minutos += 1
                return Crono()
            else:
                segundos += 1
                time.sleep(1)
                return Crono()
        # Este hilo llamara continuamente a la funcion cronometro para que se ejecute
        hilo = threading.Thread(target = Crono, args = ())
        #Se inicia el hilo
        hilo.start()
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("pyDakarDeath")
        self.fondo = pygame.image.load("mapa.png").convert()
        self.fondo = pygame.transform.scale(self.fondo,(ancho,alto))
        self.net = Network()
        self.width = w
        self.height = h
        #Se asignar dos variables que serán los jugadores
        self.player = Player(590, 700, imagenC)
        self.player2 = Player(690,700, imagenC2)
        self.MINAS = mina()
         
                                
                                       
        
# Esta funcion correra infinitamente al juego             
    
    def run(self):
        global contador, minutos, segundos, Jugador1, Jugador2, vida_player, vida_player2, disparo_2, mina_indicacion, Num_x, Num_y, puntos_J1, puntos_J2, imagenC, imagenC2, direccion, Imagen_Disparo_Jugador, pausado
        global pausado_J2
        clock = pygame.time.Clock()
        run = True
        
        # establece el tamaño de la ventana
        cyan = (0, 255, 255, 100)

        # se crea una superficie para dibujar los puntos de cada jugador
        pygame.display.set_caption(u'Superficies transparentes')

        cyan_surface = pygame.Surface((175, 175)).convert_alpha()

        cyan_surface.fill(cyan)
        
        while run:
            # crea la superficie de color cyan de dimensiones width=240, height=240
            
            # establece el título de la ventana
            self.player
            
            self.screen.fill((255,255,255))
            
            
            clock.tick(60)
            self.tiempo = pygame.time.get_ticks()/1000

            # Aqui se dibuja el tiempo y las variables segundos y minutos en pantalla
            
            Texto_Tiempo = pygame.font.Font (None, 50)
            Texto_Pantalla = Texto_Tiempo.render("Tiempo " + str(minutos) + " : " + str(int(segundos)), 0,(255,255,255))

            # Se dibuja en pantalla los puntos de los jugadores

            Puntajes_J1 = pygame.font.Font (None, 30)
            Texto_J1 = Puntajes_J1.render('Jugador 1: ' + str(int(puntos_J1)) , 0,(255,255,255))

            Puntajes_J2 = pygame.font.Font (None, 30)
            Texto_J2 = Puntajes_J2.render('Jugador 2: ' + str(int(puntos_J2)) , 0,(255,255,255))

            # Se dibuja el titulo puntos

            Titulo_puntaje = pygame.font.Font (None, 30)
            Titulo = Titulo_puntaje.render(str('PUNTOS'), 0,(255,255,255))

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Este evento capta si el cliente presiona una tecla

                if event.type == pygame.KEYDOWN:

                                                # si el cliente presiona espacio se creara un disparo
                                        if event.key == pygame.K_SPACE:
                                            #Se crean variables x,y para tomar la posicio actual de la nave, para asignarselo a la trayectoria del disparo
                                            x = self.player.rect.x + 15
                                            y = self.player.rect.y
                                            self.player.Disparar(x,y)
                                            disparo_2 = 1
                                            #Se define un sonido al disparo de la nave
                                            #Disparo_son = pygame.mixer.Sound("disparo de nave.wav")
                                            #Disparo_son.play()

                                        # Si presiona p pausará el juego
                                        if event.key == pygame.K_p:
                                                pausado = True
                                                
                                        """
                                                Menu = tkinter.Tk()
                                                Menu.geometry("300x300+0+0")
                                                Menu.title ("Menú")  
                                                Menu.config(bg='white')
                                                Menu.wm_attributes("-topmost", 1)
                                                Menu.pack()
                                                
                                                """
                                        
            # Este evento capta si el cliente deja presionado una tecla    
                
            keys = pygame.key.get_pressed()

            # El if de pausa se ejecutara si pausado es igual a True y de despausara hasta que el cliente presione e
            
            if pausado == True or pausado_J2 == True:
        
                pygame.font.init()
                Texto_Pausa = pygame.font.Font (None, 45)
                Texto_Pausa = Texto_Pausa.render("Juego Pausado ", 0,(255,255,255))
                tiempo_pausa = segundos
                while pausado:
                        for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                                        if event.key == pygame.K_e:
                                                                pausado = False
                                                                segundos = tiempo_pausa
                        self.screen.blit(Texto_Pausa,(550,500))

                 # Se ejecutan los movimientos del jugador en pantalla        
                        
            if keys[pygame.K_RIGHT]:
                if self.player.rect.x <= 1320 - self.player.velocity:
                    self.player.rect.x += self.player.velocity

                    # Esta variable indica hacia que direccion se iran los proyectiles
                    direccion = 3
                    #Cambia la imagen del disparo
                    Imagen_Disparo_Jugador = "proyectil_v3.png"
                    # Cambiara la imagen del jugador hacia donde este yendo
                    imagenC = "carro2.png"
                    self.player = Player(self.player.rect.x, self.player.rect.y, imagenC)

                # Se actualiza la imagen del jugador en el otro cliente
            self.player2 = Player(self.player2.rect.x, self.player2.rect.y, imagenC2)

            if keys[pygame.K_LEFT]:
                if self.player.rect.x >= self.player.velocity:
                    self.player.rect.x -= self.player.velocity
                    direccion = 4
                    Imagen_Disparo_Jugador = "proyectil_v3.png"
                    imagenC = "carro3.png"
                    self.player = Player(self.player.rect.x, self.player.rect.y, imagenC)
           

            if keys[pygame.K_UP]:
                if self.player.rect.y >= self.player.velocity:
                    self.player.rect.y -= self.player.velocity
                    direccion = 0
                    Imagen_Disparo_Jugador = "proyectil_v2.png"
                    imagenC = "carro1.png"
                    self.player = Player(self.player.rect.x, self.player.rect.y, imagenC)
         

            if keys[pygame.K_DOWN]:
                if self.player.rect.y <= 723 - self.player.velocity:
                    self.player.rect.y += self.player.velocity
                    direccion = 1
                    Imagen_Disparo_Jugador = "proyectil_v2.png"
                    imagenC = "carro4.png"
                    self.player = Player(self.player.rect.x, self.player.rect.y, imagenC)

            # Send Network Stuff
            #Aqui se le asignan las variables al jugador 2 del otro cliente para que sean enviadas al servidor
            self.player2.rect.x, self.player2.rect.y, segundos, minutos, disparo_2, mina_indicacion, Num_x, Num_y, puntos_J2, imagenC2, pausado_J2 = self.parse_data(self.send_data())

            # Update Canvas
            self.screen.blit(self.fondo, (0, 0))
            self.player.Dibujar(self.screen)
            self.player2.Dibujar(self.screen)
            self.MINAS.comportamiento(self.tiempo)

# Esta variable hara que esten sacando numeros al azar
            dibujar_mina = (randint(0,1000))

            # Si dibujar mina es igual a aparicion ejecutara la clase de mina para que se dibuje en ambos clientes
            
            if dibujar_mina == self.MINAS.aparicion_mina:
                        x = self.MINAS.rect.left
                        y = self.MINAS.rect.top
                        self.MINAS.aparicion(x,y)
                        mina_indicacion = 1
        # Si el tamaño de la lista disparo es mayor a 0 está dibujara continuamente los disparos
                
            if len(self.player.lista_disparo) > 0:
                    for x in self.player.lista_disparo:
                        x.Dibujar(self.screen)
                        x.Trayecto()
                        if x.rect.top < -20:
                                self.player.lista_disparo.remove(x)
                        # Capta si el disparo coliciona con el otro jugados, y si coliciona se sumaran 4 puntos al jugador
                        else:
                                if x.rect.colliderect(self.player2.rect):
                                                vida_player -= 5
                                                puntos_J1 += 4
                                                self.player.lista_disparo.remove(x)
            
                            



            if disparo_2 == 1:
                x = self.player2.rect.x + 15
                y = self.player2.rect.y
                self.player2.Disparar(x,y)
                disparo_2 = 0

            if mina_indicacion == 1:
                x = self.MINAS.rect.left
                y = self.MINAS.rect.top
                self.MINAS.aparicion(x,y)
        
                


            if len(self.player.lista_disparo) > 0:
                    for x in self.player2.lista_disparo:
                        x.Dibujar(self.screen)
                        x.Trayecto()
                        if x.rect.top < -20:
                                self.player2.lista_disparo.remove(x)
                
                    
                                
           # if len(self.MINAS.lista_mina) > 0:
            if len(self.MINAS.lista_mina) > 0:
                for x in self.MINAS.lista_mina:
                                     x.Dibujar(self.screen)
                
            
            # dibuja la superficie de color cyan en la posición x=140, y=140
            self.screen.blit(cyan_surface, (1195, 0))
            self.screen.blit(Texto_J1,(1220,40))
            self.screen.blit(Texto_J2,(1220,95))
            cyan_surface.blit(Titulo,(45,0))  
            self.screen.blit(Texto_Pantalla,(20,20))
            pygame.display.update()
            pygame.display.flip()           

        pygame.quit()
    def send_data(self):

        data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y) + "," + str(segundos) + "," + str(minutos) + "," + str(disparo_2) + "," + str(mina_indicacion) + "," + str(Num_x) + "," + str(Num_y) + "," + str(puntos_J1) + "," + str(imagenC) + "," + str(pausado)
        reply = self.net.send(data)
        #print (data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]), int(d[6]), int(d[7]), int(d[8]), str(d[9]), bool(d[10])
        except:
            return 0,0

def iniciar():

    if __name__ == "__main__":
            g = Game(ancho,alto)
            g.run()

B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=iniciar, cursor='hand2')
B_Jugar.place(x=642,y=540)



Ventana.mainloop()
