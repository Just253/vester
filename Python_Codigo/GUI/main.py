import os
import json
from os.path import exists
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton,MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout


pathArchivo = os.path.abspath(__file__)
pathCarpeta = os.path.dirname(pathArchivo)
nombreArchivosBD = pathCarpeta + "\carrito.json"

detener = False
listaDelCarrito = [] # [{"nombreProducto": "Manzana","valorPorUnidad": 1.5,"cantidadProducto": 8}]

class AgregarProductoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50)
        self.producto = MDTextField(hint_text='Producto')
        self.cantidad = MDTextField(hint_text='Cantidad')
        self.precio = MDTextField(hint_text='Precio')
        self.agregar = MDRectangleFlatButton(text='Agregar', on_release=self.AgregarProducto)
        self.volver = MDRectangleFlatButton(text='Volver', on_release=self.AbrirMenuPrincipalScreen)

        self.lista = MostrarListaScreen()

        self.layout.add_widget(self.lista)
        self.layout.add_widget(self.producto)
        self.layout.add_widget(self.cantidad)
        self.layout.add_widget(self.precio)
        self.layout.add_widget(self.agregar)
        self.layout.add_widget(self.volver)
        self.add_widget(self.layout)


    def AbrirMenuPrincipalScreen(self, obj):
        self.dialog = MDDialog(title='Advertencia', text='Se perderán todos los productos no guardados', size_hint=(0.7, 0.3))
        self.dialog.open()
        
        Main.screen.change_screen('menuPrincipal')

    def validarNumero(self, cadena):
        try:
            int(cadena)
            return True
        except ValueError:
            return False

    def AnadirProducto(self, nombre, cantidad, precioUnitario):
        listaDelCarrito.append({
            'nombreProducto': nombre,
            'cantidadProducto': cantidad,
            'valorPorUnidad': precioUnitario
        })
        self.SaveData()
        self.ActualizarLista()
        self.producto.text = ''
        self.cantidad.text = ''
        self.precio.text = ''
        self.dialog = MDDialog(title='Éxito', text='Producto agregado correctamente', size_hint=(0.7, 0.3))
        self.dialog.open()

    def AgregarProducto(self, obj):
        nombre = self.producto.text.upper()
        cantidad = self.cantidad.text
        precioUnitario = self.precio.text
        if nombre == '' or cantidad == '' or precioUnitario == '':
            self.dialog = MDDialog(title='Error', text='Por favor ingrese todos los campos', size_hint=(0.7, 0.3))
            self.dialog.open()
            return
        if not self.validarNumero(cantidad) or not self.validarNumero(precioUnitario):
            self.dialog = MDDialog(title='Error', text='Por favor ingrese números válidos', size_hint=(0.7, 0.3))
            self.dialog.open()
            return
        self.AnadirProducto(nombre, cantidad, precioUnitario)

class EliminarProductoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50)
        self.lista = MDList()
        self.MostrarSoloLista()
        self.layout.add_widget(self.lista)
        self.add_widget(self.layout)

    def MostrarSoloLista(self):
        self.lista.clear_widgets()
        for producto in listaDelCarrito:
            productoNombre = producto['nombreProducto']
            cantidad = producto['cantidadProducto']
            precioUnitario = producto['valorPorUnidad']
            precioTotal = str(float(cantidad) * float(precioUnitario))
            item = OneLineListItem(text=f'{productoNombre} | {cantidad} | {precioUnitario} | {precioTotal}')
            item.bind(on_release=self.EliminarProducto)
            self.lista.add_widget(item)

    def EliminarProducto(self, obj):
        index = listaDelCarrito.index({'nombreProducto': obj.text.split('|')[0].strip()})
        listaDelCarrito.pop(index)
        self.SaveData()
        self.ActualizarLista()

class MostrarListaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50)
        self.lista = MDList()
        self.MostrarSoloLista()
        self.layout.add_widget(self.lista)
        self.add_widget(self.layout)


    def MostrarSoloLista(self):
        self.lista.clear_widgets()
        encabezado = [
            ("PRODUCTO", dp(10)),
            ("CANTIDAD", dp(60)),
            ("VALOR UNITARIO", dp(60)),
            ("TOTAL", dp(60))

        ]

        datos = []
        for producto in listaDelCarrito:
            productoNombre = producto['nombreProducto']
            cantidad = producto['cantidadProducto']
            precioUnitario = producto['valorPorUnidad']
            precioTotal = str(float(cantidad) * float(precioUnitario))
            datos.append((productoNombre, cantidad, precioUnitario, precioTotal))

        tabla = MDDataTable( 
            size_hint=(0.9, 0.6),
            use_pagination=True,
            rows_num=len(datos),
            column_data=encabezado,
            row_data=datos
        )
        self.layout.add_widget(tabla)


class VesterApp(MDApp):
    def build(self):
        self.LoadSaveData()
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"

        self.screen = Screen()
        self.icon = 'assets\logo_Vester.png'
        self.Menu()
        return self.screen
    def Menu(self):
        self.screen.clear_widgets()
        buttons = MDRectangleFlatButton
        self.layout = BoxLayout(orientation='vertical', padding=50, size_hint=(1, 1))
        
        self.agregar_producto = buttons(text='Añadir producto al carrito', on_release=self.AbrirAgregarProductoScreen, size_hint=(1, 0.25))
        self.eliminar_producto = buttons(text='Eliminar producto', on_release=self.AbrirEliminarProductoScreen, size_hint=(1, 0.25))
        self.mostrar_lista = buttons(text='Mostrar lista', on_release=self.AbrirMostrarListaScreen, size_hint=(1, 0.25))
        self.salir = buttons(text='Salir', on_release=self.Salir, size_hint=(1, 0.25))
        self.layout.add_widget(self.agregar_producto)
        self.layout.add_widget(self.eliminar_producto)
        self.layout.add_widget(self.mostrar_lista)
        self.layout.add_widget(self.salir)
        self.screen.add_widget(self.layout)

    def AbrirAgregarProductoScreen(self, obj):
        self.screen.clear_widgets()
        self.screen.add_widget(AgregarProductoScreen())

    def AbrirEliminarProductoScreen(self, obj):
        self.screen.clear_widgets()
        self.screen.add_widget(EliminarProductoScreen())

    def AbrirMostrarListaScreen(self, obj):
        self.screen.clear_widgets()
        self.screen.add_widget(MostrarListaScreen())

    def LoadSaveData(self):
        file_exists = exists(nombreArchivosBD)
        if not file_exists:
            self.SaveData()
        file = open(nombreArchivosBD,"r")
        contenido = json.load(file)
        for item in contenido:
            listaDelCarrito.append(item)
        file.close()
        return

    def SaveData(self):
        file = open(nombreArchivosBD,"w")
        datos = json.dumps(listaDelCarrito)
        file.write(datos)
        file.close()
        return

    def LimpiarPantalla(self):
        self.lista.clear_widgets()

    def Salir(self, obj):
        self.LimpiarPantalla()
        self.SaveData()
        self.stop()

    def ActualizarLista(self):
        self.LimpiarPantalla()
        self.MostrarSoloLista()
        return

if __name__ == "__main__":
    Main = VesterApp().run()