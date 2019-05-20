import pygame, sys
import socket
#from network import Network
import pickle
import tkinter
from random import randint
import threading
import time

global Num_x, Num_y, contador, mina, dibujar_mina, Imagen_Disparo_Jugador, minutos
Num_x = 0
Num_y = 0
contador = 0
mina = []
dibujar_mina = 0
Imagen_Disparo_Jugador = "proyectil_v2.png"
minutos = 0
segundos = 0

ancho = 1366
alto = 768

pygame.init()


class Network():
    global mina, dibujar_mina
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555            
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        recibir = self.client.recv(2048)
        recibir_1 = pickle.loads(recibir)
        return recibir_1
    def send(self, data):
        datos = data
        datos_1 = pickle.dumps(datos) 
        self.client.send(datos_1)
        reply = self.client.recv(2048)
        reply_1 = pickle.loads(reply)
        #print(type(reply_1))
        
        if isinstance(reply_1, list):
            if self.id != self.id:
                return reply_1
                
                
        elif isinstance(reply_1, str):
            return reply_1
        

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
                Num_x = (randint(0,1200))
                Num_y = (randint(0,700))
                
        
                
        #Agrega las minas creadas en una lista        
        def aparicion(self,x,y):
                Aparicion = mina()
                self.lista_mina.append(Aparicion)
        
                 
               
        # Se dibuja en la ventana las minas
        def Dibujar (self, superficie):
                superficie.blit (self.imagen_mina, self.rect)

class Proyectil(pygame.sprite.Sprite):
        def __init__(self,posx,posy, imagen, personaje):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_proyectil = pygame.image.load (imagen)
                #self.imagen_proyectil = pygame.transform.scale(self.imagen_proyectil,(50,45))
                self.rect = self.imagen_proyectil.get_rect()
                self.v_disparo = 13
                self.rect.top = posy
                self.rect.left = posx
                self.disparo_personaje = personaje

                
                
        # Define el movimiento de los proyectiles
        
        def Trayecto(self):
                if self.disparo_personaje == False:
                        self.rect.top = self.rect.top + self.v_disparo
                else:
                        self.rect.top = self.rect.top - self.v_disparo
                 
                        
        #Se crea una superficie para dibujar los proyectiles

        def Dibujar (self, superficie):
                superficie.blit (self.imagen_proyectil, self.rect)
                
class Player(pygame.sprite.Sprite):
    width = height = 50

    def __init__(self, startx, starty):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_Jugador = pygame.image.load ("carro1.png")
        self.imagen_Jugador = pygame.transform.scale(self.imagen_Jugador,(45,45))
        self.rect = self.imagen_Jugador.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.velocity = 2
        self.lista_disparo = []
    def Disparar (self,x,y):
        
                global Imagen_Disparo_Jugador
                disparo = Proyectil(x,y, Imagen_Disparo_Jugador,True)
                self.lista_disparo.append(disparo)
    
    def Dibujar(self, superficie):
        superficie.blit (self.imagen_Jugador, self.rect)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.rect.x += self.velocity
        elif dirn == 1:
            self.rect.x -= self.velocity
        elif dirn == 2:
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity




class Game:
    global Num_x, Num_y, contador, dibujar_mina, minutos, segundos
    def __init__(self, w, h):
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
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("pyDakarDeath")
        self.fondo = pygame.image.load("mapa.png").convert()
        self.fondo = pygame.transform.scale(self.fondo,(ancho,alto))
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(590, 700)
        self.player2 = Player(690,700)
        self.MINAS = mina()
        hilo = threading.Thread(target = Crono, args = ())
        hilo.start()

    
    
    
    def run(self):
        global contador, minutos, segundos
        clock = pygame.time.Clock()
        run = True
        while run:
            
            self.screen.fill((255,255,255))
            clock.tick(60)
            self.tiempo = pygame.time.get_ticks()/1000
            #self.crono = pygame.time.get_ticks()/1000

            Texto_puntaje = pygame.font.Font (None, 50)
            Texto_Pantalla = Texto_puntaje.render("Tiempo " + str(minutos) + " : " + str(int(segundos)), 0,(255,255,255))
        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                            
                                            print("Hola")
                                            #Se crean variables x,y para tomar la posicio actual de la nave, para asignarselo a la trayectoria del disparo
                                            x = self.player.rect.x + 15
                                            y = self.player.rect.y
                                            self.player.Disparar(x,y)
                                            # Se define un sonido al disparo de la nave
                                            #Disparo_son = pygame.mixer.Sound("disparo de nave.wav")
                                            #Disparo_son.play()
                    

            keys = pygame.key.get_pressed()
            
            

            if keys[pygame.K_RIGHT]:
                if self.player.rect.x <= 1320 - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.rect.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.rect.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.rect.y <= 723 - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            self.player2.rect.x, self.player2.rect.y = self.parse_data(self.send_data())

            # Update Canvas
            self.screen.blit(self.fondo, (0, 0))
            self.player.Dibujar(self.screen)
            self.player2.Dibujar(self.screen)
            self.MINAS.comportamiento(self.tiempo)

            dibujar_mina = (randint(0,400))
            
            if dibujar_mina == self.MINAS.aparicion_mina:
                        x = self.MINAS.rect.left
                        y = self.MINAS.rect.top
                        self.MINAS.aparicion(x,y)
                        """
                        values=[self.net.id, "Mina", Num_x, Num_y, dibujar_mina]
                        reply2 = self.net.send(values)
                        return reply2
                           """
            if len(self.player.lista_disparo) > 0:
                    for x in self.player.lista_disparo:
                        x.Dibujar(self.screen)
                        x.Trayecto()
                        if x.rect.top < -20:
                                self.player.lista_disparo.remove(x)

                                
           # if len(self.MINAS.lista_mina) > 0:
            if len(self.MINAS.lista_mina) > 0:
                for x in self.MINAS.lista_mina:
                                     x.Dibujar(self.screen)
                                     
            self.screen.blit(Texto_Pantalla,(20,20))                                                            
                                                          
            pygame.display.update()
            pygame.display.flip()           

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.rect.x) + "," + str(self.player.rect.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0





if __name__ == "__main__":
    g = Game(ancho,alto)
    g.run()
