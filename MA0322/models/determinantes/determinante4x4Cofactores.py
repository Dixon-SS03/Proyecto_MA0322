from ...utils.commonUtils import fmt
from .determinante3x3Sarrus import determinante3x3Sarrus
from .determinante3x3Cofactores import determinante3x3Cofactores


#   SUBMATRIZ 3×3

def submatriz3x3(matriz4, fila_eliminar, col_eliminar):
    """ Construye manualmente una submatriz 3×3 eliminando fila/columna """
    sub = []
    for f in range(4):
        if f != fila_eliminar:
            fila_nueva = []
            for c in range(4):
                if c != col_eliminar:
                    fila_nueva.append(matriz4[f][c])
            sub.append(fila_nueva)
    return sub


#  SIGNO DEL COFACTOR

def signoCofactor(f, c):
    """ Calcula (-1)^(f+c) sin potencias """
    suma = f + c
    signo = 1
    while suma > 0:
        signo = -signo
        suma -= 1
    return signo


#   DETERMINANTE 4×4 CON SALIDA VISUAL

def determinante4x4(matriz, metodo_3x3, modo, indice):
    """
    Calcula det(4×4) por cofactores con pasos visuales.
    metodo_3x3: "sarrus" o "cofactores"
    modo: "fila" o "columna"
    indice: 1–4
    """

    pasos = []
    det_total = 0.0

    # Convertir índice humano → interno
    k = indice - 1

    # Mostrar matriz original
    pasos.append({"tipo": "texto", "valor": f"Expansión por {modo} {indice}"})
    pasos.append({"tipo": "matriz", "valor": matriz})
    pasos.append({"tipo": "texto", "valor": "-----------------------------------"})

    #   DESARROLLO POR FILA

    if modo == "fila":
        fila = k

        for col in range(4):

            aij = matriz[fila][col]
            sg = signoCofactor(fila, col)

            pasos.append({"tipo": "texto", "valor": f"Elemento a[{fila+1},{col+1}] = {fmt(aij)}"})
            pasos.append({"tipo": "texto", "valor": f"Signo del cofactor: {fmt(sg)}"})

            # Submatriz
            sub = submatriz3x3(matriz, fila, col)

            pasos.append({"tipo": "texto", "valor": "Submatriz 3×3:"})
            pasos.append({"tipo": "matriz", "valor": sub})

            # Subdeterminante
            if metodo_3x3 == "sarrus":
                det_sub, pasos_sub = determinante3x3Sarrus(sub)
            else:
                det_sub, pasos_sub = determinante3x3Cofactores(sub)

            pasos.append({"tipo": "texto", "valor": "Cálculo del subdeterminante:"})

            for p in pasos_sub:
                pasos.append(p)     # YA vienen en formato visual

            cofactor = sg * det_sub
            termino = aij * cofactor
            det_total += termino

            pasos.append({"tipo": "texto", "valor": f"Cofactor = {fmt(sg)} * {fmt(det_sub)} = {fmt(cofactor)}"})
            pasos.append({"tipo": "texto", "valor": f"Término = {fmt(aij)} * {fmt(cofactor)} = {fmt(termino)}"})
            pasos.append({"tipo": "texto", "valor": ""})

    #   DESARROLLO POR COLUMNA

    else:
        col = k

        for fila in range(4):

            aij = matriz[fila][col]
            sg = signoCofactor(fila, col)

            pasos.append({"tipo": "texto", "valor": f"Elemento a[{fila+1},{col+1}] = {fmt(aij)}"})
            pasos.append({"tipo": "texto", "valor": f"Signo del cofactor: {fmt(sg)}"})

            sub = submatriz3x3(matriz, fila, col)

            pasos.append({"tipo": "texto", "valor": "Submatriz 3×3:"})
            pasos.append({"tipo": "matriz", "valor": sub})

            if metodo_3x3 == "sarrus":
                det_sub, pasos_sub = determinante3x3Sarrus(sub)
            else:
                det_sub, pasos_sub = determinante3x3Cofactores(sub)

            pasos.append({"tipo": "texto", "valor": "Cálculo del subdeterminante:"})

            for p in pasos_sub:
                pasos.append(p)

            cofactor = sg * det_sub
            termino = aij * cofactor
            det_total += termino

            pasos.append({"tipo": "texto", "valor": f"Cofactor = {fmt(sg)} * {fmt(det_sub)} = {fmt(cofactor)}"})
            pasos.append({"tipo": "texto", "valor": f"Término = {fmt(aij)} * {fmt(cofactor)} = {fmt(termino)}"})
            pasos.append({"tipo": "texto", "valor": ""})

    #   RESULTADO FINAL

    pasos.append({"tipo": "texto", "valor": "====================================="})
    pasos.append({"tipo": "texto", "valor": f"DETERMINANTE FINAL 4×4 = {fmt(det_total)}"})
    pasos.append({"tipo": "texto", "valor": "====================================="})

    return det_total, pasos
