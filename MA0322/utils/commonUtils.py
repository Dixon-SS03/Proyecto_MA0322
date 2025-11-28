def fmt(n):
    """
    Formatea un número:
      - Si es entero exacto lo devuelve sin decimales.
      - Si tiene parte decimal lo mantiene tal cual.

    Nota:
      Maneja errores por si llega algo inesperado.
    """
    try:
        if int(n) == n:
            return str(int(n))
    except Exception:
        return str(n)

    return str(n)


def esNumero(valor):
    """
    Valida manualmente si un string representa un número real simple.

    NO PERMITE:
      - notación científica (e / E)
      - comas
      - doble signo (++, --, +-, -+)
      - ".5" o "5."
      - caracteres no numéricos

    PERMITE:
      - enteros (5, -3, +10)
      - decimales positivos o negativos (10.25, -7.5, +0.001)

    Retorna:
      True  si es válido
      False si no lo es
    """

    if valor is None:
        return False

    valor = str(valor).strip()
    if valor == "":
        return False

    # Prohibidos
    for c in valor:
        if c in (",", "e", "E"):
            return False

    # Signos duplicados
    if "++" in valor or "--" in valor or "+-" in valor or "-+" in valor:
        return False

    i = 0
    punto = False

    # Signo inicial
    if valor[0] == "+" or valor[0] == "-":
        if len(valor) == 1:
            return False
        i = 1

    # No permitir ".5" ni "5."
    if valor[i] == "." or valor[-1] == ".":
        return False

    # Validación carácter a carácter
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


def signoCofactor(f, c):
    """
    Devuelve el signo del cofactor usando la regla:

        (-1)^(f + c)

    donde f y c son índices base 0.

    Cambiar de signo (f+c) veces.
    """
    suma = f + c
    signo = 1

    while suma > 0:
        signo = -signo
        suma -= 1

    return signo
