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

#INCONSISTENCIAS
'''
    SUGAR CANE ... Su tipo no esta en el catalogo
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior

from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import time, firebirdsql

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
        self.item_kwargs = kwargs.get('item_kwargs', {})
        
        if self.values != None:
            
            #llenar todos los elementos
            for i in sorted(self.values):
                self.prod = self.item_cls(size_hint_y=None, 
                                            height=50, 
                                            label='[color=%s]'%self.item_textcolor + i + '[/color]',
                                            text='[color=%s]'%self.item_textcolor + i + '[/color]',
                                            **self.item_kwargs
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
            self.rect = Rectangle(source='styles/backgrounds/fieldsetbackgroundbig.png', size=self.size, pos=self.pos)
              
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
        
class LabelButton(ButtonBehavior, Label):
    pass
        
class CheckItem(BoxLayout):
    def __init__(self, **kwargs):
        super(CheckItem, self).__init__(**kwargs)
        
        self.on_active = kwargs.get('on_active', None)
        
        self.checkbox = CheckBox(size_hint_x=None, width=50, 
                                    background_checkbox_normal='styles/backgrounds/checkbox.png',
                                    background_checkbox_down='styles/backgrounds/checkbox_active.png'
                                    )
        self.add_widget(self.checkbox)
        
        self.label = LabelButton(text=kwargs.get('label'), markup=True, size_hint_x=None, width=200, text_size=(190,None), on_press=self.docheck)
        self.add_widget(self.label)
        
        if self.on_active != None:             
            self.checkbox.bind(active=self.on_active)
        
        
    def docheck(self, w):
        if self.checkbox.active:
            self.checkbox.active = False
        else:
            self.checkbox.active = True
        
class ProductFilter(Fieldset):
    def __init__(self, **kwargs):
        super(ProductFilter, self).__init__(padding=20, spacing=20, size_hint_y=None, height=80, **kwargs)
        
        self.productos = DropButton(text='[color=000000]Productos[/color]', 
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    item_kwargs={'on_active':self.selected_product},
                                    values= {'AGUARDIENTE':{'key':'AC', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'ALCOHOL':{'key':'AL', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'ANIS':{'key':'AN', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'DESTILADO':{'key':'BA', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'HABANERO':{'key':'HB', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'JEREZ':{'key':'JZ', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'LICOR':{'key':'LC', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MEZCAL':{'key':'MZ', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'PARRAS':{'key':'PA', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'RON':{'key':'RN', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'SANGRITA':{'key':'SG', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'SIDRA AMBAR':{'key':'SB', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'SIDRA ROSADA':{'key':'SR', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'TEQUILA':{'key':'TQ', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VERMOUTH':{'key':'VT', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VINO DE CONSAGRAR':{'key':'VG', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VODKA':{'key':'VK', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'ESTUCHE MINIATURA MEXICANO':{'key':'E1', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'ESTUCHE MINIATURA MTY':{'key':'E2', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'ESTUCHE MINIATURA REGIONAL':{'key':'E3', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'CHAROLA MINIATURA MEXICANO':{'key':'E4', 'marcas':[], 'capacidades':[], 'tipos':[], 'refcount':0}
                                    })
                                    
        self.marcas = DropButton(text='[color=000000]Marcas[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    values = {'38':{'key':'TR', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'AJITA':{'key':'AJ', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'AMECA Y ANAMARINA':{'key':'AM', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'BARANTRO':{'key':'BT', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'BOLA DE ORO':{'key':'BL', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'CAFKA':{'key':'CF', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'CAÑONAZO':{'key':'CA', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'CHOPERENA':{'key':'CN', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'DEL CORAZON':{'key':'CZ', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'DIVINO':{'key':'DV', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'DOS CORONAS':{'key':'DC', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'EL CHORRITO':{'key':'CH', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'EL JINETE':{'key':'JT', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'EL TIGRE':{'key':'TG', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'FAROLAZO':{'key':'FR', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'FURKEN':{'key':'FU', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'GRAN PEÑUELA':{'key':'GP', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'HIJOS DE VILLA':{'key':'HV', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'LA LUPE':{'key':'LL', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'LAJITA':{'key':'LJ', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MARINA':{'key':'MR', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MATACAÑA':{'key':'MT', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MOCAMBO':{'key':'MM', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'OTELO':{'key':'TL', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'PETROVA':{'key':'PT', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'PETROVA KINGEBRA':{'key':'PK', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'PLUMA ROJA':{'key':'PR', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'TORINO':{'key':'TR', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VILLA RICA':{'key':'HV', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VILLALOBOS':{'key':'VL', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VILLALOBOS PLATINUM':{'key':'VP', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'VINO DE CONSAGRAR':{'key':'GC', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MEXICANO':{'key':'MX', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'MONTERREY':{'key':'MT', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0},
                                    'SURTIDO REGIONAL':{'key':'RG', 'productos':[], 'capacidades':[], 'tipos':[], 'refcount':0}
                                    })
                                    
        self.capacidades = DropButton(text='[color=000000]Capacidades[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                    values = {'0.050':{'key':'00', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.200':{'key':'20', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.200':{'key':'21', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.250':{'key':'25', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.355':{'key':'35', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.440':{'key':'44', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.500':{'key':'50', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.690':{'key':'69', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.700':{'key':'70', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.750':{'key':'75', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '0.950':{'key':'95', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '1.000':{'key':'01', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '1.500':{'key':'15', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '1.690':{'key':'16', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '1.750':{'key':'17', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '3.970':{'key':'39', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '5.000':{'key':'50', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '20.000':{'key':'02', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0},
                                    '200.000':{'key':'GR', 'productos':[], 'marcas':[], 'tipos':[], 'refcount':0}
                                    })
                                    
        self.tipos = DropButton(text='[color=000000]Tipos[/color]',
                                    item_cls=CheckItem,
                                    item_textcolor='000000',
                                values = {'BLANCO Y C/PERA':{'key':'11', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'BLANCO Y CAFE ESPECIAL':{'key':'12', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'BLANCO LUJO Y LICOR C/GUSANO':{'key':'13', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ESPECIAL MONTERREY':{'key':'14', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'AÑEJO ESPECIAL':{'key':'15', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    '34% Alc. Vol.':{'key':'19', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ORO':{'key':'21', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ORO LUJO':{'key':'22', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ORO EXTRA':{'key':'23', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'REPOSADO':{'key':'31', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'REPOSADO ANIVERSARIO':{'key':'32', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'REPOSADO LUJO':{'key':'36', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'AÑEJO':{'key':'41', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'AÑEJO LUJO':{'key':'43', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'SOLERA':{'key':'51', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'STANDARD':{'key':'61', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'STANDARD LUJO':{'key':'63', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'DESTILADO DE AGAVE':{'key':'64', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    '10 AÑOS BUCANERO':{'key':'70', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'CIRUELA Y 15 AÑOS':{'key':'71', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'DURAZNO Y 20 AÑOS':{'key':'72', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'MANZANA Y 20 AÑOS ARTE':{'key':'73', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'MEMBRILLO':{'key':'74', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'NANCHE DULCE':{'key':'75', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'NARANJA':{'key':'76', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'PIÑA':{'key':'77', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ZARZAMORA':{'key':'78', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'LIMON':{'key':'79', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'MANZANA DULCE':{'key':'81', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'NANCHE':{'key':'82', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'TEJOCOTE':{'key':'83', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'HIERBA DEL BURRO':{'key':'84', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'HIERBA MAESTRA':{'key':'85', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'HERBAL Y PLATANO':{'key':'86', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'MELON':{'key':'87', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'MENTA BLANCA':{'key':'88', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'BLUE CURACAO':{'key':'89', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'CAFE':{'key':'91', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'CAFE MINI REDONDA':{'key':'92', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0},
                                    'ESTUCHES MINI Y SIN TIPO':{'key':'99', 'productos':[], 'marcas':[], 'capacidades':[], 'refcount':0}
                                    })
        
        self.add_widget(self.productos)
        self.add_widget(self.marcas)
        self.add_widget(self.capacidades)
        self.add_widget(self.tipos)
        
        
        #hacemos el trabajo de sacar la relacion de los filtros .... muy muy lento por ahora
        self.fill_productosdeps()
        self.fill_marcasdeps()
        self.fill_capacidadesdeps()
        self.fill_tiposdeps()
        
        
    def selected_product(self, w, val):
        producto = w.parent.label.text.split(']')[1].split('[')[0]
        print producto, val
        
        if val:
            #marcas ... Agrega los que no esten de este producto
            for marcakey in self.productos.values[producto]['marcas']:
                if self.is_added_to(self.marcas, marcakey):
                    #incrementar contador de referencias
                    
            
            #capacidades
            
            #tipos
        
    def is_added_to(self, dropcontrol, key):
        
        
    def 
        
    def fill_productosdeps(self):
        '''
        Llena la lista de dependencias de los productos
        '''
        for i in sorted(self.productos.values):
            key = self.productos.values[i]['key']
            
            sql = "select CVE_ART from INVE01 where CVE_ART like '%s_______'" % key
            result = con.cursor().execute(sql).fetchall()
                
            
            for row in result:
                
                #marcas
                for marca in sorted(self.marcas.values):
                    
                    marca_cve = self.marcas.values[marca]['key']
                
                    if row[0][5] == marca_cve[0] and row[0][6] == marca_cve[1]:
                        
                        if marca_cve not in self.productos.values[i]['marcas']:
                            self.productos.values[i]['marcas'].append(marca_cve)
            
                #capacidades
                for capacidad in sorted(self.capacidades.values):
                    
                    capacidad_cve = self.capacidades.values[capacidad]['key']
                
                    if row[0][7] == capacidad_cve[0] and row[0][8] == capacidad_cve[1]:
                        
                        if capacidad_cve not in self.productos.values[i]['capacidades']:
                            self.productos.values[i]['capacidades'].append(capacidad_cve)
                
                
                #tipos
                for tipo in sorted(self.tipos.values):
                    
                    tipo_cve = self.tipos.values[tipo]['key']
                
                    if row[0][3] == tipo_cve[0] and row[0][4] == tipo_cve[1]:
                        
                        if tipo_cve not in self.productos.values[i]['tipos']:
                            self.productos.values[i]['tipos'].append(tipo_cve)
            
            
        #print self.productos.values['AGUARDIENTE']['marcas']
        #print self.productos.values['AGUARDIENTE']['capacidades']
        #print self.productos.values['AGUARDIENTE']['tipos']
    
    def fill_marcasdeps(self):
        '''
        Llena la lista de dependencias de las marcas
        '''
        for i in sorted(self.marcas.values):
            key = self.marcas.values[i]['key']
            
            sql = "select CVE_ART from INVE01 where CVE_ART like '_____%s__'" % key
            result = con.cursor().execute(sql).fetchall()
                
            
            for row in result:
                
                #productos
                for producto in sorted(self.productos.values):
                    
                    producto_cve = self.productos.values[producto]['key']
                
                    if row[0][0] == producto_cve[0] and row[0][1] == producto_cve[1]:
                        
                        if producto_cve not in self.marcas.values[i]['productos']:
                            self.marcas.values[i]['productos'].append(producto_cve)
            
                #capacidades
                for capacidad in sorted(self.capacidades.values):
                    
                    capacidad_cve = self.capacidades.values[capacidad]['key']
                
                    if row[0][7] == capacidad_cve[0] and row[0][8] == capacidad_cve[1]:
                        
                        if capacidad_cve not in self.marcas.values[i]['capacidades']:
                            self.marcas.values[i]['capacidades'].append(capacidad_cve)
                
                
                #tipos
                for tipo in sorted(self.tipos.values):
                    
                    tipo_cve = self.tipos.values[tipo]['key']
                
                    if row[0][3] == tipo_cve[0] and row[0][4] == tipo_cve[1]:
                        
                        if tipo_cve not in self.marcas.values[i]['tipos']:
                            self.marcas.values[i]['tipos'].append(tipo_cve)
            
    
    def fill_capacidadesdeps(self):
        '''
        Llena la lista de dependencias de las capacidades
        '''
        for i in sorted(self.capacidades.values):
            key = self.capacidades.values[i]['key']
            
            sql = "select CVE_ART from INVE01 where CVE_ART like '_______%s'" % key
            result = con.cursor().execute(sql).fetchall()
                
            
            for row in result:
                
                #productos
                for producto in sorted(self.productos.values):
                    
                    producto_cve = self.productos.values[producto]['key']
                
                    if row[0][0] == producto_cve[0] and row[0][1] == producto_cve[1]:
                        
                        if producto_cve not in self.capacidades.values[i]['productos']:
                            self.capacidades.values[i]['productos'].append(producto_cve)
            

                #marcas
                for marca in sorted(self.marcas.values):
                    
                    marca_cve = self.marcas.values[marca]['key']
                
                    if row[0][5] == marca_cve[0] and row[0][6] == marca_cve[1]:
                        
                        if marca_cve not in self.capacidades.values[i]['marcas']:
                            self.capacidades.values[i]['marcas'].append(marca_cve)
                
                            
                #tipos
                for tipo in sorted(self.tipos.values):
                    
                    tipo_cve = self.tipos.values[tipo]['key']
                
                    if row[0][3] == tipo_cve[0] and row[0][4] == tipo_cve[1]:
                        
                        if tipo_cve not in self.capacidades.values[i]['tipos']:
                            self.capacidades.values[i]['tipos'].append(tipo_cve)
                            
    
    def fill_tiposdeps(self):
        '''
        Llena la lista de dependencias de los tipos
        '''
        for i in sorted(self.tipos.values):
            key = self.tipos.values[i]['key']
            
            sql = "select CVE_ART from INVE01 where CVE_ART like '___%s____'" % key
            result = con.cursor().execute(sql).fetchall()
                
            
            for row in result:
                
                #productos
                for producto in sorted(self.productos.values):
                    
                    producto_cve = self.productos.values[producto]['key']
                
                    if row[0][0] == producto_cve[0] and row[0][1] == producto_cve[1]:
                        
                        if producto_cve not in self.tipos.values[i]['productos']:
                            self.tipos.values[i]['productos'].append(producto_cve)
            

                #marcas
                for marca in sorted(self.marcas.values):
                    
                    marca_cve = self.marcas.values[marca]['key']
                
                    if row[0][5] == marca_cve[0] and row[0][6] == marca_cve[1]:
                        
                        if marca_cve not in self.tipos.values[i]['marcas']:
                            self.tipos.values[i]['marcas'].append(marca_cve)
                
                            
                #capacidades
                for capacidad in sorted(self.capacidades.values):
                    
                    capacidad_cve = self.capacidades.values[capacidad]['key']
                
                    if row[0][7] == capacidad_cve[0] and row[0][8] == capacidad_cve[1]:
                        
                        if capacidad_cve not in self.tipos.values[i]['capacidades']:
                            self.tipos.values[i]['capacidades'].append(capacidad_cve)

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
        
        self.fromdate = DatePicker(label='Desde: ')
        self.todate = DatePicker(label='Hasta: ')
        self.box_fechas.add_widget( self.fromdate )
        self.box_fechas.add_widget( self.todate )
        
        
        self.fieldset_fechas.add_widget(self.box_fechas)
        
        self.fieldset_fechas.add_widget(CheckItem(label='[color=000000]Hacer comparacion de fechas[/color]'))
        
        
        self.layout.add_widget(self.fieldset_fechas)
        
        #LUGAR-CLIENTE
        self.fieldset_lugarcliente = BoxLayout(padding=20, spacing=20, size_hint_y=None, height=80)
        
        zonasvalues = [str(i)[4:][:3] for i in con.cursor().execute("select DISTINCT CVE_VEND from CLIE01").fetchall()]
        self.zonas = DropButton(text='[color=000000]Lugar / Zona[/color]', 
                                    values=zonasvalues, 
                                    item_cls=CheckItem,
                                    item_textcolor='000000'
                                    )
        
        '''
        #crear cursor para extraer las zonas directo de la base de datos
        cur = con.cursor()

        # Execute the SELECT statement:
        cur.execute("select DISTINCT CVE_VEND from CLIE01")

        #extraer todos los resultados
        result = cur.fetchall()
        
        #llenar todos los elementos
        for i in result:
            
            #verificar esta funcion, creo no esta funcionando
            if str(i) != '(None,)':
            
                n = str(i)[4:]
                self.prod = CheckItem(label=n[:3])
                
                self.zonas.drop.add_widget(self.prod)
        '''
        
        self.fieldset_lugarcliente.add_widget( self.zonas )
        
        
        self.fieldset_lugarcliente.add_widget(DropButton(text='[color=000000]Clientes[/color]'))
        
        self.layout.add_widget(self.fieldset_lugarcliente)
        
        
        #BOTON DE CONSULTA
        self.layout.add_widget(CustomButton(text='Consulta', size_hint=(None,None), size=(300,50), on_press=self.on_consulta))
        
        #RESULTADO
        self.fieldset_result = Fieldset(padding=20)
        self.txt_sql = TextInput()
        self.fieldset_result.add_widget(self.txt_sql)
        
        
        self.layout.add_widget(self.fieldset_result)
        
        
        self.add_widget(self.layout)
        
        
    def on_consulta(self, w):
        '''
        Evento lanzado al dar click al boton 'Iniciar consulta'
        Basicamente aqui va a crearse la consulta importante que
        necesitamos.
        '''
                
        #condicion para extraer productos
        sqlproduct = ""
        
        #recorrer la lista de productos y agregar a la consulta los que esten seleccionados
        for i in self.fieldset_categorias.productos.drop.children[0].children[:len(self.fieldset_categorias.productos.drop.children[0].children)-1]:
        
            #si el producto actual esta checked
            if i.checkbox.active:
                #print i.label.text
                
                #obtener el codigo
                cod = self.fieldset_categorias.productos.values[i.label.text]
                
                #print cod
                
                #si es el primer like, ponerlo como el primero
                if sqlproduct == '':
                    sqlproduct = "and ( (UPPER(PAR.CVE_ART) like '%s_______' " % cod
                else:
                    #ya hay likes, los siguientes son OR-eados
                    sqlproduct += " or UPPER(PAR.CVE_ART) like '%s_______' " % cod
                    
        addand = True
        
        #TIPO
        for i in self.fieldset_categorias.tipos.drop.children[0].children[:len(self.fieldset_categorias.tipos.drop.children[0].children)-1]:
        
            #si el producto actual esta checked
            if i.checkbox.active:
                #print i.label.text
                
                #obtener el codigo
                cod = self.fieldset_categorias.tipos.values[i.label.text]
                
                #print cod
                
                #si es el primer like, ponerlo como el primero
                if sqlproduct == '':
                    sqlproduct = "and ( (UPPER(PAR.CVE_ART) like '___%s____' " % cod
                    addand = False
                elif addand:
                    sqlproduct += ") and (UPPER(PAR.CVE_ART) like '___%s____' " % cod
                    addand = False
                else:
                    #ya hay likes, los siguientes son OR-eados
                    sqlproduct += " or UPPER(PAR.CVE_ART) like '___%s____' " % cod
                    

        addand = True
                    
        #MARCA
        for i in self.fieldset_categorias.marcas.drop.children[0].children[:len(self.fieldset_categorias.marcas.drop.children[0].children)-1]:
        
            #si el producto actual esta checked
            if i.checkbox.active:
                
                #obtener el codigo
                cod = self.fieldset_categorias.marcas.values[i.label.text]
                
                #si es el primer like, ponerlo como el primero
                if sqlproduct == '':
            
                    sqlproduct = "and ( (UPPER(PAR.CVE_ART) like '_____%s__' " % cod
                    addand = False
                elif addand:
                    sqlproduct += ") and (UPPER(PAR.CVE_ART) like '_____%s__' " % cod
                    addand = False
                else:
                    #ya hay likes, los siguientes son OR-eados
                    sqlproduct += " or UPPER(PAR.CVE_ART) like '_____%s__' " % cod
        
        
        addand = True
                    
        #CAPACIDAD
        for i in self.fieldset_categorias.capacidades.drop.children[0].children[:len(self.fieldset_categorias.capacidades.drop.children[0].children)-1]:
        
            #si el producto actual esta checked
            if i.checkbox.active:
                
                #obtener el codigo
                cod = self.fieldset_categorias.capacidades.values[i.label.text]
                
                #si es el primer like, ponerlo como el primero
                if sqlproduct == '':
                
                    sqlproduct = "and ( (UPPER(PAR.CVE_ART) like '_______%s' " % cod
                    addand = False
                elif addand:
                    sqlproduct += ") and (UPPER(PAR.CVE_ART) like '_______%s' " % cod
                    addand = False
                else:
                    #ya hay likes, los siguientes son OR-eados
                    sqlproduct += " or UPPER(PAR.CVE_ART) like '_______%s' " % cod
                    
        if sqlproduct != "":
            sqlproduct += ')      )'
            
        
        #FECHAS
        fecha_inicio = self.fromdate.get_date()
        fecha_final = self.todate.get_date()
        
        #ZONAS
        zones = ''
        for i in self.zonas.drop.children[0].children:
            if i.checkbox.active:
                if zones == '':
                    zones = "'  %s'" % i.label.text
                else:
                    zones += ",'  %s'" % i.label.text
                    
        if zones != '':
            zones = 'and CVE_VEND in (%s) )' % zones
        else:
            zones = ')'
            
        
        #consulta adecuada con buen rendimiento
        finalsql = '''select PAR.CVE_ART, INVE01.DESCR, sum(PAR.CANT), sum(PAR.PREC), INVE01.UNI_MED
            from PAR_FACTF01 PAR, INVE01
                where CVE_DOC in (select CVE_DOC from FACTF01 where FECHA_DOC between '%s' and '%s' and STATUS='E'
                        %s
                        and PAR.CVE_ART=INVE01.CVE_ART 
                        %s
                group by PAR.CVE_ART, INVE01.DESCR, INVE01.UNI_MED''' % (fecha_inicio, fecha_final, zones, sqlproduct)
        
        print finalsql
        
        #mostrar consulta en texto
        self.txt_sql.text = finalsql

        return

        #crear cursor
        cur = con.cursor()
        
        # Execute the SELECT statement:
        cur.execute(finalsql)

        #extraer todos los resultados
        result = cur.fetchall()
        
        #experimental
        lay_tableview = ScrollView()
        lay_boxview = BoxLayout(orientation='vertical', size_hint_y=None)
        
        #RESULTADOS EN LISTBOX
        for i in result:
        
        
            prod = ProductItem()
            
            prod.clave = str(i[0])
            prod.producto = str(i[1])
            
            #checar si este producto esta en piezas
            if ord(prod.clave[1]) >= ord('a') and ord(prod.clave[1]) <= ord('z'):
                print 'Convirtiendo a cajas', prod.clave
                
                sql = "select DESCR from INVE01 where CVE_ART=UPPER('%s')" % prod.clave
                
                #crear cursor
                cur = con.cursor()
        
                # Execute the SELECT statement:
                cur.execute(sql)

                #extraer todos los resultados
                result = cur.fetchall()
                
                protokens = result[0][0].split()
                print protokens
                
                botellaspcaja = protokens[-1]
                
                try:
                    #si la segunda es mayuscula, usar despues de la tercera
                    if ord(botellaspcaja[2]) >= ord('A') and ord(botellaspcaja[2]) <= ord('Z'):
                        cajas = (1.0/float( botellaspcaja[3:] )   ) * float(i[2])
                    elif ord(botellaspcaja[1]) >= ord('A') and ord(botellaspcaja[1]) <= ord('Z'):
                        cajas = (1.0/float( botellaspcaja[2:] )   ) * float(i[2])
                    else:
                        cajas = (1.0/float( botellaspcaja[1:] )   ) * float(i[2])
                except:
                    print '--- ERROR AL CONVERTIR CAJAS EN PRODUCTO: %s %s ------' % (prod.clave, prod.producto)
            else:
                cajas = i[2]
            
            prod.cajas = str(cajas)
            prod.total = str(i[3])
            
            lay_boxview.add_widget(prod)
            
            
        lay_boxview.height = len(lay_boxview.children)*35
        lay_tableview.add_widget(lay_boxview) 
        self.tab_prodtable.add_widget(lay_tableview)
            
        #RESULTADOS EN GRAFICA
        self.tab_prodgraph.remove_widget(self.plot_prod)
        
        self.plot_prod = Plot(
                    values={'0':50,
                            '1': 23,
                            '2': 10,
                            '3':80
                            }
                )
        
        self.tab_prodgraph.add_widget(self.plot_prod)
        
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
    
    #conectar con la base de datos ... la conexion es global para tener acceso desde 
    #cualquier parte del archivo
    con = firebirdsql.connect(
                    dsn='104.236.181.245:/SAE50EMPRE01.FDB',
                    user='sysdba', 
                    password='masterkey'
                        )
    
    #ejecutamos como aplicacion y le pasamos el widget de la clase Livesa
    runTouchApp(Livesa() )
