from models.determinantes.validaciones import validarMatriz
from models.determinantes.determinante2x2 import determinante2x2
from models.determinantes.determinante3x3Sarrus import determinante3x3Sarrus
from models.determinantes.determinante3x3Cofactores import determinante3x3Cofactores
from models.determinantes.determinantesGauss import determinanteGauss
from models.determinantes.determinante4x4Cofactores import determinante4x4


def convertir_a_float(matriz):
    matriz_float = []
    for fila in matriz:
        fila_conv = []
        for v in fila:
            fila_conv.append(float(v))
        matriz_float.append(fila_conv)
    return matriz_float


def contar_filas(matriz):
    n = 0
    for _ in matriz:
        n += 1
    return n


def calcularDeterminante(matriz, metodo, modo=None, indice=None):
    ok, error = validarMatriz(matriz)
    if not ok:
        return None, [], error

    matriz = convertir_a_float(matriz)
    n = contar_filas(matriz)

    # 2×2
    if n == 2:
        if metodo != "cofactores":
            return None, [], "Para 2×2 solo se utiliza Cofactores."
        resultado, pasos = determinante2x2(matriz)
        return resultado, pasos, None

    # 3×3
    if n == 3:

        if metodo == "sarrus":
            return *determinante3x3Sarrus(matriz), None

        if metodo == "cofactores":
            return *determinante3x3Cofactores(matriz), None

        if metodo == "gauss":
            return *determinanteGauss(matriz), None

        return None, [], "Método no válido para matrices 3×3."

    # 4×4
    if n == 4:

        if metodo == "gauss":
            return *determinanteGauss(matriz), None

        if metodo == "cofactores":
            if modo not in ("fila", "columna"):
                return None, [], "Debe seleccionar FILA o COLUMNA."
            if indice not in (1,2,3,4):
                return None, [], "Índice debe ser 1 a 4."
            return *determinante4x4(matriz, metodo, modo, indice), None

        return None, [], "Método no válido para 4×4."

    
    # Error real
    return None, [], "Solo se permiten matrices 2×2, 3×3 y 4×4."