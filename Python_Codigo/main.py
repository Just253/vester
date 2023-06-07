import os, time
# Variables
listaDelCarrito = [] 


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
  print('-----------------------------------------------------------------------------')

def MostrarLista():
  MostrarSoloLista()
  input('Vester > Presione cualquier tecla para volver al menu principal')
  Menu()

def AnadirCarrito():
  LimpiarPantalla()
  print('Lista de productos disponibles:')
  print('Nombre del producto               Costo por unidad            Unidades disponibles')
  print('Manzanas                          1.5                         25')
  print('Peras                             2.75                        15')
  print('Limones                           7.2                         10')
  print('-----------------------------------------------------------------------------')
  print('Vester > Tu lista de compras:')
  MostrarSoloLista()
  print('-----------------------------------------------------------------------------')
  print('Vester > Ingrese el nombre del producto que desea agregar: (escriba menu para volver al menu principal)')
  nombre = input('Vester > Producto > ')
  nombre = nombre.upper()
  if nombre == 'MENU':
    Menu()
  else:
    print('Vester > Ingrese la cantidad del producto: ' )
    cantidad = input('Cantidad > ')
    if validarNumero(cantidad) == False:
      print('Vester > La cantidad debe ser un numero, no se ha agregado el producto')
      time.sleep(3)
      AnadirCarrito()
  
    print('Vester > Ingrese el precio unitario del producto: ')
    precio = input('Precio > ')
    if validarNumero(precio) == False:
      print('Vester > El precio debe ser un numero, no se ha agregado el producto')
      time.sleep(3)
      AnadirCarrito()
    datos = nombre + ',' + cantidad + ',' + precio
    listaDelCarrito.append(datos)
    AnadirCarrito()

def EliminarCarrito():
  LimpiarPantalla()
  print('Vester > Tu lista de compras:')
  MostrarSoloLista()
  print('-----------------------------------------------------------------------------')
  print('Vester > Ingrese el numero del producto que desea eliminar: (escriba menu para volver al menu principal)')
  numero = input('Vester > Numero >')
  if numero.upper() == 'MENU':
    Menu()
  else:
    if validarNumero(numero) == False:
      print('Vester > Debe ingresar un numero valido, vuelva a intentarlo')
      time.sleep(3)
      EliminarCarrito()
  
    indice = int(numero)
    if indice > len(listaDelCarrito):
      print('Vester > Debe ingresar un numero valido, vuelva a intentarlo')
      time.sleep(3)
      EliminarCarrito()
    else:
      indice = indice - 1
      del listaDelCarrito[indice]
      EliminarCarrito()
  
def RealizarCompra():
  LimpiarPantalla()
  print('Vester > Su compra final es:')
  MostrarSoloLista()
  costo = 0
  for productos in listaDelCarrito:
    producto, cantidad, precio = productos.split(',')
    costoUnidad = float(precio)
    cantidad = int(cantidad)
    costo = costo + costoUnidad * cantidad
  print('Vester > Su compra ha finalizado, debe abonarse un total de $', costo)
  print('Vester > Gracias por su compra!')
  time.sleep(5)
  Menu()

def ObtenerAyuda():
  LimpiarPantalla()
  print('Vester > En caso de estar perdido puede revisar mediante el menu principal el listado de productos disponible,')
  print('Vester > si necesita eliminar un producto de su lista de compras puede seleccionar la opcion correspondiente del menu principal.')
  print('Vester > Si desea finalizar su compra y abonar sus productos, seleccione la opcion correspondiente del menu principal.')
  tecla = input('Vester > Presione una tecla para volver al menu principal...')
  Menu()




def Menu():
  LimpiarPantalla()
  print('-----------------------------------')
  print('   Vester - Comprador Inteligente  ')
  print('-----------------------------------')
  print('1. Anadir productos al carrito')
  print('2. Eliminar productos del carrito')
  print('3. Ver lista de productos')
  print('4. Realizar la compra')
  print('5. Obtener ayuda')
  print('6. Salir')
  opcion = int(input('Vester > Elija la opcion que desea: '))
  if opcion == 1:
    AnadirCarrito()
  elif opcion == 2:
    EliminarCarrito()
  elif opcion == 3:
    MostrarLista()
  elif opcion == 4:
    RealizarCompra()
  elif opcion == 5:
    ObtenerAyuda()
  elif opcion == 6:
    LimpiarPantalla()
    time.sleep(3)
    print('Gracias por usar Comprador Inteligente!')
    exit()
  else:
    print('La opcion ingresada no es correcta')
    time.sleep(2)
    Menu()


def CompradorInteligente():
  #Example 
  listaDelCarrito.append("Manzana,25,1.5")
  listaDelCarrito.append("Pera,15,2.75")
  listaDelCarrito.append("Limon,10,1.5")
  Menu()

CompradorInteligente()

