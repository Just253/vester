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


// test incluye
Proceso sin_titulo
	resultado = incluye("a123bc123d123ef","az") // Verdadero
  
	Escribir resultado
  // incluye("abc", "abcd") # Falso 
  // incluye("abc", "c") # Verdadero
  // incluye("abc", "C") # Falso 
  // incluye("abc", "ABC") # Falso
  // incluye("Tostadora", "st") # Verdadero
  // incluye("Tostadora", "sT") # Falso

FinProceso
