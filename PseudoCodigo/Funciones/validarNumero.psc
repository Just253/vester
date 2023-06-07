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

// test
Proceso test
	Leer num
	result = validarNumero(num)
	Escribir result
FinProceso