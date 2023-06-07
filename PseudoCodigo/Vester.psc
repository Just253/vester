Funcion resultado = incluye(text,string)
	longitudText = Longitud(text)
	longitudString = Longitud(string)
	Si longitudString > longitudText Entonces
		resultado = Falso
	SiNo
		Para posicion <- 1 Hasta longitudText Con Paso 1 hacer
			char = Subcadena(text,posicion,longitudString + posicion - 1)
			//Escribir char , " NUMERO: ", posicion
			Si char = string entonces
				resultado = verdadero
				posicion = longitudText
			SiNo
				resultado = Falso
			FinSi
		FinPara
	FinSi
FinFuncion


Funcion resultado = validarNumero(num)
	largo = Longitud(num)
	validarNum = Verdadero
	validarMenos = Verdadero
	conPunto = 0
	Para i=1 Hasta largo Con Paso 1 Hacer
		char =  Subcadena(num, i, i)
		Si incluye("0123456789.-", char) = Falso Entonces
			validarNum = Falso
			i = largo
		SiNo
			Si char = "." Entonces
				conPunto = conPunto + 1
			FinSi
			Si char = "-" Y i <> 1 Entonces
				ValidarMenos = Falso
				ValidarMenos = Falso
				i = largo
			FinSi
		FinSi
	Fin Para
	Si validarNum = Verdadero Y conPunto < 2 Y validarMenos = Verdadero Entonces
		resultado = Verdadero
	SiNo
		resultado = Falso
	FinSi
FinFuncion

Funcion espacios = RellenarEspacios(txt,num)
    Para i = 1 Hasta (num - Longitud(txt)) Hacer
        espacios = espacios + " "
    FinPara
FinFuncion

Funcion MostrarSoloLista(lista,index)
    costo = 0
    Escribir "Producto      | Cantidad      | PrecioUnitario | Total"
    Para _i = 1 Hasta index Hacer
        comas = 0
        indexPrimeraComa = 0
        Para __i = 1 Hasta Longitud(lista[_i])-1 Hacer
            letra = Subcadena(lista[_i], __i, __i)
            Si letra = "," Entonces
                comas = comas + 1
                Si comas = 1 Entonces
                    indexPrimeraComa = __i
                FinSi
                Si comas = 2 Entonces
                    producto = Subcadena(lista[_i],1,indexPrimeraComa-1)
                    costoUnidad = ConvertirANumero((Subcadena(lista[_i], __i+1, Longitud(lista[_i]))))
                    cantidad = ConvertirANumero(Subcadena(lista[_i], indexPrimeraComa + 1, __i - 1))
                    costo = costo + costoUnidad * cantidad
                    precio = costoUnidad * cantidad        
                    Escribir producto,RellenarEspacios(producto,14),"| ", cantidad,RellenarEspacios(ConvertirATexto(cantidad),14),"| ", costoUnidad,RellenarEspacios(ConvertirATexto(costoUnidad),16),"| ",precio, RellenarEspacios(ConvertirATexto(precio),14)         
                FinSi
            FinSi
        FinPara
    FinPara
FinFuncion

Funcion AnadirCarrito(lista,index)
	Limpiar Pantalla
	Escribir "Lista de productos disponibles:"
	Escribir "Nombre del producto               Costo por unidad            Unidades disponibles"
	Escribir "Manzanas                          1.5                         25"
	Escribir "Peras                             2.75                        15"
	Escribir "Limones                           7.2                         10"
	Escribir "-----------------------------------------------------------------------------"
	Escribir "Vester > Tu lista de compras:"
	MostrarSoloLista(lista,index)
	
	Escribir "Vester > Ingrese el nombre del producto que desea agregar: (escriba menu para volver al menu principal)"
	Leer nombre
	nombre = Minusculas(nombre)
	Si nombre = "menu" Entonces
		Menu(lista,index)
	Sino 
		Escribir "Vester > Ingrese la cantidad del producto:"
		Leer cantidad
		Si validarNumero(cantidad) = Falso Entonces
			Escribir "Vester > La cantidad debe ser un numero, no se ha agregado el producto"
			Esperar 3 segundos
			AnadirCarrito(lista,index)
		FinSi
		
		Escribir "Vester > Ingrese el precio unitario del producto:"
		Leer precio
		Si validarNumero(precio) = Falso Entonces
			Escribir "Vester > El precio debe ser un numero, no se ha agregado el producto"
			Esperar 3 segundos
			AnadirCarrito(lista,index)
		FinSi
		
		datos = nombre + "," + cantidad + "," + precio
		index = index + 1
		lista[index] = datos
		AnadirCarrito(lista,index)
	FinSi
	
FinFuncion

Funcion EliminarCarrito(lista,index)
    Limpiar Pantalla
    Escribir "Vester > La lista de compras que tiene es la siguiente:"
    MostrarSoloLista(lista,index)
    Escribir "Vester > Ingrese el numero del producto que desea eliminar: (escriba menu para volver al menu principal)"
    Leer _numero
    Si _numero = "menu" Entonces
        Menu(lista,index)
    Sino
        Si validarNumero(_numero) = Falso Entonces
            Escribir "Vester > Debe ingresar un numero valido, vuelva a intentarlo"
            Esperar 3 segundos
            EliminarCarrito(lista,index)
        Sino
            indice = ConvertirANumero(_numero)
            Para _i = indice Hasta index Hacer
                lista[_i] = lista[_i+1]
            FinPara	
            index = index - 1
            EliminarCarrito(lista,index)
        FinSi
    FinSi
FinFuncion

Funcion ListaProductos(lista,index)
    Limpiar Pantalla
    Escribir "Vester > La lista de productos disponibles es:"
    MostrarSoloLista(lista,index)
    Escribir "--------------------------------------"
    Escribir "Vester > Ingrese cualquier tecla para volver al menu principal"
    Leer tecla
    Menu(lista,index)
FinFuncion

Funcion RealizarCompra(lista,index)
    Limpiar Pantalla
    Escribir "Vester > Su compra final es:"
    MostrarSoloLista(lista,index)
    costo = 0
    Para _i = 1 Hasta index Hacer
        comas = 0
        indexPrimeraComa = 0
        Para __i = 1 Hasta Longitud(lista[_i])-1 Hacer
            letra = Subcadena(lista[_i], __i, __i)
            Si letra = "," Entonces
                comas = comas + 1
                Si comas = 1 Entonces
                    indexPrimeraComa = __i
                FinSi
                Si comas = 2 Entonces
                    costoUnidad = ConvertirANumero((Subcadena(lista[_i], __i+1, Longitud(lista[_i]))))
                    cantidad = ConvertirANumero(Subcadena(lista[_i], indexPrimeraComa + 1, __i - 1))
                    costo = costo + costoUnidad * cantidad      
                FinSi
            FinSi
        FinPara
    FinPara
    Escribir "Vester > Su compra ha finalizado, debe abonarse un total de $",costo
    Escribir "Vester > Gracias por su compra! Vuelva pronto."
FinFuncion

Funcion ObtenerAyuda(lista,index)
    Limpiar Pantalla
    Escribir "Vester > En caso de estar perdido puede revisar mediante el menu principal el listado de productos disponible,"
    Escribir "Vester > si necesita eliminar un producto de su lista de compras puede seleccionar la opcion correspondiente del menu principal."
    Escribir "Vester > Si desea finalizar su compra y abonar sus productos, seleccione la opcion correspondiente del menu principal."
    Leer tecla
    Menu(lista,index)
FinFuncion



Funcion Menu(lista,index)
	Limpiar Pantalla
	Escribir "-----------------------------------"
	Escribir "   Vester - Comprador Inteligente  "
	Escribir "-----------------------------------"
	Escribir "1. Anadir productos al carrito"
	Escribir "2. Eliminar productos del carrito"
	Escribir "3. Ver lista de productos"
	Escribir "4. Realizar la compra"
	Escribir "5. Obtener ayuda"
	Escribir "6. Salir"
    Escribir "Vester > Elija la opcion que desea:"
	Leer opcion
	Segun opcion Hacer
		1: AnadirCarrito(lista,index)
		2: EliminarCarrito(lista,index)
		3: ListaProductos(lista,index)
		4: RealizarCompra(lista,index)
		5: ObtenerAyuda(lista,index)
		6: 
			Limpiar Pantalla
			Escribir "Gracias por usar Comprador Inteligente!"
		De Otro Modo:
			Escribir "La opcion ingresada no es correcta"
			Esperar 2 segundos
			Menu(lista,index)
	FinSegun
FinFuncion

Algoritmo CompradorInteligente
    index = 3
    Dimension lista[10] 
    lista[1] = "Manzana,25,1.5"
    lista[2] = "Pera,15,2.75"
    lista[3] = "Limon,10,7.2"
	Menu(lista,index)
FinAlgoritmo
