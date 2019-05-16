import pygame, sys
import socket
#from network import Network
import pickle
import tkinter
from random import randint

global Num_x, Num_y, contador
Num_x = 0
Num_y = 0
contador = 0


ancho = 1366
alto = 768

pygame.init()

class Network():

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
        """
        :param data: str
        :return: str
        """
        try:
            datos = data
            datos_1 = pickle.dumps(datos) 
            self.client.send(datos_1)
            reply = self.client.recv(2048)
            reply_1 = pickle.loads(reply) 
            return reply_1
        except socket.error as e:
            return str(e)

class mina(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.imagen_mina = pygame.image.load ("mina.png")
                self.imagen_mina = pygame.transform.scale(self.imagen_mina,(40,40))
                self.rect = self.imagen_mina.get_rect()
                global Num_x, Num_y, contador
                self.rect.top = Num_x
                self.rect.left = Num_y
                self.aparicion_mina = 5
                self.lista_mina = []
                self.Num_x = 0
            
    
                
                
        # Define los tiempos para llamar las funciones de rango
        def comportamiento(self, tiempo):
                #self.Rango()
                self.Rango_x()

        # Origina numeros al azar para el eje x para que las estrellas aparescan en distintios lugares
        def Rango_x(self):
                global Num_x, Num_y
                Num_x = (randint(0,1200))
                Num_y = (randint(0,700))
                
        

        #Define el tiempo de aparicion de cada una de las estrellas

        #def Rango(self):
                

        
                
        #Agrega las estrellas creadas en una lista        
        def aparicion(self,x,y):
                global contador
                Aparicion = mina()
                self.lista_mina.append(Aparicion)
                contador += 1
                 
               
        # Se dibuja en la ventana las estrellas
        def Dibujar (self, superficie):
                superficie.blit (self.imagen_mina, self.rect)


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("pyDakarDeath")
        
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(200,200)
        self.MINAS = mina()

    def run(self):
        global contador
        clock = pygame.time.Clock()
        run = True
        while run:
            self.screen.fill((255,255,255))
            clock.tick(60)
            self.tiempo = pygame.time.get_ticks()/1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= 1320 - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= 723 - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.player.draw(self.screen)
            self.player2.draw(self.screen)
            self.MINAS.comportamiento(self.tiempo)

            if (randint(0,100) == self.MINAS.aparicion_mina):
                        x = self.MINAS.rect.left
                        y = self.MINAS.rect.top
                        self.MINAS.aparicion(x,y)
                        for x in self.MINAS.lista_mina:
                                     print("Hola")
                                     x.Dibujar(self.screen)
                                    
           # if len(self.MINAS.lista_mina) > 0:
                                 
                                                          
            pygame.display.update()
                       

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0





   # def draw_text(self, text, size, x, y):
    #    pygame.font.init()
     #   font = pygame.font.SysFont("pyDakarDeath", size)

      #  self.screen.draw(render, (x,y))



if __name__ == "__main__":
    g = Game(ancho,alto)
    g.run()
