import re

def eliminar_espacios(texto: str) -> str:
    salida = ""
    for caracteres in texto:
        if caracteres !=" ":
            salida += caracteres
    return salida

def dividir_ecuacuion(texto: str) -> str:
    izquierda = ""
    derecha = ""
    igualdad = False
    for caracteres in texto:
        if caracteres == "=":
            igualdad = True
            continue  
        if not igualdad:
            izquierda += caracteres
        else:
            derecha += caracteres
    if not igualdad:
        raise ValueError("La ecuacion no contiene ningun caracter de igualdad")
    return izquierda, derecha
       

def obtener_valores(ecuacion):
    valores = []
    posicion_actual = ""

    for i, caracter in enumerate(ecuacion):
        if (caracter == "+" or caracter == "-") and i !=0:
            valores += [posicion_actual]
            posicion_actual = caracter
        else:
            posicion_actual += caracter
    if posicion_actual != "":
        valores += [posicion_actual]
    return valores

def obtener_coeficientes(termino: str):

    variables = termino[-1]
    numeros = termino[:-1]

    if numeros == "" or numeros == "+":
        coeficiente = 1
    elif numeros == "-":
        coeficiente = -1
    else:
        coeficiente = int(numeros)

    return coeficiente, variables

def caracteres_validos(ecuacion: str):
    permitidos = "xyzXYZ+-=0123456789 "
    for c in ecuacion:
        es_valido = False
        for p in permitidos:
            if c == p:
                es_valido = True
                break
        if not es_valido:
            return False, c
    return True, None

def contiene_variable(izquierda: str):
    for c in izquierda:
        if c == "x" or c == "y" or c == "z":
            return True
    return False


def contador_igualdades(ecuacion):
    contador = 0
    for c in ecuacion:
        if c == "=":
            contador += 1
    return contador

def valores_enteros(valor: str):
    if valor == "":
        return False
    i = 0

    if valor[0] == "+" or valor[0] == "-":
        if len(valor) == 1:
            return False
        i = 1
    
    while i < len(valor):
        c = valor[i]
        digitos = False
        for d in "0123456789":
            if c == d:
                digitos = True
                break
        if not digitos:
            return False
        i += 1
    return True

def validar_formato_plano(ecuacion: str):
    errores = []

    solo_espacios = True
    for c in ecuacion:
        if c != " ":
            solo_espacios = False
            break
    if solo_espacios:
        errores.append("La ecuación no puede estar vacía.")
        return False, errores

    ok, invalido = caracteres_validos(ecuacion)
    if not ok:
        errores.append(f"Carácter no permitido: '{invalido}'")
        return False, errores

    total_igual = contador_igualdades(ecuacion)
    if total_igual == 0:
        errores.append("Falta el signo '='.")
        return False, errores
    if total_igual > 1:
        errores.append("La ecuación tiene más de un signo '='.")
        return False, errores

    try:
        ecuacion_sin = eliminar_espacios(ecuacion)
        izquierda, derecha = dividir_ecuacuion(ecuacion_sin)
    except ValueError as e:
        errores.append(str(e))
        return False, errores

    if not contiene_variable(izquierda):
        errores.append("La ecuación debe contener al menos una variable (x, y o z).")

    if not valores_enteros(derecha):
        errores.append("El lado derecho de la ecuación debe ser un número entero válido.")

    return len(errores) == 0, errores



def obtener_plano(ecuacion: str):
    ecuacion = eliminar_espacios(ecuacion)
    izquierda, derecha = dividir_ecuacuion(ecuacion)
    terminos = obtener_valores(izquierda)

    a = b = c = 0

    for t in terminos:
        coeficiente, variable = obtener_coeficientes(t)
        if variable == "x":
            a += coeficiente
        elif variable == "y":
            b += coeficiente
        elif variable == "z":
            c += coeficiente
        else:
            raise ValueError(f"La variable {variable} no es valida. Solo se permiten x, y, z.")

    try:
        d = int(derecha)
    except ValueError:
        raise ValueError("El lado derecho de la ecuacion debe ser un numero entero.")

    return a, b, c, d
#----------------------------------------------------------------------------------------------------------------------------------------------------


def numerico_texto(numero):
    digitos = "0123456789"

    if numero == 0:
        return "0"

    texto = ""
    while numero > 0:
        ultimo = numero % 10
        texto = digitos[ultimo] + texto
        numero = (numero - ultimo) 

    return texto


def longitud(texto):
    contador = 0

    for _ in texto:
        contador += 1
    return contador

def redondear_decimal(numero):
    
    if numero < 0:
        return "-" + numerico_texto(-numero)
    
    valor =  int(numero * 10000)

    entero = valor // 10000
    decimal = valor - entero * 10000

    entero_texto = numerico_texto(entero)
    decimal_texto = numerico_texto(decimal)

    while longitud(decimal_texto) < 4:
        decimal_texto = "0" + decimal_texto

    return entero_texto + "." + decimal_texto


def matriz_texto(matriz):
    texto = ""

    numero_fila = 0
    total_filas = 0

    for _ in matriz:
        total_filas += 1
    while numero_fila < total_filas:
        fila = matriz[numero_fila]

        texto =  texto + "["

        numero_columnas = 0
        total_columnas = 0

        for _ in fila:
            total_columnas += 1
        while numero_columnas < total_columnas:
            valor = fila[numero_columnas]
            valor_texto = redondear_decimal(valor)

            texto = texto + valor_texto

            if numero_columnas == 2:
                texto = texto + "|"
            else:
                texto = texto + " "
            numero_columnas += 1
        texto = texto + "] \n"
        numero_fila += 1
    return texto




if __name__ == "__main__":
    ecuacion = "= 5"

    ok, errores = validar_formato_plano(ecuacion)

    if not ok:
        print("Errores encontrados:")
        for e in errores:
            print("-", e)
    else:
        a, b, c, d = obtener_plano(ecuacion)
        print(f"Coeficientes del plano: a={a}, b={b}, c={c}, d={d}")