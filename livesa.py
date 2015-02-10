#!/usr/bin/python
# -*- coding: utf8 -*-

'''
Esqueleto para aplicacion LIVESA.


Acerca los comentarios:

    En python los comentarios multilinea se ponen entre tripes comillas simples.
    Los comentarios de una sola linea inician con el caracter #
    
Notas:
    Toda la tabulacion esta hecha con el caracter de espacio, cada 4 espacios son 
    un tabulador, tomar en cuenta que el editor use espacios en lugar de TABs
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class CustomButton(Button):
    '''
    Boton con fondo personalizado ... 
    '''
    
    def __init__(self, **kwargs):
        '''
        Sobreescribimos la funcion init del widget Button
        '''
        
        #llamamos a la funcion contructor del objeto button
        super(CustomButton, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(source='background.jpg', size=Window.size)

class Livesa(FloatLayout):
    '''
    Clase que representa el formulario principal de la aplicacion
    '''
    
    def __init__(self, **kwargs):
        '''
        Funcion constructor o de inicializacion de este widget
        '''
        
        #llamar a la funcion constructor de la clase madre, FloatLayout en este caso
        #esto es necesario debido a que la clase madre tambien necesita realizar algunas operaciones de inicializacion
        super(Livesa, self).__init__(**kwargs)
        
        #definimos la funcion que se ejcutara cuando cambie de tamaño la ventana
        self.bind(size=self.draw_background)
        
        #se agrega un widget personalizado (definido en la linea 25)
        self.mybutton = CustomButton(text='Hola mundo')
        
        #agregamos el boton a la lista de hijos de este widget, solo cuando es agregado con add_widget es dibujado en pantalla
        self.add_widget(self.mybutton)
        
    def draw_background(self, w, val):
        '''
        Comentario: Esta funcion se ejecutara cada vez que el tamaño del
        formulario Livesa cambie (en este caso, la ventana)
        '''
        #Todo widget contiene un objeto canvas el cual se encarga de 
        #todas las operaciones de dibujo de cada widget.
        
        #cambiamos las intrucciones de dibujo 'antes de' las intrucciones
        #normales para dibujar el widget, basicamente en la siguiente sentencia
        #se cambia el color de fondo (y no afecta las intrucciones normales de dibujo del widget)
        with self.canvas.before:
            Color(1, 1, 1, 1) #color en formato RGBA, blanco en este caso ... los valores deben ser entre zero y 1
            
            #dibujamos un rectangulo con el color actual (seleccionado en la instruccion anterior)
            self.rect = Rectangle(size=Window.size)
            
            #tambien en lugar de pintar un fondo liso, puede usarse una imagen ... (descomentar la siguiente linea para ver el resultado)
            #self.rect = Rectangle(source='background.jpg', size=Window.size)
            

#la siguiente condicion sirve para usar este archivo como aplicacion o como modulo, 
#cuando es aplicacion (ejecucion tipo python livesa.py), la variable __name__ contiene la cadena "__main__"
if __name__ == "__main__":
    
    #importamos la funcion que sirve como punto de entrada de aplicacion
    from kivy.base import runTouchApp
    
    #ejecutamos como aplicacion y le pasamos el widget de la clase Livesa (definida en la linea 16)
    runTouchApp(Livesa() )
