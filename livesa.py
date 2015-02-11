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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox

from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import time

class CustomButton(Button):
    '''
    Boton con fondo personalizado ... 
    '''
    
    def __init__(self, **kwargs):
        '''
        Sobreescribimos la funcion __init__ de la clase Button
        '''
        
        #llamamos a la funcion contructor del objeto button y le indicamos por default la imagen que usara de fondo
        super(CustomButton, self).__init__(background_normal='styles/backgrounds/blueroundsquare.png',
                                           background_down='styles/backgrounds/blueroundsquarepressed.png',
                                           #size_hint_y=None,   #esto es necesario para poder cambiar el tama;o del widget, de lo contrario siempre toma el tama;o de su padre (1,1)
                                           #size=(300,80),   #
                                           #height=80,
                                           #pos=(100,100),
                                           **kwargs)
             
class DateButton(Button):
    
    def __init__(self, **kwargs):
        
        #llamamos a la funcion contructor del objeto button y le indicamos por default la imagen que usara de fondo
        super(DateButton, self).__init__(background_normal='styles/backgrounds/datebackground.png',
                                           background_down='styles/backgrounds/datebackground.png',
                                           markup=True,
                                           **kwargs)
              

class DatePicker(BoxLayout):
    
    months = ('01',
                '02',
                '03',
                '04',
                '05',
                '06',
                '07',
                '08',
                '09',
                '10',
                '11',
                '12'
                )
    
    def __init__(self, **kwargs):
        
        super(DatePicker, self).__init__(size_hint=(None,None),
                                            size=(250,40),
                                            **kwargs)
    
        
        self.add_widget(Label(text='[color=000000]'+kwargs.get('label')+'[/color]', markup=True))
    
        self.btn_day = DateButton(text='[color=000000]'+time.strftime("%d")+'[/color]', on_release=self.show_days)
        self.add_widget(self.btn_day)
        
        self.add_widget(Label(text='[color=000000]/[/color]', size_hint_x=None, width=10, markup=True))
        
        self.btn_month = DateButton(text='[color=000000]'+time.strftime("%m")+'[/color]', on_release=self.show_months )
        self.add_widget(self.btn_month)
        
        self.add_widget(Label(text='[color=000000]/[/color]', size_hint_x=None, width=10, markup=True))
        
        self.btn_year = DateButton(text='[color=000000]'+time.strftime("%Y")+'[/color]', on_release=self.show_years )
        self.add_widget(self.btn_year)
        
        #day options
        self.drop_day = DropDown()
        for i in range(1,32):
            day = Button(text=str(i), size_hint_y=None, height=30 )
            day.bind(on_press=self.set_day)
            self.drop_day.add_widget( day )
        
        #month options
        self.drop_month = DropDown()
        for i in range(1,13):
            month = Button(text=str(i), size_hint_y=None, height=30 )
            month.bind(on_press=self.set_month)
            self.drop_month.add_widget(month )
        
        #year options
        self.drop_year = DropDown()
        for i in range(2014,2002,-1):
            year = Button(text=str(i), size_hint_y=None, height=30 )
            year.bind(on_press=self.set_year)
            self.drop_year.add_widget(year)
        
    def show_days(self, w):
        self.drop_day.open(w)
        
    def show_months(self, w):
        self.drop_month.open(w)
        
    def show_years(self, w):
        self.drop_year.open(w)
        
    def set_day(self, w):
        self.btn_day.text = '[color=000000]'+w.text+'[/color]'
        self.drop_day.dismiss()
        
    def set_month(self, w):
        self.btn_month.text = '[color=000000]'+w.text+'[/color]'
        self.drop_month.dismiss()
        
    def set_year(self, w):
        self.btn_year.text = '[color=000000]'+w.text+'[/color]'
        self.drop_year.dismiss()
        
    def get_date(self):
        return "%s.%s.%s" % (self.btn_day.text, self.btn_month.text, self.btn_year.text)
              
class Fieldset(BoxLayout):
    def __init__(self, **kwargs):
        super(Fieldset, self).__init__(**kwargs)
        
        #definimos la funcion que se ejcutara cuando cambie de tamaño la ventana
        self.bind(size=self.draw_background)
        
    def draw_background(self, w, val):
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(source='styles/backgrounds/fieldsetbackground.png', size=self.size, pos=self.pos)
              
class TabButton(Button):
    '''
    Boton con fondo personalizado ... 
    '''
    
    def __init__(self, **kwargs):
        '''
        Sobreescribimos la funcion __init__ de la clase Button
        '''
        
        #llamamos a la funcion contructor del objeto button y le indicamos por default la imagen que usara de fondo
        super(TabButton, self).__init__(background_normal='styles/backgrounds/bluesquare.png',
                                           #background_down='styles/backgrounds/bluesquarepressed.png',
                                           **kwargs)
                                           
class SuperiorMenu(AnchorLayout):
    def __init__(self, **kwargs):
        super(SuperiorMenu, self).__init__(anchor_x='center', 
                                            anchor_y='top', 
                                            **kwargs)
        
        self.box = BoxLayout(size_hint_y=None, height=50, spacing=2)
        
        self.box.add_widget(TabButton(text='Productos', on_press=self.on_productos) )
        self.box.add_widget(TabButton(text='Cliente', on_press=self.on_clientes) )
        self.box.add_widget(TabButton(text='Ruta', on_press=self.on_rutas) )
        self.box.add_widget(TabButton(text='Vendedor', on_press=self.on_vendedor) )

        self.add_widget(self.box)

    def on_productos(self, w):
        print 'Go products'
        
    def on_clientes(self, w):
        print 'Go clientes'
        
    def on_rutas(self, w):
        print 'Go rutas'
        
    def on_vendedor(self, w):
        print 'Go vendedor'
        
class CheckItem(BoxLayout):
    def __init__(self, **kwargs):
        super(CheckItem, self).__init__(**kwargs)
        
        self.checkbox = CheckBox(size_hint_x=None, width=50)
        self.add_widget(self.checkbox)
        
        self.label = Label(text=kwargs.get('label'), markup=True, size_hint_x=None, width=200)
        self.add_widget(self.label)
        

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
        
        self.layout = BoxLayout(orientation='vertical')
        
        #definimos la funcion que se ejcutara cuando cambie de tamaño la ventana
        self.bind(size=self.draw_background)

        self.layout.add_widget(SuperiorMenu() )
        
        #CATEGORIAS
        self.fieldset_categorias = Fieldset(padding=20)
        self.fieldset_categorias.add_widget(CustomButton(text='Productos'))
        self.fieldset_categorias.add_widget(CustomButton(text='Marcas'))
        self.fieldset_categorias.add_widget(CustomButton(text='Capacidades'))
        self.fieldset_categorias.add_widget(CustomButton(text='Tipos'))
        self.layout.add_widget(self.fieldset_categorias)
        
        #FECHAS
        self.fieldset_fechas = Fieldset(padding=20, orientation='vertical')
        self.box_fechas = BoxLayout()
        
        self.box_fechas.add_widget(DatePicker(label='Desde: ') )
        self.box_fechas.add_widget(DatePicker(label='Hasta: ') )
        
        
        self.fieldset_fechas.add_widget(self.box_fechas)
        
        self.fieldset_fechas.add_widget(CheckItem(label='[color=000000]Hacer comparacion de fechas[/color]'))
        
        
        self.layout.add_widget(self.fieldset_fechas)
        
        #LUGAR-CLIENTE
        self.fieldset_lugarcliente = BoxLayout(padding=20)
        self.fieldset_lugarcliente.add_widget(CustomButton(text='Lugar / Zona'))
        self.fieldset_lugarcliente.add_widget(CustomButton(text='Clientes'))
        
        self.layout.add_widget(self.fieldset_lugarcliente)
        
        self.add_widget(self.layout)
        
        #BOTON DE CONSULTA
        
        #RESULTADO
        
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
