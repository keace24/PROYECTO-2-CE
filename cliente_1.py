#######################################
#Tecnologico de Costa Rica            #
#                                     #
#Estudiantes:                         #
#                                     #
#Armando Fallas Garro  2019226675     #
#Kevin Calderón Esquivel  20191517479 #
#                                     #
#Taller de programacion               #
#                                     #
#Profesor: Antonio González Torres    #
#                                     #
#######################################

import socket
import tkinter
from tkinter import *
from tkinter import messagebox
import pygame,sys
from pygame import *
from random import randint
import winsound
import json
import threading
import pickle
import time

ipServidor = "localhost"
puertoServidor = 9797

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ipServidor, puertoServidor))
print("Conectado con el servidor ---> %s:%s" %(ipServidor, puertoServidor))



Ventana = tkinter.Tk()
pygame.init()
Ventana.title("pyDakarDeath")
Ventana.wm_state('zoomed')
Ventana.config(bg='white')
img = PhotoImage(file='Fondo.png')
Logo = Label(Ventana, image=img)
Logo.pack()



ancho = 1366
alto = 768



#Esta funcion creara una ventana nueva cuando el jugador presione el boton de jugar y indicara en que nivel se encuentra el jugador
        

def Iniciar_nivel():
        global nivel
        pygame.font.init()
        nivel_txt =str(nivel)
        Level = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("pyDakarDeath")
        Texto_nivel = pygame.font.Font (None, 80)
        Texto = Texto_nivel.render("Nivel: " + str(nivel), 0,(230,126,41))
        Texto_Name = pygame.font.Font (None, 80)
        Texto_N = Texto_Name.render("Jugador: ", 0,(230,126,41))
        Texto_indicacion = pygame.font.Font (None, 45)
        Texto_in = Texto_indicacion.render("Presione [s] para empezar... ", 0,(230,126,41))

        #Se le asigna un ciclo whie para que la ventana se cierre y comience el juego al presionar la tecla S


        while True:
                for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_s:
                                        pygame.display.quit()
                                        Jugar()
                                        pygame.quit()


                # Se dibuja los diferentes texto en la pantalla, indicandole sus coordenadas                  

                Level.blit(Texto_N,(850,200))
                Level.blit(Texto,(100,200))
                Level.blit(Texto_in,(200,650))
                pygame.display.update()

class Jugador_1(pygame.sprite.Sprite):
        def __init__(self, x, y):
                pygame.sprite.Sprite.__init__(self)
                self.carro_1 = pygame.image.load("Carro1.png")   
                self.carro_1 = pygame.transform.scale(self.carro_1,(70,70))
                self.rect = self.carro_1.get_rect()
                self.rect.centerx = x
                self.rect.centery = y
                self.velocidad_nave = 6
                self.negro = (0,0,0)
                
                self.lista_disparo = []

        #Llama la funcion proyectil para dibujar y darle la trayectoria al disparo del jugador       

        #Se crea una superficie para dibujar los enemigos
      
        def Dibujar (self, superficie):
                superficie.blit (self.carro_1, self.rect)
        
class Jugador_2(pygame.sprite.Sprite):
        def __init__(self,x, y):
                pygame.sprite.Sprite.__init__(self)
                self.carro_1 = pygame.image.load("Carro1.png")   
                self.carro_1 = pygame.transform.scale(self.carro_1,(70,70))
                self.rect = self.carro_1.get_rect()
                self.rect.centerx = x
                self.rect.centery = y
                self.velocidad_nave = 6
                self.negro = (0,0,0)
                
                self.lista_disparo = []
                
                
        #Llama la funcion proyectil para dibujar y darle la trayectoria al disparo del jugador       

        #Se crea una superficie para dibujar los enemigos
      
        def Dibujar (self, superficie):
                superficie.blit (self.carro_1, self.rect)



def Jugar():
        pygame.init()
        global posx_1, posx_2, posy_1, posy_2, Jugador1, Jugador2, datos
        #Se minimixa la ventana principal
        Ventana.withdraw()
        #Se definen el tamaño de la pantalladel juego
        juego = pygame.display.set_mode((ancho, alto),pygame.FULLSCREEN)
        pygame.display.set_caption ("pyDakarDeath")

        #Se crea una variable reloj 
        reloj = pygame.time.Clock()

        #se define una cancion de fondo para el juego
        
        #pygame.mixer.music.load("Cancion. verificar peso.mpeg")
        #pygame.mixer.music.play(3)

        #Se le asignan unas variables a funciones y a clases para ser llamadas cuando se necesiten
        
        jugando = True
        
        
        
        # El while es donde se estara ejecutando cada una de las instrucciones de las clases para que el juego corra
        while True:
                tiempo = pygame.time.get_ticks()/1000

                datos = [posx_1, posx_2, posy_1, posy_2]
                mensaje1 = pickle.dumps(datos)
                s.sendall(mensaje1)
                
                data = s.recv(1024)
                data_serv = pickle.loads(data)
                x = list(data_serv)
                posx_2 = x[1]
                posy_2 = x[3]
                Jugador2.rect.centerx = posx_2
                Jugador2.rect.centery = posy_2 
                
               # Texto_puntaje = pygame.font.Font (None, 50)
               # Texto_Pantalla = Texto_puntaje.render("Puntaje: " + str(marcador), 0,(255,255,255))
                
                #Se define el color de fondo, tiempo, posicion de la imagen de nave
                juego.fill(Jugador1.negro)

                # Se le asigna una variable al evento cuando se dejapresionada una tecla
                keys = pygame.key.get_pressed()

               # juego.blit(Jugador.Nave,(Jugador.posx,Jugador.posy))
                reloj.tick(60)
                
                # Se define los eventos para los movimientos derecha, izquierda, arriba, abajo, y disparo de la nave
                # y las coordenadas limites para que no se salga de la ventana

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        if jugando == True:
                                if event.type == pygame.KEYDOWN:
                                        """
                                        if event.key == pygame.K_SPACE:
                                                #Se crean variables x,y para tomar la posicio actual de la nave, para asignarselo a la trayectoria del disparo
                                                x = Jugador1.rect.centerx
                                                y = Jugador2.rect.centery
                                                Jugador.Disparar(x,y)
                                                # Se define un sonido al disparo de la nave
                                                #Disparo_son = pygame.mixer.Sound("disparo de nave.wav")
                                                Disparo_son.play()
                                                
                                                """
                # Se definen los eventos al presionar las teclas
                                        
                if keys[K_LEFT]:
                                
                                
                        if Jugador1.rect.left > -1:
                                
                                Jugador1.rect.left -= Jugador1.velocidad_nave
                                posx_1 = Jugador1.rect.centerx
                                print(posx_1)
                                
                elif keys[K_RIGHT]:
                                
                                
                        if Jugador1.rect.right < 1350:
                                Jugador1.rect.right += Jugador1.velocidad_nave
                                posx_1 = Jugador1.rect.centerx
                                print(posx_1)
                                
                elif keys[K_UP]:
                        pass
                elif keys[K_DOWN]:
                        pass
                Jugador1.Dibujar(juego)
                Jugador2.Dibujar(juego)
                pygame.display.update()
        
def Cerrar():
    if messagebox.askokcancel("Salir","¿Desea salir?"):
        print ("Ha cerrado la ventana")
        Ventana.destroy()
def Salir():
    if messagebox.askyesno("Salir","¿Desea salir?"):
        Ventana.destroy()

Ventana.protocol("WM_DELETE_WINDOW",Cerrar)        

B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="red",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="red",command=Iniciar_nivel, cursor='pirate')
B_Jugar.place(x=642,y=500)

global nivel, posx_1, posx_2, posy_1, posy_2, Jugador, Jugador2, datos
nivel = 1
posx_1 = 603
posy_1 = 550
posx_2 = 690
posy_2 = 550
Jugador1 = Jugador_1(posx_1, posy_1)
Jugador2 = Jugador_2(posx_2, posy_2)
datos = []

Ventana.mainloop()


