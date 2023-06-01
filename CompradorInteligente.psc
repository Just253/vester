Funcion AdministrarCarrito():
    Dimension lista[100]
    lista_titulo = "Ingrese su lista de compras:"
    presupuesto_titulo = "Ingrese su presupuesto maximo:"
    resultado_titulo = "El costo total es de $xxx y estos son los productos que se ajustan a su presupuesto:"
    Definir presupuesto_maximo Como Real

    Escribir "Comprador Inteligente"
    Escribir lista_titulo
    Para i = 1 Hasta 100 Hacer
        Escribir "Ingrese el producto nro. ", i, " (o pulse enter si ha terminado):"
        Leer lista[i]
        Si lista[i] = "" Entonces
            i = 100
        FinSi
    FinPara
    Escribir presupuesto_titulo
    Leer presupuesto_maximo
    Escribir "Presione ENTER para calcular"
    Leer tecla
    Escribir resultado_titulo

    Para i = 1 Hasta 100 Hacer
        Si lista[i] <> "" Entonces
            Escribir lista[i]
        FinSi
    FinPara
FinFuncion

Funcion resultado = Login(usuario,contraseña):
    Si usuario = "jotaro" y contraseña = "speedwagon":
        resultado = Verdadero
    sino:
        resultado = Falso
    FinSi
FinFuncion

Algoritmo CompradorInteligente
    Escribir "Ingrese usuario y contraseña (separados por un espacio): "
    Leer Usuario,Contrasena
    
    //Esta parte sería reemplazada por una consulta a una BD
FinAlgoritmo