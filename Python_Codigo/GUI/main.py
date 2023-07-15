import os
import json
from os.path import exists
# Kivy 
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
# KivyMD
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
##### BUTTONS AND BOX LAYOUTS ##########
Button  = MDRectangleFlatButton
Input  = MDTextField
########################################
######### VARIABLES ####################
buttonsSize = (0.5,0.1)

spaceSize = (0.05,0.05)

########################################


pathArchivo = os.path.abspath(__file__)
pathCarpeta = os.path.dirname(pathArchivo)
nombreArchivosBD = pathCarpeta + "\carrito.json"

listaDelCarrito = [] 

def spacer():
    return Widget(size_hint=spaceSize)

def validarNumero(cadena):
    try:
        # Es float en ves de int para poder soportar numeros con decimales
        float(cadena) 
        return True
    except ValueError:
        return False

def AñadirProducto(nombre,cantidad,precioUnitario):
    listaDelCarrito.append({
        'nombreProducto': nombre,
        'cantidadProducto': cantidad,
        'valorPorUnidad': precioUnitario
    })
    guardar()

def EliminarProducto(index):
    print("index: " + str(index))
    del listaDelCarrito[index]
    guardar()

def guardar():
    file = open(nombreArchivosBD,"w")
    datos = json.dumps(listaDelCarrito)
    file.write(datos)
    file.close()

def cargar():
    file_exists = exists(nombreArchivosBD)
    if not file_exists:
        guardar()
    file = open(nombreArchivosBD,"r")
    contenido = json.load(file)
    for item in contenido:
        listaDelCarrito.append(item)
    file.close()

def obtener_indice(numero):
    return (numero - 4) // 5

class ListaDeCompras:
    def __init__(self):
        pass
        self.tabla = self.TablaDeLaLista()
    def TablaDeLaLista(self):
        self.layout = MDFloatLayout()
        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.2, "center_y": 0.1},
            adaptive_size=True,
            #padding="24dp",
            spacing="24dp",
        )
        button = MDRectangleFlatButton(text="Eliminar seleccion", on_press=self.eliminar_producto)
        self.table = MDDataTable(
            use_pagination=True,
            check=True,
            pagination_menu_height=dp(40),
            rows_num=5,
            column_data=[
                ("Producto", dp(30)),
                ("Cantidad", dp(30)),
                ("Precio Unitario", dp(30)),
                ("Total", dp(30)),
                
            ],
            row_data=self.get_row_data(),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            
        )   
        button_box.add_widget(button)
        self.layout.add_widget(self.table)
        self.layout.add_widget(button_box)
        return self.layout

    def get_row_data(self):
        data = []
        for producto in listaDelCarrito:
            productoNombre = producto['nombreProducto']
            cantidad = producto['cantidadProducto']
            precioUnitario = producto['valorPorUnidad']
            precioTotal = str(float(cantidad) * float(precioUnitario))
            data.append((productoNombre, cantidad, precioUnitario, precioTotal))
        return data

    def eliminar_producto(self, instance_button):   
        if len(self.table.get_row_checks()) == 0:
            dialog = MDDialog(title="Error", text="Por favor seleccione al menos un producto")
            dialog.open()
        else:
            print(self.table.get_row_checks())
            for data_row in self.table.get_row_checks():
                for producto in listaDelCarrito:
                    if producto["nombreProducto"] == data_row[0] and producto["cantidadProducto"] == data_row[1] and producto["valorPorUnidad"] == data_row[2]:
                        listaDelCarrito.remove(producto)
                        break
            self.table.update_row_data(1,data=self.get_row_data()) 
    def actualizarTabla(self):
        self.tabla.children[1].update_row_data(1,data=self.get_row_data())
class VesterApp(MDApp):
    def build(self):
        cargar()
        lista_de_compras = ListaDeCompras()
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager = ScreenManager()
        self.icon = "assets/logo_Vester.png"
        
        self.menu_screen = Menu(name='menu')
        self.comprar_screen = Comprar(name='comprar', lista_de_compras = lista_de_compras)
        self.lista_screen = Lista(name='lista',lista_de_compras = lista_de_compras)

        self.screen_manager.add_widget(self.menu_screen)
        self.screen_manager.add_widget(self.comprar_screen)
        self.screen_manager.add_widget(self.lista_screen)
        return self.screen_manager

class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical",padding=25, size_hint=(1, 1))
        self.add_widget(self.layout)

        titulo = Label(text="Vester", font_size=50, size_hint=(1, 0.2))
        
        comprar_btn = Button(text="Comprar", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.10})
        comprar_btn.bind(on_press=self.ir_a_comprar)

        mostrar_btn = Button(text="Mostrar Lista", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.6})
        mostrar_btn.bind(on_press=self.ir_a_lista)

        salir_btn = Button(text="Salir", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.2})
        salir_btn.bind(on_press=self.salir)
        
        
        self.layout.add_widget(titulo)
        self.layout.add_widget(comprar_btn)
        self.layout.add_widget(spacer())
        self.layout.add_widget(mostrar_btn)
        self.layout.add_widget(spacer())
        self.layout.add_widget(salir_btn)

    def ir_a_comprar(self, instance):
        self.manager.current = 'comprar'

    def ir_a_lista(self, instance):
        self.manager.current = 'lista'

    def salir(self, instance):
        guardar()
        App.get_running_app().stop()

class Comprar(Screen):
    lista_de_compras = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lista_de_compras = kwargs['lista_de_compras']
        self.layout = BoxLayout(orientation="vertical", padding=10)

        self.lista = self.lista_de_compras.tabla
        
        titulo = Label(text="Comprar", font_size=50, size_hint=(1, 1.1), size_hint_y=None, height=dp(50))

        self.producto = Input(hint_text="Nombre del producto", multiline=False)
        self.cantidad = Input(hint_text="Cantidad", multiline=False)
        self.precio = Input(hint_text="Precio", multiline=False)


        añadir_btn = Button(text="Añadir al carrito", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.4})
        añadir_btn.bind(on_press=self.añadir_al_carrito)

        volver_btn = Button(text="Volver al menú principal", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.2})
        volver_btn.bind(on_press=self.volver_al_menu)
        
        self.add_widget(self.layout)

        self.layout.add_widget(titulo)
        self.layout.add_widget(self.producto)
        self.layout.add_widget(self.cantidad)
        self.layout.add_widget(self.precio)
        self.layout.add_widget(añadir_btn)
        self.layout.add_widget(volver_btn)
    def on_pre_enter(self, *args):
        print("Entras Compras")
        self.layout.add_widget(self.lista_de_compras.tabla,index=-1)
        return super().on_pre_enter(*args)
    def on_leave(self, *args):
        print("Sales Compras")
        self.layout.remove_widget(self.lista_de_compras.tabla)
        return super().on_pre_leave(*args)
    
    def añadir_al_carrito(self, instance):
        nombre = self.producto.text
        cantidad = self.cantidad.text
        precio = self.precio.text
        if nombre and cantidad and precio and validarNumero(cantidad) and validarNumero(precio):
            AñadirProducto(nombre, cantidad, precio)
            self.producto.text = ''
            self.cantidad.text = ''
            self.precio.text = ''
            dialog = MDDialog(title="Producto añadido", text="El producto ha sido añadido al carrito.")
            dialog.open()
            self.actualizar()
        else:
            dialog = MDDialog(title="Error", text="Por favor ingrese valores válidos.")
            dialog.open()

    def volver_al_menu(self, instance):
        self.manager.current = 'menu'
    def actualizar (self):
        self.layout.remove_widget(self.lista_de_compras.tabla)
        self.lista_de_compras.tabla = self.lista_de_compras.TablaDeLaLista()
        self.layout.add_widget(self.lista_de_compras.tabla,index=-1)

class Lista(Screen):
    lista_de_compras = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lista_de_compras = kwargs['lista_de_compras']
        self.body = BoxLayout(orientation='vertical',padding=10)
        
        titulo = Label(text="Lista de productos", font_size=50, size_hint=(1, 1.1), size_hint_y=None, height=dp(50))

        volver_btn = Button(text="Volver al menú principal", size_hint=(0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.2})
        volver_btn.bind(on_press=self.volver_al_menu)

        self.body.add_widget(titulo)
        #self.body.add_widget(self.lista)
        self.body.add_widget(volver_btn)
        self.add_widget(self.body)

    def on_pre_enter(self, *args):
        print("Entras Lista")
        self.body.add_widget(self.lista_de_compras.tabla,index=-1)
        return super().on_pre_enter(*args)
    
    def on_leave(self, *args):
        print("Sales Lista")
        self.body.remove_widget(self.lista_de_compras.tabla)
        return super().on_pre_leave(*args)
    
    def volver_al_menu(self, instance):
        self.manager.current = 'menu'

if __name__ == "__main__":
    VesterApp().run()
