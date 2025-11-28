from models.determinantes.calcularDeterminante import calcularDeterminante


def resolverDeterminante(datos):

    matriz  = datos.get("matriz")
    metodo  = datos.get("metodo")
    modo    = datos.get("modo")     # fila o columna
    indice  = datos.get("indice")   # 1..4

    if matriz is None:
        return None, [], "No se recibió la matriz."

    if metodo is None:
        return None, [], "No se recibió el método."

    resultado, pasos, error = calcularDeterminante(
        matriz,
        metodo,
        modo,
        indice
    )

    return resultado, pasos, error