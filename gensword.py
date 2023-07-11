import random, string, re,requests, hashlib, os
from os.path import exists
import datetime

pathArchivo = os.path.abspath(__file__)
pathCarpeta = os.path.dirname(pathArchivo)
nombreArchivosBD = pathCarpeta + "\passwords.json"

# Kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.clipboard import Clipboard
# KivyMD
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.selectioncontrol.selectioncontrol import MDSwitch
##### BUTTONS AND BOX LAYOUTS ##########
Button  = MDRectangleFlatButton
Input  = MDTextField
########################################
##### VARIABLES #########################
buttonsSize = (0.5,0.1)

spaceSize = (0.05,0.05)

########################################
def spacer():
  return Widget(size_hint=spaceSize)

def verificar_contraseña(contra):
    puntaje = 0
    motivos = ""
    if len(contra) >= 8:
        puntaje += 1
    else:
        motivos += "La contraseña debe tener al menos 8 caracteres.\n"
    if re.search(r'[a-z]', contra) and re.search(r'[A-Z]', contra):
        puntaje += 1
    else:
        motivos += "La contraseña debe contener al menos una letra mayúscula y una minúscula.\n"
    if re.search(r'\d', contra):
        puntaje += 1
    else:
        motivos += "La contraseña debe contener al menos un número.\n"
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', contra):
        puntaje += 1
    else:
        motivos += "La contraseña debe contener al menos un carácter especial.\n"
    if re.search(r'(123|234|345|456|567|678|789|890)', contra):
        puntaje -= 1
        motivos += "La contraseña no debe contener secuencias numéricas.\n"
    if re.search(r'(qwertyuiop|asdfghjkl|zxcvbnm)', contra, re.IGNORECASE):
        puntaje -= 1
        motivos += "La contraseña no debe contener secuencias de teclado.\n"

    sha1hash = hashlib.sha1(contra.encode('utf-8')).hexdigest().upper()
    hash_prefix, hash_suffix = sha1hash[:5], sha1hash[5:]
    url = f'https://api.pwnedpasswords.com/range/{hash_prefix}'
    response = requests.get(url)
    if response.status_code == 200:
        hashes = response.text.splitlines()
        #print(hashes)
        for h in hashes:
            if hash_suffix in h:
                puntaje -= 1
                motivos += "La contraseña ha sido filtrada en una base de datos de contraseñas comprometidas.\n"
                break
    return puntaje, motivos

passwords = [{
  "password":"secreto123$",
  "score":4,
  "state":"Moderada",
  "hash":"f4716f4adec1e7e50c3e732e31e641c0b58b94dc",
  "time": "2021-07-31 01:23:00"
}]

def LoadPasswords():
  import json
  file_exists = exists(nombreArchivosBD)
  if not file_exists:
    SavePasswords()
  file = open(nombreArchivosBD,"r")
  contenido = json.load(file)
  for item in contenido:
    passwords.append(item)
  file.close()

def SavePasswords():
  import json
  file = open(nombreArchivosBD,"w+")
  passwords_json = json.dumps(passwords, indent=2)
  file.write(passwords_json)
  file.close()

def getState(puntaje):
  mensaje = ""
  match puntaje:
   case 0: 
     mensaje = "Muy débil"
   case 1:
     mensaje = "Débil"
   case 2:
     mensaje = "Moderada"
   case 3:
     mensaje = "Fuerte"
   case _:
     mensaje = "Muy fuerte"
  return mensaje
class JeremiasApp(MDApp):
  def build(self):
    self.theme_cls.primary_palette = "Orange"
    self.theme_cls.theme_style = "Dark"

    self.screen_manager = ScreenManager()

    self.menu_screen = Menu(name='menu')
    self.generarContraseña_screen = GenerarContraseña(name='GenerarContraseña')
    self.verificarContraseña_screen = VerificarContraseña(name='VerificarContraseña')

    self.screen_manager.add_widget(self.menu_screen)
    self.screen_manager.add_widget(self.generarContraseña_screen)
    self.screen_manager.add_widget(self.verificarContraseña_screen)
    return self.screen_manager

class Menu(Screen):
  def __init__(self, **kwargs):
    LoadPasswords()
    super().__init__(**kwargs)
    self.layout = BoxLayout(orientation="vertical",padding=25, size_hint=(1, 1))
    self.add_widget(self.layout)

    titulo = Label(text="Gessword", font_size=50, size_hint=(1, 0.2))
    
    generar_btn = Button(text="Generar contraseña", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.10})
    generar_btn.bind(on_press=self.ir_a_generar)

    verificar_btn = Button(text="Verificar contraseña", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.6})
    verificar_btn.bind(on_press=self.ir_a_verificar)

    salir_btn = Button(text="Salir", size_hint=buttonsSize, pos_hint={"center_x": 0.5, "center_y": 0.2})
    salir_btn.bind(on_press=self.salir)
    
    
    self.layout.add_widget(titulo)
    self.layout.add_widget(generar_btn)
    self.layout.add_widget(spacer())
    self.layout.add_widget(verificar_btn)
    self.layout.add_widget(spacer())
    self.layout.add_widget(salir_btn)

  def ir_a_generar(self, instance):
    self.manager.current = 'GenerarContraseña'

  def ir_a_verificar(self, instance):
    self.manager.current = 'VerificarContraseña'

  def salir(self, instance):
    App.get_running_app().stop()

class GenerarContraseña(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.layout = BoxLayout(orientation="vertical", padding=10)
    
    titulo = Label(text="Generar", font_size=50, size_hint=(1, 1.1), size_hint_y=None, height=dp(20))

    self.nombre = Input(hint_text="Ingrese su nombre", multiline=False)
    self.longitud = Input(hint_text="Longitud de la contraseña", multiline=False)
    
    self.minusculas_loyout = MDBoxLayout(size_hint=(1, 0.2), orientation="horizontal", padding=[dp(0), 0, dp(0), 0])
    self.mayusculas_loyout = MDBoxLayout(size_hint=(1, 0.2),orientation="horizontal", padding=[dp(0), 0, dp(0), 0])
    self.simbolos_loyout = MDBoxLayout(size_hint=(1, 0.2),orientation="horizontal", padding=[dp(0), 0, dp(0), 0])
    self.numeros_loyout = MDBoxLayout(size_hint=(1, 0.2),orientation="horizontal", padding=[dp(0), 0, dp(0), 0])

    self.minusculas_switch = MDSwitch(active=True, pos_hint={"center_x": 0.9, "center_y": 0.5})
    self.minusculas_label = MDLabel(text=f"Minusculas ({string.ascii_lowercase})")

    self.mayusculas_switch = MDSwitch(active=True,pos_hint={"center_x": 0.9, "center_y": 0.5})
    self.mayusculas_label = MDLabel(text=f"Mayusculas ({string.ascii_uppercase})")

    self.simbolos_switch = MDSwitch(active=True, pos_hint={"center_x": 0.9, "center_y": 0.5})
    self.simbolos_label = MDLabel(text=f"Simbolos ({string.punctuation})")

    self.numeros_switch = MDSwitch(active=True,pos_hint={"center_x": 0.9, "center_y": 0.5})
    self.numeros_label = MDLabel(text=f"Numeros ({string.digits})")
    
    self.minusculas_loyout.add_widget(self.minusculas_label)
    self.minusculas_loyout.add_widget(self.minusculas_switch)

    self.mayusculas_loyout.add_widget(self.mayusculas_label)
    self.mayusculas_loyout.add_widget(self.mayusculas_switch)

    self.simbolos_loyout.add_widget(self.simbolos_label)
    self.simbolos_loyout.add_widget(self.simbolos_switch)

    self.numeros_loyout.add_widget(self.numeros_label)
    self.numeros_loyout.add_widget(self.numeros_switch)

    self.contraseñasRecientes = self.HistorialdeContraseñas()


    generar_btn = Button(text="Generar", size_hint=(0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.55})
    generar_btn.bind(on_press=self.generarContraseña)

    regresar_btn = Button(text="Regresar", size_hint=(0.15, 0.05),pos_hint={"center_x": 0.5, "center_y": 0.1})
    regresar_btn.bind(on_press=self.regresar)

    self.layout.add_widget(titulo)
    self.layout.add_widget(self.nombre)
    self.layout.add_widget(self.longitud)
    self.layout.add_widget(self.minusculas_loyout)
    self.layout.add_widget(self.mayusculas_loyout)
    self.layout.add_widget(self.simbolos_loyout)
    self.layout.add_widget(self.numeros_loyout)
    self.layout.add_widget(self.contraseñasRecientes)
    self.layout.add_widget(generar_btn)
    self.layout.add_widget(regresar_btn)

    self.add_widget(self.layout)

  def generarContraseña(self, instance):
    longitud = self.longitud.text
    nombre = self.nombre.text
    if nombre == "" or longitud == "":
      dialog = MDDialog(title="Error", text="Falta completar nombre o longitud")
      dialog.open()
      return
    if not longitud.isdigit():
      dialog = MDDialog(title="Error", text="Ingrese solo numeros en longitud")
      dialog.open()
      return
    
    longitud = int(longitud)
    caracteresPermitidos = ""

    if self.minusculas_switch.active:
      caracteresPermitidos += string.ascii_lowercase
    if self.mayusculas_switch.active:
      caracteresPermitidos += string.ascii_uppercase
    if self.simbolos_switch.active:
      caracteresPermitidos += string.punctuation
    if self.numeros_switch.active:
      caracteresPermitidos += string.digits
    contraseña = nombre + self.GeneradorContraseña(longitud = longitud, caracteresPermitidos = caracteresPermitidos)
    dialog = MDDialog(title="Contraseña generada", text=f"Contraseña: {contraseña} | Copiada al portapapeles ")
    momento_actual = datetime.datetime.now()
    fechaTexto = momento_actual.strftime("%Y-%m-%d %H:%M")
    # obten el hash de la contraseña 
    passwordHash = hashlib.sha256(contraseña.encode("utf-8")).hexdigest()
    score, motivos = verificar_contraseña(contraseña)
    state = getState(score)

    passwords.append({
      "password": contraseña,
      "hash": passwordHash,
      "time": fechaTexto,
      "state": state,
      "score": score 
    })

    Clipboard.copy(contraseña)
    dialog.open() 

    self.layout.remove_widget(self.contraseñasRecientes)
    self.contraseñasRecientes = self.HistorialdeContraseñas()
    self.layout.add_widget(self.contraseñasRecientes, index = 2)
    SavePasswords()
  def GeneradorContraseña(self, longitud, caracteresPermitidos):
    contraseña = "".join(random.choice(caracteresPermitidos)for i in range(longitud))
    return contraseña
  def regresar(self, instance):
    self.manager.current = "menu"
  def HistorialdeContraseñas(self):
    self.historial = MDDataTable(
      size_hint=(0.7, 1),
      use_pagination=False,
      rows_num = 5,
      pos_hint={"center_x": 0.5, "center_y": 0.5},
      column_data=[
          ("Contraseña", dp(30)),
          ("Calificacion", dp(30)),
          ("Fecha de creacion", dp(60)),
      ],
      row_data=self.get_row_data(),
    )
    return self.historial
    
  def get_row_data(self):
    data = []
    for passwordData in passwords:
      password = passwordData['password']
      if len(password) > 5:
        password = password[:5] + '***'
      time = passwordData['time']
      state = passwordData['state']
      data.append((password, state, time))
    print(data)
    return data

class VerificarContraseña(Screen):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.body = BoxLayout(orientation='vertical',padding=10)
    
    titulo = Label(text="Verificar seguridad de la contraseña", font_size=50, size_hint=(1, 1.1), size_hint_y=None, height=dp(50))

    self.contraseña = Input(hint_text="Ingrese la contraseña", multiline=False)
    self.verificar_btn = Button(text="Verificar", size_hint=(0.5, 0.03), pos_hint={"center_x": 0.5, "center_y": 0.5})
    self.verificar_btn.bind(on_press=self.verificarContraseña)

    self.regresar_btn = Button(text="Regresar", size_hint=(0.15, 0.03),pos_hint={"center_x": 0.5, "center_y": 0.1})
    self.regresar_btn.bind(on_press=self.regresar)

    self.body.add_widget(titulo)
    self.body.add_widget(spacer())
    self.body.add_widget(self.contraseña)
    self.body.add_widget(spacer())
    self.body.add_widget(self.verificar_btn)
    self.body.add_widget(self.regresar_btn)

    self.add_widget(self.body)
  def verificarContraseña(self, instance):
    contraseña = self.contraseña.text
    if contraseña == "":
      dialog = MDDialog(title="Error", text="Ingrese contraseña")
      dialog.open()
      return
    puntaje,motivos = verificar_contraseña(contraseña)
    mensaje = getState(puntaje) 
    texto = f"La contraseña {contraseña} es contraseña {mensaje}"
    if motivos != "":
      texto += f"\n\nCosas a tomar en cuenta ⚠:\n{motivos}"
    dialog = MDDialog(title="Puntaje contraseña", text=texto)
    dialog.open()
  def regresar(self, instance):
    self.manager.current = "menu"

if __name__ == "__main__":
  JeremiasApp().run()
