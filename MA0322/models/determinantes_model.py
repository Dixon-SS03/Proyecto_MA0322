# ============================================================
#   VALIDACIONES Y UTILIDADES
# ============================================================

def fmt(n):
    """
    Formatea un número:
    - Si es entero exacto: lo muestra sin decimales
    - Si tiene decimales reales: mantiene decimales
    """
    if int(n) == n:
        return str(int(n))
    return str(n)



def es_numero(valor):
    """
    Valida manualmente si un string representa un número real válido.
    """

    if valor is None:
        return False

    valor = valor.strip()
    if valor == "":
        return False

    # No permitir comas ni notación científica
    for c in valor:
        if c == "," or c == "e" or c == "E":
            return False

    i = 0
    punto = False

    # Signo inicial
    if valor[0] == "+" or valor[0] == "-":
        if len(valor) == 1:
            return False
        i = 1

    # No permitir ".5" o "5."
    if valor[i] == "." or valor[-1] == ".":
        return False

    # Validación carácter por carácter
    while i < len(valor):
        c = valor[i]

        if c == ".":
            if punto:
                return False
            punto = True
        else:
            es_digito = False
            for d in "0123456789":
                if c == d:
                    es_digito = True
                    break
            if not es_digito:
                return False
        i += 1

    return True



def validar_matriz(matriz):

    if matriz is None:
        return False, "La matriz no fue enviada."

    filas = len(matriz)
    if filas not in (3, 4):
        return False, "La matriz debe ser 3x3 o 4x4."

    for fila in matriz:
        if len(fila) != filas:
            return False, "La matriz debe ser cuadrada."

    # Validación de cada elemento
    for f in range(filas):
        for c in range(filas):
            valor_texto = str(matriz[f][c]).strip()

            if valor_texto == "":
                return False, f"El valor en ({f+1},{c+1}) está vacío."

            if not es_numero(valor_texto):
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) no es válido."

            partes = valor_texto.split(".")
            entero = partes[0].replace("+", "").replace("-", "")
            decimal = partes[1] if len(partes) == 2 else ""

            if len(entero) > 9:
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) tiene demasiados dígitos enteros."

            if len(decimal) > 4:
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) tiene demasiados decimales."

    return True, None



# ============================================================
#   DETERMINANTE 3x3 (SARRUS)
# ============================================================

def determinante_3x3_sarrus(m):
    pasos = []

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]

    p1 = a * e * i
    p2 = b * f * g
    p3 = c * d * h

    pasos.append(f"Diagonal principal 1: {fmt(a)} * {fmt(e)} * {fmt(i)} = {fmt(p1)}")
    pasos.append(f"Diagonal principal 2: {fmt(b)} * {fmt(f)} * {fmt(g)} = {fmt(p2)}")
    pasos.append(f"Diagonal principal 3: {fmt(c)} * {fmt(d)} * {fmt(h)} = {fmt(p3)}")

    suma_principales = p1 + p2 + p3
    pasos.append(f"Suma diagonales principales = {fmt(p1)} + {fmt(p2)} + {fmt(p3)} = {fmt(suma_principales)}")

    s1 = c * e * g
    s2 = a * f * h
    s3 = b * d * i

    pasos.append(f"Diagonal secundaria 1: {fmt(c)} * {fmt(e)} * {fmt(g)} = {fmt(s1)}")
    pasos.append(f"Diagonal secundaria 2: {fmt(a)} * {fmt(f)} * {fmt(h)} = {fmt(s2)}")
    pasos.append(f"Diagonal secundaria 3: {fmt(b)} * {fmt(d)} * {fmt(i)} = {fmt(s3)}")

    suma_secundarias = s1 + s2 + s3
    pasos.append(f"Suma diagonales secundarias = {fmt(s1)} + {fmt(s2)} + {fmt(s3)} = {fmt(suma_secundarias)}")

    determinante = suma_principales - suma_secundarias
    pasos.append(f"Determinante = {fmt(suma_principales)} - {fmt(suma_secundarias)} = {fmt(determinante)}")

    return determinante, pasos



# ============================================================
#   DETERMINANTE 3x3 POR COFACTORES
# ============================================================

def determinante_3x3_cofactores(m):
    pasos = []

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]

    pasos.append("Desarrollo por la primera fila:")
    pasos.append("det(A) = a*C11 - b*C12 + c*C13")
    pasos.append(" ")

    M11 = e * i - f * h
    C11 = M11
    pasos.append(f"M11 = ({fmt(e)}*{fmt(i)} - {fmt(f)}*{fmt(h)}) = {fmt(M11)}")
    pasos.append(f"C11 = +{fmt(M11)}")
    term1 = a * C11
    pasos.append(f"Término 1 = {fmt(a)} * {fmt(C11)} = {fmt(term1)}")
    pasos.append(" ")

    M12 = d * i - f * g
    C12 = -M12
    pasos.append(f"M12 = ({fmt(d)}*{fmt(i)} - {fmt(f)}*{fmt(g)}) = {fmt(M12)}")
    pasos.append(f"C12 = -({fmt(M12)}) = {fmt(C12)}")
    term2 = b * C12
    pasos.append(f"Término 2 = {fmt(b)} * {fmt(C12)} = {fmt(term2)}")
    pasos.append(" ")

    M13 = d * h - e * g
    C13 = M13
    pasos.append(f"M13 = ({fmt(d)}*{fmt(h)} - {fmt(e)}*{fmt(g)}) = {fmt(M13)}")
    pasos.append(f"C13 = +{fmt(M13)}")
    term3 = c * C13
    pasos.append(f"Término 3 = {fmt(c)} * {fmt(C13)} = {fmt(term3)}")
    pasos.append(" ")

    determinante = term1 + term2 + term3
    pasos.append(f"Determinante = {fmt(term1)} + {fmt(term2)} + {fmt(term3)} = {fmt(determinante)}")

    return determinante, pasos



# ============================================================
#   SUBMATRIZ 3x3 (PARA COFACTORES 4x4)
# ============================================================

def submatriz_3x3(matriz, fila_elim, col_elim):
    sub = []
    for f in range(4):
        if f != fila_elim:
            nueva = []
            for c in range(4):
                if c != col_elim:
                    nueva.append(matriz[f][c])
            sub.append(nueva)
    return sub



# ============================================================
#   DETERMINANTE 4x4 POR COFACTORES
# ============================================================

def determinante_4x4(matriz, metodo_3x3, modo, indice):
    pasos = []
    k = indice - 1

    pasos.append(f"Desarrollo por {modo} {indice}")
    pasos.append(" ")

    det_total = 0

    # ----------------------------------------------------
    # DESARROLLO POR FILA
    # ----------------------------------------------------
    if modo == "fila":
        fila = k
        for col in range(4):

            elemento = matriz[fila][col]
            signo = (-1) ** (fila + col)

            pasos.append(f"Elemento a[{fila+1},{col+1}] = {fmt(elemento)}")
            pasos.append(f"Signo del cofactor = (-1)^({fila+1}+{col+1}) = {fmt(signo)}")

            sub = submatriz_3x3(matriz, fila, col)

            pasos.append("Submatriz 3x3:")
            for fi in sub:
                pasos.append("  " + str([fmt(x) for x in fi]))
            pasos.append(" ")

            if metodo_3x3 == "sarrus":
                det_sub, pasos_sub = determinante_3x3_sarrus(sub)
            else:
                det_sub, pasos_sub = determinante_3x3_cofactores(sub)

            pasos.append("Cálculo 3x3:")
            for p in pasos_sub:
                pasos.append("  " + p)

            cofactor = signo * det_sub
            pasos.append(f"Cofactor = {fmt(signo)} * {fmt(det_sub)} = {fmt(cofactor)}")

            termino = elemento * cofactor
            pasos.append(f"Término = {fmt(elemento)} * {fmt(cofactor)} = {fmt(termino)}")
            pasos.append(" ")

            det_total += termino


    # ----------------------------------------------------
    # DESARROLLO POR COLUMNA
    # ----------------------------------------------------
    else:
        col = k
        for fila in range(4):

            elemento = matriz[fila][col]
            signo = (-1) ** (fila + col)

            pasos.append(f"Elemento a[{fila+1},{col+1}] = {fmt(elemento)}")
            pasos.append(f"Signo del cofactor = (-1)^({fila+1}+{col+1}) = {fmt(signo)}")

            sub = submatriz_3x3(matriz, fila, col)

            pasos.append("Submatriz 3x3:")
            for fi in sub:
                pasos.append("  " + str([fmt(x) for x in fi]))
            pasos.append(" ")

            if metodo_3x3 == "sarrus":
                det_sub, pasos_sub = determinante_3x3_sarrus(sub)
            else:
                det_sub, pasos_sub = determinante_3x3_cofactores(sub)

            pasos.append("Cálculo 3x3:")
            for p in pasos_sub:
                pasos.append("  " + p)

            cofactor = signo * det_sub
            pasos.append(f"Cofactor = {fmt(signo)} * {fmt(det_sub)} = {fmt(cofactor)}")

            termino = elemento * cofactor
            pasos.append(f"Término = {fmt(elemento)} * {fmt(cofactor)} = {fmt(termino)}")
            pasos.append(" ")

            det_total += termino

    pasos.append("======================================")
    pasos.append(f"DETERMINANTE FINAL 4x4 = {fmt(det_total)}")
    pasos.append("======================================")

    return det_total, pasos



# ============================================================
#   FUNCIÓN PRINCIPAL (LLAMADA POR BACKEND)
# ============================================================

def calcular_determinante(matriz, metodo, fila, columna):

    ok, error = validar_matriz(matriz)
    if not ok:
        return None, [], error

    # Convertir matriz a float
    matriz_float = []
    for fila_m in matriz:
        fila_conv = []
        for v in fila_m:
            fila_conv.append(float(v))
        matriz_float.append(fila_conv)

    matriz = matriz_float
    n = len(matriz)

    if n == 3:
        if metodo == "sarrus":
            resultado, pasos = determinante_3x3_sarrus(matriz)
        else:
            resultado, pasos = determinante_3x3_cofactores(matriz)

    elif n == 4:
        resultado, pasos = determinante_4x4(matriz, metodo, fila, columna)

    else:
        return None, [], "Solo se permiten matrices 3x3 o 4x4."

    return resultado, pasos, None
