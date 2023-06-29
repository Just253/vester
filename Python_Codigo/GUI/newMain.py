import os
import json
from os.path import exists
# Kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

# KivyMD
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel


##### BUTTONS AND BOX LAYOUTS ##########
Button  = MDRectangleFlatButton
Input  = MDTextField
########################################


pathArchivo = os.path.abspath(__file__)
pathCarpeta = os.path.dirname(pathArchivo)
nombreArchivosBD = pathCarpeta + "\carrito.json"

listaDelCarrito = [] # [{"nombreProducto": "Manzana","valorPorUnidad": 1.5,"cantidadProducto": 8}]

def validarNumero(cadena):
    try:
        int(cadena)
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

class VesterApp(MDApp):
    def build(self):
        cargar()
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager = ScreenManager()
        self.icon = "assets/logo_Vester.png"
        self.menu_screen = Menu(name='menu')
        self.comprar_screen = Comprar(name='comprar')
        self.lista_screen = Lista(name='lista')
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
        self.layout.add_widget(titulo)

        comprar_btn = Button(text="Comprar", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.6})
        comprar_btn.bind(on_press=self.ir_a_comprar)
        self.layout.add_widget(comprar_btn)

        mostrar_btn = Button(text="Mostrar Lista", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.4})
        mostrar_btn.bind(on_press=self.ir_a_lista)
        self.layout.add_widget(mostrar_btn)

        salir_btn = Button(text="Salir", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.2})
        salir_btn.bind(on_press=self.salir)
        self.layout.add_widget(salir_btn)

    def ir_a_comprar(self, instance):
        self.manager.current = 'comprar'

    def ir_a_lista(self, instance):
        self.manager.current = 'lista'

    def salir(self, instance):
        guardar()
        App.get_running_app().stop()

class Comprar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=50)
        self.add_widget(self.layout)

        self.lista = Lista().devolver_SoloLista()
        
        titulo = Label(text="Comprar", font_size=50, size_hint=(1, 1.1))

        self.producto = Input(hint_text="Nombre del producto", multiline=False)
        self.cantidad = Input(hint_text="Cantidad", multiline=False)
        self.precio = Input(hint_text="Precio", multiline=False)


        añadir_btn = Button(text="Añadir al carrito", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.4})
        añadir_btn.bind(on_press=self.añadir_al_carrito)

        volver_btn = Button(text="Volver al menú principal", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.2})
        volver_btn.bind(on_press=self.volver_al_menu)

        self.layout.add_widget(titulo)
        self.layout.add_widget(self.lista)
        self.layout.add_widget(self.producto)
        self.layout.add_widget(self.cantidad)
        self.layout.add_widget(self.precio)
        self.layout.add_widget(añadir_btn)
        self.layout.add_widget(volver_btn)

    def añadir_al_carrito(self, instance):
        nombre = self.nombre_input.text.upper()
        cantidad = self.cantidad_input.text
        precio = self.precio_input.text
        if nombre and cantidad and precio and validarNumero(cantidad) and validarNumero(precio):
            AñadirProducto(nombre, cantidad, precio)
            self.nombre_input.text = ''
            self.cantidad_input.text = ''
            self.precio_input.text = ''
            dialog = MDDialog(title="Producto añadido", text="El producto ha sido añadido al carrito.")
            dialog.open()
        else:
            dialog = MDDialog(title="Error", text="Por favor ingrese valores válidos.")
            dialog.open()

    def volver_al_menu(self, instance):
        self.manager.current = 'menu'

class Lista(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body = BoxLayout(orientation='vertical',padding=10)
        
        titulo = MDLabel(text="Lista de productos", font_size=20, size_hint=(0.5, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(titulo)
        contentLista = self.TablaDeLaLista()

        volver_btn = Button(text="Volver al menú principal", size_hint=(0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.2})
        volver_btn.bind(on_press=self.volver_al_menu)

        #body.add_widget(titulo)
        self.body.add_widget(contentLista)
        self.body.add_widget(volver_btn)
        self.add_widget(self.body)
      

    def TablaDeLaLista(self):
        self.table = MDDataTable(
            size_hint=(1, 1.1),
            use_pagination=True,
            pagination_menu_height=dp(40),
            rows_num=len(listaDelCarrito),
            column_data=[
                ("Producto", dp(30)),
                ("Cantidad", dp(30)),
                ("Precio Unitario", dp(30)),
                ("Total", dp(30)),
                ("Eliminar", dp(30))
            ],
            row_data=self.get_row_data(),
            pos_hint={'center_x': 0.5, 'center_y': 1.5}
        )
        self.table.bind(on_row_press=self.eliminar_producto)
        

        return self.table
    def get_row_data(self):
        data = []
        for producto in listaDelCarrito:
            productoNombre = producto['nombreProducto']
            cantidad = producto['cantidadProducto']
            precioUnitario = producto['valorPorUnidad']
            precioTotal = str(float(cantidad) * float(precioUnitario))
            eliminar_btn = Button(text="Eliminar", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5, "center_y": 0.5})
            eliminar_btn.bind(on_press=self.eliminar_producto)
            data.append((productoNombre, cantidad, precioUnitario, precioTotal, eliminar_btn))
        return data

    def eliminar_producto(self, instance_table, instance_row):
        index = instance_row.index
        EliminarProducto(index)
        self.table.rows_num = len(listaDelCarrito)
        self.table.row_data = self.get_row_data()

    def volver_al_menu(self, instance):
        self.manager.current = 'menu'
    
    def devolver_SoloLista(self):
        return self.TablaDeLaLista()

if __name__ == "__main__":
    VesterApp().run()