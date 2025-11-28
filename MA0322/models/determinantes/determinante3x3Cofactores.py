from utils.commonUtils import fmt


def determinante3x3Cofactores(m):
    """
    Determinante 3×3 por cofactores de la primera fila.
    Devuelve:
        det (float),
        pasos (lista de objetos visuales)
    """

    pasos = []

    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]

    # Mostrar la matriz visualmente
    pasos.append({"tipo": "texto", "valor": "Método de Cofactores (1ª fila) – Matriz 3×3"})
    pasos.append({"tipo": "matriz", "valor": m})
    pasos.append({"tipo": "texto", "valor": ""})

    # C11 (signo +)

    M11 = e * i - f * h
    C11 = M11
    term1 = a * C11

    pasos.append({"tipo": "texto", "valor": "Cálculo de C11"})
    pasos.append({"tipo": "matriz", "valor": [[e, f], [h, i]]})
    pasos.append({"tipo": "texto", "valor": f"M11 = ({fmt(e)} * {fmt(i)}) - ({fmt(f)} * {fmt(h)}) = {fmt(M11)}"})
    pasos.append({"tipo": "texto", "valor": f"C11 = +{fmt(M11)}"})
    pasos.append({"tipo": "texto", "valor": f"Término = a * C11 = {fmt(a)} * {fmt(C11)} = {fmt(term1)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    # C12 (signo -)

    M12 = d * i - f * g
    C12 = -M12
    term2 = b * C12

    pasos.append({"tipo": "texto", "valor": "Cálculo de C12"})
    pasos.append({"tipo": "matriz", "valor": [[d, f], [g, i]]})
    pasos.append({"tipo": "texto", "valor": f"M12 = ({fmt(d)} * {fmt(i)}) - ({fmt(f)} * {fmt(g)}) = {fmt(M12)}"})
    pasos.append({"tipo": "texto", "valor": f"C12 = -({fmt(M12)}) = {fmt(C12)}"})
    pasos.append({"tipo": "texto", "valor": f"Término = b * C12 = {fmt(b)} * {fmt(C12)} = {fmt(term2)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    # C13 (signo +)

    M13 = d * h - e * g
    C13 = M13
    term3 = c * C13

    pasos.append({"tipo": "texto", "valor": "Cálculo de C13"})
    pasos.append({"tipo": "matriz", "valor": [[d, e], [g, h]]})
    pasos.append({"tipo": "texto", "valor": f"M13 = ({fmt(d)} * {fmt(h)}) - ({fmt(e)} * {fmt(g)}) = {fmt(M13)}"})
    pasos.append({"tipo": "texto", "valor": f"C13 = +{fmt(M13)}"})
    pasos.append({"tipo": "texto", "valor": f"Término = c * C13 = {fmt(c)} * {fmt(C13)} = {fmt(term3)}"})
    pasos.append({"tipo": "texto", "valor": ""})

    # RESULTADO FINAL

    det = term1 + term2 + term3

    pasos.append({"tipo": "texto", "valor": "===================================="})
    pasos.append({"tipo": "texto",
                  "valor": f"Determinante = {fmt(term1)} + {fmt(term2)} + {fmt(term3)}"})
    pasos.append({"tipo": "texto",
                  "valor": f"DETERMINANTE FINAL 3×3 = {fmt(det)}"})
    pasos.append({"tipo": "texto", "valor": "===================================="})

    return det, pasos