from ...utils.commonUtils import fmt


def determinante3x3Sarrus(m):
    """
    Determinante 3×3 por la regla de Sarrus (solo 3×3).
    Retorna:
      - determinante (float)
      - pasos (lista de objetos visuales)
    """

    pasos = []

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]

    # Mostrar matriz original visualmente
    pasos.append({"tipo": "texto", "valor": "Método de Sarrus para 3×3"})
    pasos.append({"tipo": "matriz", "valor": m})
    pasos.append({"tipo": "texto", "valor": ""})

    # DIAGONALES PRINCIPALES
    p1 = a * e * i
    p2 = b * f * g
    p3 = c * d * h

    pasos.append({"tipo": "texto", "valor": "Diagonales principales:"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(a)} * {fmt(e)} * {fmt(i)} = {fmt(p1)}"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(b)} * {fmt(f)} * {fmt(g)} = {fmt(p2)}"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(c)} * {fmt(d)} * {fmt(h)} = {fmt(p3)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    suma_principales = p1 + p2 + p3
    pasos.append({"tipo": "texto", "valor": f"Suma diagonales principales = {fmt(suma_principales)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    # DIAGONALES SECUNDARIAS
    s1 = c * e * g
    s2 = a * f * h
    s3 = b * d * i

    pasos.append({"tipo": "texto", "valor": "Diagonales secundarias:"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(c)} * {fmt(e)} * {fmt(g)} = {fmt(s1)}"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(a)} * {fmt(f)} * {fmt(h)} = {fmt(s2)}"})
    pasos.append({"tipo": "texto", "valor": f"{fmt(b)} * {fmt(d)} * {fmt(i)} = {fmt(s3)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    suma_secundarias = s1 + s2 + s3
    pasos.append({"tipo": "texto", "valor": f"Suma diagonales secundarias = {fmt(suma_secundarias)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    # RESULTADO FINAL
    det = suma_principales - suma_secundarias

    pasos.append({"tipo": "texto", "valor":
                  f"Determinante = {fmt(suma_principales)} − {fmt(suma_secundarias)}"})
    pasos.append({"tipo": "texto", "valor": f"DETERMINANTE FINAL = {fmt(det)}"})

    return det, pasos
