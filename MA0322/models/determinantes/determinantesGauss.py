from ...utils.commonUtils import fmt


def copiaMatriz(m):
    """
    Copia profunda manual de matriz.
    """
    nueva = []
    for fila in m:
        fila_nueva = []
        for x in fila:
            fila_nueva.append(x)
        nueva.append(fila_nueva)
    return nueva




def calcularTamano(m):
    """
    Cuenta filas manualmente.
    """
    n = 0
    for _ in m:
        n += 1
    return n




def determinanteGauss(matriz):
    """
    Convierte la matriz en triangular superior usando eliminación gaussiana
    y luego multiplica los elementos de la diagonal principal.
    """

    pasos = []
    n = calcularTamano(matriz)

    # Copia profunda manual
    M = copiaMatriz(matriz)

    # Signo del determinante (cambia cuando se intercambian filas)
    det_signo = 1

    pasos.append("=== Método de Reducción Gaussiana ===")
    pasos.append("Objetivo: convertir la matriz en triangular superior")
    pasos.append("")

    fila = 0
    while fila < n:

        col = fila  # pivote en la diagonal

        
        if M[fila][col] == 0:

            swap = fila + 1
            encontrado = False

            while swap < n:
                if M[swap][col] != 0:
                    encontrado = True
                    break
                swap += 1

            if encontrado:
                pasos.append(
                    f"F{fila+1} ↔ F{swap+1}  (se intercambian filas, cambia el signo del determinante)"
                )
                det_signo = -det_signo

                temp = M[fila]
                M[fila] = M[swap]
                M[swap] = temp

                pasos.append("Matriz después del intercambio:")
                for f in M:
                    pasos.append("  " + str([fmt(x) for x in f]))
                pasos.append("")
            else:
                pasos.append(f"No se encontró pivote no nulo en columna {col+1}")
                pasos.append("Determinante = 0")
                return 0.0, pasos

        

        pivote = M[fila][col]
        pasos.append(f"Pivote en ({fila+1},{col+1}) = {fmt(pivote)}")

        fila2 = fila + 1
        while fila2 < n:

            abajo = M[fila2][col]

            if abajo != 0:

                m = abajo / pivote
                pasos.append(f"F{fila2+1} = F{fila2+1} - ({fmt(m)}) * F{fila+1}")

                col2 = 0
                while col2 < n:
                    M[fila2][col2] = M[fila2][col2] - m * M[fila][col2]
                    col2 += 1

                pasos.append("Matriz actualizada:")
                for f in M:
                    pasos.append("  " + str([fmt(x) for x in f]))
                pasos.append("")

            fila2 += 1

        fila += 1

    

    diag = 1.0
    i = 0
    while i < n:
        diag *= M[i][i]
        i += 1

    det = diag * det_signo

    pasos.append("=== Matriz triangular final ===")
    for ff in M:
        pasos.append("  " + str([fmt(x) for x in ff]))
    pasos.append("")

    pasos.append(f"Producto de la diagonal = {fmt(diag)}")
    pasos.append(f"Signo por intercambios = {fmt(det_signo)}")
    pasos.append(f"DETERMINANTE FINAL = {fmt(det)}")

    return det, pasos
