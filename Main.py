"""
VESTER, una IA que administria tu lista de compras
Caracteristicas:
Menu con diferentes opciones

Simulacion de ofertas [Cupon encontrado! Obten un 10% de descuento con: "XXX-XXX-XXX"] |Aparece de manera aleatoria|
	- Simulacion de costo por tipo de envio [Por donde quieres enviar tu paquete: A, B o C] | En caso elija delivery 
	- Simulacion de comparacion de precios [Compras "X" a ">$" en este lugar esta a "<$"] | Aparece de manera aleatoria|
	- Simulacion de sugerencias de compras [Compraste "X" tal vez te interese "Y"] | Aparece de manera aleatoria |
	- Simulacion de reseñas [Este proveedor tiene una reseña de "X" estrellas] | Sin periodo de aparicion|
	- Simulacion de tendencias [Este producto super viral! tiene mas de "X" compras] | Sin periodo de aparicion |
    
Detalles:
	- Interfaz enriquezida 
	- Limpieza de pantalla 
	- Prefijo antes de las consultas [Vester >> Implementar.ramdom] 
	- Opcion Inicio / Perfil / Canasta / Reiniciar
	- Sugerencia Guia [Vester >> Esta seccion es usada principalmente para "X" asunto]


"""
import random

#----------------------------------------
saldo = 100
mostrarNotificaciones = True
distribuidores = [ "plazavea", "metro", "tottus" ]
listaDeProductosEnCarrito = [ ]
numeroDeLista = 0


#----------------------------------------
def Ofertar():
  descuento = random.randint(1,25)
  proveedor = random.choice(distribuidores)
  producto = random.choice(listaDeProductos)
  print(f"Vester >> Cupon encontrado! Obten un {descuento}% de descuento con: {proveedor} para tu producto: {producto}")

def agregarProductoACarrito():
  global numeroDeLista
  print("Vester > Escriba el nombre del producto que desea agregar y separando con una coma su precio: ")
  while True:
    datosDelProducto = input()
    if "," not in datosDelProducto:
      print("Vester > El formato no es el permitido, intentalo nuevamente.")
    else:
      break
  numeroDeLista = numeroDeLista + 1
  listaDeProductosEnCarrito.append(f"{numeroDeLista}. {producto}, precio: ${precio}")

def Menu():
  print("Administrador virtual de compras")
  print("Vester > Bienvenido(a) a Vester! estas son las opciones que tenemos para ti")
  print("1. Ofertas")
  print("2. Comparar precios")
  print("3. Añadir productos a carrito")
  print("4. Paqueteria")
  print("5. Reseñas")
  print("6. Ver saldo")
  print("7. Ver carrito")
  print("8. Terminar compra")
  print("9. Salir")
  
  opcion = input("Vester > Escriba la opcion deseada y presione ENTER: ")

  match opcion:
    case "1":
      Ofertar()
    case "2":
      CompararPrecios()
    case "3":
      AgregarProductoACarrito()
    case "4":
      Paqueteria()
    case "5":
      Resenas()
    case "6":
      VerSaldo()
    case "7":
      VerCarrito()
    case "8":
      TerminarCompra()
    case "9":
      Salir()
    case _:
      print(f"Vester > No existe la opcion {opcion}, intenta nuevamente ")
      Menu()
