from models.determinantes_model import calcular_determinante


def resolver_determinante(datos):
    """
    datos = {
        "matriz": [[...]],
        "metodo": "sarrus" / "cofactores",
        "fila": 1  (solo 4x4),
        "columna": 2 (solo 4x4)
    }
    """

    matriz = datos.get("matriz")
    metodo = datos.get("metodo")
    fila = datos.get("fila")
    columna = datos.get("columna")

    if matriz is None:
        return None, [], "No se recibió la matriz."

    # Llamamos al modelo matemático
    resultado, pasos, error = calcular_determinante(
        matriz, metodo, fila, columna
    )

    return resultado, pasos, error
