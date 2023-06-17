import os, json, time 

pathArchivo = os.path.abspath(__file__)
pathCarpeta = os.path.dirname(pathArchivo)
nombreArchivosBD = pathCarpeta + "\carrito.json"

detener = False
listaDelCarrito = [] # [{"nombreProducto": "Manzana","valorPorUnidad": 1.5,"cantidadProducto": 8}]

def LoadSaveData():
  file = open(nombreArchivosBD,"r")
  contenido = json.load(file)
  print(contenido)
  for item in contenido["Productos"]:
    print(item)
    listaDelCarrito.append(item)
  file.close()
  return

def SaveData():
  file = open(nombreArchivosBD,"w")
  datos = json.dumps(listaDelCarrito)
  file.write(datos)
  file.close()
  return

def LimpiarPantalla():
  # Windows
  if os.name == "nt":
    os.system("cls")
  # Mac y Linux
  else:
    os.system("clear")
  return

def validarNumero(cadena):
  try:
    int(cadena)
    return True
  except ValueError:
    return False
  
def MostrarSoloLista():
  #costo = 0
  print('Producto      | Cantidad      | PrecioUnitario | Total')
  for productos in listaDelCarrito:
    producto = productos.split(',')[0]
    cantidad = productos.split(',')[1]
    precioUnitario = productos.split(',')[2]
    precioTotal = str(float(cantidad) * float(precioUnitario))

    formatoProducto = producto.ljust(13)
    formatoCantidad = cantidad.rjust(13)
    formatoPrecio = precioUnitario.rjust(14)


    #print(producto.ljust(14), '|', cantidad.rjust(4), '|', unidad.rjust(15), '|', precio.rjust(14))
    print(formatoProducto, '|', formatoCantidad, '|', formatoPrecio, '|', precioTotal.rjust(13))

def MostrarLista():
  LimpiarPantalla()
  MostrarSoloLista()
  input('Vester > Presione cualquier tecla para volver al menu principal')
  Menu()

def AnadirProducto(nombre,cantidad,precioUnitario):
  listaDelCarrito.append({
    'nombreProducto': nombre,
    'cantidadProducto': cantidad,
    'valorPorUnidad': precioUnitario
  })
  SaveData()

def Comprar():
  LimpiarPantalla()
  print('Vester > Ingrese el nombre del producto que desea agregar: (escriba menu para volver al menu principal)')
  nombre = input('Vester > Producto > ')
  nombre = nombre.upper()
  if nombre == 'MENU':
    return Menu()
  else:
    print('Vester > Ingrese la cantidad del producto: ' )
    cantidad = input('Vester > Cantidad > ')
    while validarNumero(cantidad) == False:
      print('Vester > Error: Cantidad no valida, ingresala nuevamente: ')
      cantidad = input('Vester > Ingrese la cantidad del producto:')
    
    valorUnidad = input('Vester > Ingrese el precio unitario del producto: ' )
    while validarNumero(valorUnidad) == False:
      print('Vester > Error: Precio Unitario no valido, ingresalo nuevamente: ')
      valorUnidad = input('Vester > Ingrese el precio unitario del producto:')
    AnadirProducto(nombre,cantidad,valorUnidad)
    return
def Salir():
  LimpiarPantalla()
  print('Vester > Que tengas un bonito dia.')
  exit()
  
def Menu():
  LimpiarPantalla()
  print('Vester > Elige una opcion:')
  print('1) Comprar')
  print('2) Mostrar Lista')
  print('3) Salir del sistema')
  eleccion = input('Vester > Ingresa la opcion correcta (numero): ')
  verificacion = validarNumero(eleccion)
  if verificacion == True:
    if eleccion == '1':
      Comprar()
    elif eleccion == '2':
      MostrarLista()
    elif eleccion == '3':
      Salir()
  else:
    print('Vester > La opcion ingresada no es un numero.')
    time.sleep(2)
    return
  
def Main():
  LoadSaveData()
  print(listaDelCarrito)
  for producto in listaDelCarrito:
    print(producto.get('cantidadProducto') , producto.get('nombreProducto') , producto.get('valorPorUnidad'))
  Menu()

if __name__ == "__main__":
  Main()