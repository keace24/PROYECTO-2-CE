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

import tkinter
from tkinter import *
from tkinter import messagebox
import pygame,sys
from pygame import *
from random import randint
import winsound
import csv
import json
import threading

Ventana = tkinter.Tk()
pygame.init()
Ventana.title("pyDakarDeath")
Ventana.wm_state('zoomed')
Ventana.config(bg='black')


#global
#nivel = 1
#Marcador = 0
#Name = ''

class Nombre_Jugador():
        def __init__(self):
        
                global Name, marcador
                marcador = 0
                pygame.font.init()
                self.Canvas_Jugador = Canvas (Ventana, bg = "black", width = 250, height = 300)
                self.Canvas_Jugador.pack()

                self.dato=tkinter.StringVar()
                self.Nombre = Entry(self.Canvas_Jugador, bd = 5, justify = LEFT, textvariable=self.dato)
                self.Nombre.place(x=120,y=20)
                
                self.Label_Jugador = Label (self.Canvas_Jugador,text = "Jugador:",fg = "white",bg = "black")
                self.Label_Jugador.place (x=20,y=20)
                
                self.B_Guardar = tkinter.Button(self.Canvas_Jugador, text="Guardar",fg="white",width=9,height=2,bg="GREEN",command=self.Lista_J, cursor='hand2')
                self.B_Guardar.place(x=120,y=50)
                self.B_Jugar2 = tkinter.Button(self.Canvas_Jugador, text="Jugar",fg="white",width=9,height=2,bg="GREEN",command=Iniciar_nivel, cursor='hand2')
                self.B_Jugar2.place(x=120,y=100)

        def Lista_J(self):
                global Name
                archivo = open ("Jugadores.csv","a")
                Name = self.dato.get()
                archivo.write(Name)
                archivo.write("\n")
                print (Name)
                archivo.close

def Cerrar():
    if messagebox.askokcancel("Salir","¿Desea salir?"):
        print ("Ha cerrado la ventana")
        Ventana.destroy()
def Salir():
    if messagebox.askyesno("Salir","¿Desea salir?"):
        Ventana.destroy()

Ventana.protocol("WM_DELETE_WINDOW",Cerrar)        

B_Salir = tkinter.Button(Ventana, text="Salir",fg="white",width=10,height=3,bg="GREEN",command=Salir, cursor='pirate')
B_Salir.place(x=642,y=600)
B_Jugar = tkinter.Button(Ventana, text="Jugar",fg="white",width=10,height=3,bg="GREEN",command=Nombre_Jugador, cursor='hand2')
B_Jugar.place(x=642,y=540)

Ventana.mainloop()
