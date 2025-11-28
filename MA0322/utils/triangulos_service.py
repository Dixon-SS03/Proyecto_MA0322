from models.triangulos_model import Triangulo

def resolver_triangulo(datos):
    """
    datos = {
        "A": [x1, y1],
        "B": [x2, y2],
        "C": [x3, y3]
    }

    Devuelve:
        resultado: dict con lados, ángulos, clasificaciones y pasos
    """

    A = datos.get("A")
    B = datos.get("B")
    C = datos.get("C")

    # Validación básica
    if A is None or B is None or C is None:
        return {
            "mensaje": "Faltan coordenadas de alguno de los puntos",
            "pasos": []
        }

    # Instanciamos el modelo
    triangulo = Triangulo(A, B, C)

    # Analizamos el triángulo
    resultado = triangulo.analizar()

    return resultado
