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
from kivy.uix.togglebutton import ToggleButton

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

class DropDownList(DropDown):
    def __init__(self, **kwargs):
        super(DropDownList, self).__init__(**kwargs)
        
        self.container.padding = 5
        
        with self.canvas.before:
            Color(1, 1, 1, .8)  # colors range from 0-1 instead of 0-255
            self.rect = Rectangle(source='styles/backgrounds/droplistopened.png', size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
        
        #for mouse over event
        Window.bind(mouse_pos=self.check_over)
        
        self.opacity = .9
        
    def check_over(self, instance, value):
        if self.collide_point(value[0], value[1]):
            self.opacity = 1
        else:
            self.opacity = .9

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def on_select(self, data):
        print data

class DropButton(Button):
    
    def __init__(self, **kwargs):
        
        #llamamos a la funcion contructor del objeto button y le indicamos por default la imagen que usara de fondo
        super(DropButton, self).__init__(background_normal='styles/backgrounds/droplist.png',
                                           background_down='styles/backgrounds/droplistdown.png',
                                            markup=True,
                                            font_size=24,
                                            on_release=self.do_drop,
                                           **kwargs)
                                           
        self.drop = DropDownList()
                                           
        self.values = kwargs.get('values', None)
        self.item_cls = kwargs.get('item_cls', Button)
        self.item_textcolor = kwargs.get('item_textcolor', 'FFFFFF')
        #self.item_kwargs = kwargs.get('item_kwargs', {})
        
        if self.values != None:
            
            #llenar todos los elementos
            for i in sorted(self.values):
                self.prod = self.item_cls(size_hint_y=None, 
                                            height=50, 
                                            label='[color=%s]'%self.item_textcolor + i + '[/color]'
                                            )
                self.drop.add_widget(self.prod)
                
                
        #for mouse over event
        Window.bind(mouse_pos=self.check_over)
        
        self.opacity = .7
        
    def check_over(self, instance, value):
        if self.collide_point(value[0], value[1]):
            self.opacity = 1
        else:
            self.opacity = .7
                
    
    def do_drop(self, w):
        self.drop.open(self)

class DateButton(Button):
    
    def __init__(self, **kwargs):
        
        #llamamos a la funcion contructor del objeto button y le indicamos por default la imagen que usara de fondo
        super(DateButton, self).__init__(background_normal='styles/backgrounds/datebackground.png',
                                           background_down='styles/backgrounds/datebackground.png',
                                           markup=True,
                                           **kwargs)
              

class DatePicker(BoxLayout):
    
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
        
        #definimos la funcion que se ejcutara cuando cambie de tamaño el widget
        self.bind(size=self.draw_background)
        
    def draw_background(self, w, val):
        self.canvas.before.clear()
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
                                           size_hint_y=None,
                                           height=40,
                                            **kwargs)
        
        self.box = BoxLayout(spacing=2,
                             size_hint_x=None,
                             #height=50,
                             width=600
                             )
        
        self.box.add_widget(TabButton(text='Productos', on_press=self.on_productos, size_hint_x=None, width=150) )
        self.box.add_widget(TabButton(text='Cliente', on_press=self.on_clientes, size_hint_x=None, width=150) )
        self.box.add_widget(TabButton(text='Ruta', on_press=self.on_rutas, size_hint_x=None, width=150) )
        self.box.add_widget(TabButton(text='Vendedor', on_press=self.on_vendedor, size_hint_x=None, width=150) )

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
        
        self.checkbox = CheckBox(size_hint_x=None, width=50, 
                                    background_checkbox_normal='styles/backgrounds/checkbox.png',
                                    background_checkbox_down='styles/backgrounds/checkbox_active.png'
                                    )
        self.add_widget(self.checkbox)
        
        self.label = Label(text=kwargs.get('label'), markup=True, size_hint_x=None, width=200, text_size=(190,None))
        self.add_widget(self.label)
        
class ProductFilter(Fieldset):
    def __init__(self, **kwargs):
        super(ProductFilter, self).__init__(padding=20, spacing=20, size_hint_y=None, height=80, **kwargs)
        
        self.productos = DropButton(text='[color=000000]Productos[/color]', 
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    values= {'AGUARDIENTE':'AC',
                                    'ALCOHOL':'AL',
                                    'ANIS':'AN',
                                    'DESTILADO':'BA',
                                    'HABANERO':'HB',
                                    'JEREZ':'JZ',
                                    'LICOR':'LC',
                                    'MEZCAL':'MZ',
                                    'PARRAS':'PA',
                                    'RON':'RN',
                                    'SANGRITA':'SG',
                                    'SIDRA AMBAR':'SB',
                                    'SIDRA ROSADA':'SR',
                                    'TEQUILA':'TQ',
                                    'VERMOUTH':'VT',
                                    'VINO DE CONSAGRAR':'VG',
                                    'VODKA':'VK',
                                    'ESTUCHE MINIATURA MEXICANO':'E1',
                                    'ESTUCHE MINIATURA MTY':'E2',
                                    'ESTUCHE MINIATURA REGIONAL':'E3',
                                    'CHAROLA MINIATURA MEXICANO':'E4'
                                    })
                                    
        self.marcas = DropButton(text='[color=000000]Marcas[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    values = {'38':'TR',
                                    'AJITA':'AJ',
                                    'AMECA Y ANAMARINA':'AM',
                                    'BARANTRO':'BT',
                                    'BOLA DE ORO':'BL',
                                    'CAFKA':'CF',
                                    'CAÑONAZO':'CA',
                                    'CHOPERENA':'CN',
                                    'DEL CORAZON':'CZ',
                                    'DIVINO':'DV',
                                    'DOS CORONAS':'DC',
                                    'EL CHORRITO':'CH',
                                    'EL JINETE':'JT',
                                    'EL TIGRE':'TG',
                                    'FAROLAZO':'FR',
                                    'FURKEN':'FU',
                                    'GRAN PEÑUELA':'GP',
                                    'HIJOS DE VILLA':'HV',
                                    'LA LUPE':'LL',
                                    'LAJITA':'LJ',
                                    'MARINA':'MR',
                                    'MATACAÑA':'MT',
                                    'MOCAMBO':'MM',
                                    'OTELO':'TL',
                                    'PETROVA':'PT',
                                    'PETROVA KINGEBRA':'PK',
                                    'PLUMA ROJA':'PR',
                                    'TORINO':'TR',
                                    'VILLA RICA':'HV',
                                    'VILLALOBOS':'VL',
                                    'VILLALOBOS PLATINUM':'VP',
                                    'VINO DE CONSAGRAR':'GC',
                                    'MEXICANO':'MX',
                                    'MONTERREY':'MT',
                                    'SURTIDO REGIONAL':'RG'
                                    })
                                    
        self.capacidades = DropButton(text='[color=000000]Capacidades[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    values = {'0.050':'00',
                                    '0.200':'20',
                                    '0.200':'21',
                                    '0.250':'25',
                                    '0.355':'35',
                                    '0.440':'44',
                                    '0.500':'50',
                                    '0.690':'69',
                                    '0.700':'70',
                                    '0.750':'75',
                                    '0.950':'95',
                                    '1.000':'01',
                                    '1.500':'15',
                                    '1.690':'16',
                                    '1.750':'17',
                                    '3.970':'39',
                                    '5.000':'50',
                                    '20.000':'02',
                                    '200.000':'GR'
                                    })
                                    
        self.tipos = DropButton(text='[color=000000]Tipos[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                values = {'BLANCO Y C/PERA':'11',
                                    'BLANCO Y CAFE ESPECIAL':'12',
                                    'BLANCO LUJO Y LICOR C/GUSANO':'13',
                                    'ESPECIAL MONTERREY':'14',
                                    'AÑEJO ESPECIAL':'15',
                                    '34% Alc. Vol.':'19',
                                    'ORO':'21',
                                    'ORO LUJO':'22',
                                    'ORO EXTRA':'23',
                                    'REPOSADO':'31',
                                    'REPOSADO ANIVERSARIO':'32',
                                    'REPOSADO LUJO':'36',
                                    'AÑEJO':'41',
                                    'AÑEJO LUJO':'43',
                                    'SOLERA':'51',
                                    'STANDARD':'61',
                                    'STANDARD LUJO':'63',
                                    'DESTILADO DE AGAVE':'64',
                                    '10 AÑOS BUCANERO':'70',
                                    'CIRUELA Y 15 AÑOS':'71',
                                    'DURAZNO Y 20 AÑOS':'72',
                                    'MANZANA Y 20 AÑOS ARTE':'73',
                                    'MEMBRILLO':'74',
                                    'NANCHE DULCE':'75',
                                    'NARANJA':'76',
                                    'PIÑA':'77',
                                    'ZARZAMORA':'78',
                                    'LIMON':'79',
                                    'MANZANA DULCE':'81',
                                    'NANCHE':'82',
                                    'TEJOCOTE':'83',
                                    'HIERBA DEL BURRO':'84',
                                    'HIERBA MAESTRA':'85',
                                    'HERBAL Y PLATANO':'86',
                                    'MELON':'87',
                                    'MENTA BLANCA':'88',
                                    'BLUE CURACAO':'89',
                                    'CAFE':'91',
                                    'CAFE MINI REDONDA':'92',
                                    'ESTUCHES MINI Y SIN TIPO':'99'
                                    })
        
        self.add_widget(self.productos)
        self.add_widget(self.marcas)
        self.add_widget(self.capacidades)
        self.add_widget(self.tipos)

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
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        #definimos la funcion que se ejcutara cuando cambie de tamaño la ventana
        self.bind(size=self.draw_background)

        self.layout.add_widget(SuperiorMenu() )
        
        #CATEGORIAS
        self.fieldset_categorias = ProductFilter()
        self.layout.add_widget(self.fieldset_categorias)
        
        #FECHAS
        self.fieldset_fechas = Fieldset(padding=15, orientation='vertical', size_hint_y=None, height=100)
        self.box_fechas = BoxLayout()
        
        self.box_fechas.add_widget(DatePicker(label='Desde: ') )
        self.box_fechas.add_widget(DatePicker(label='Hasta: ') )
        
        
        self.fieldset_fechas.add_widget(self.box_fechas)
        
        self.fieldset_fechas.add_widget(CheckItem(label='[color=000000]Hacer comparacion de fechas[/color]'))
        
        
        self.layout.add_widget(self.fieldset_fechas)
        
        #LUGAR-CLIENTE
        self.fieldset_lugarcliente = BoxLayout(padding=20, spacing=20, size_hint_y=None, height=80)
        self.fieldset_lugarcliente.add_widget(DropButton(text='[color=000000]Lugar / Zona[/color]'))
        self.fieldset_lugarcliente.add_widget(DropButton(text='[color=000000]Clientes[/color]'))
        
        self.layout.add_widget(self.fieldset_lugarcliente)
        
        
        #BOTON DE CONSULTA
        self.layout.add_widget(CustomButton(text='Consulta', size_hint=(None,None), size=(300,50)))
        
        #RESULTADO
        self.fieldset_result = Fieldset(padding=20)
        self.layout.add_widget(self.fieldset_result)
        
        
        self.add_widget(self.layout)
        
    def draw_background(self, w, val):
        '''
        Comentario: Esta funcion se ejecutara cada vez que el tamaño del
        formulario Livesa cambie (en este caso, la ventana)
        '''
        #Todo widget contiene un objeto canvas el cual se encarga de 
        #todas las operaciones de dibujo de cada widget.
        
        
        self.canvas.before.clear()
        
        #cambiamos las intrucciones de dibujo 'antes de' las intrucciones
        #normales para dibujar el widget, basicamente en la siguiente sentencia
        #se cambia el color de fondo (y no afecta las intrucciones normales de dibujo del widget)
        with self.canvas.before:
            Color(.95, .95, .95, 1) #color en formato RGBA, blanco en este caso ... los valores deben ser entre zero y 1
            
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
