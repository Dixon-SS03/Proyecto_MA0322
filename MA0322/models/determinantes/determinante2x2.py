from utils.commonUtils import fmt


def determinante2x2(matriz):
    """
    Calcula el determinante de una matriz 2×2:

        |a  b|
        |c  d|   =   ad − bc

    Devuelve:
      - determinante (float)
      - lista de pasos (strings)
    """

    pasos = []

    a = matriz[0][0]
    b = matriz[0][1]
    c = matriz[1][0]
    d = matriz[1][1]

    pasos.append("Determinante de matriz 2×2:")
    pasos.append(f"| {fmt(a)}   {fmt(b)} |")
    pasos.append(f"| {fmt(c)}   {fmt(d)} |")
    pasos.append("")

    pasos.append(f"Paso 1: multiplicar a*d = {fmt(a)} * {fmt(d)} = {fmt(a*d)}")
    pasos.append(f"Paso 2: multiplicar b*c = {fmt(b)} * {fmt(c)} = {fmt(b*c)}")

    det = a * d - b * c

    pasos.append("")
    pasos.append(f"Fórmula: (a*d) - (b*c) = {fmt(a*d)} - {fmt(b*c)}")
    pasos.append(f"Determinante final = {fmt(det)}")

    return det, pasos