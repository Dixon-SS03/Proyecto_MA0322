from utils.commonUtils import esNumero


def validarMatriz(matriz):
    """
    Valida matrices cuadradas permitidas:
      - 2×2
      - 3×3
      - 4×4

    Valida:
      - Estructura cuadrada
      - Campos vacíos
      - Número válido sin notación científica
      - Máximo 9 dígitos enteros y 4 decimales
    """

    if matriz is None:
        return False, "La matriz no fue enviada."

    # Número de filas
    filas = 0
    for _ in matriz:
        filas += 1

    if filas not in (2, 3, 4):
        return False, "La matriz debe ser 2×2, 3×3 o 4×4."

    # Validar que sea cuadrada
    f = 0
    while f < filas:
        columnas = 0
        for _ in matriz[f]:
            columnas += 1

        if columnas != filas:
            return False, "La matriz debe ser cuadrada."

        f += 1

    # Validar cada elemento
    f = 0
    while f < filas:

        c = 0
        while c < filas:

            valor_texto = str(matriz[f][c]).strip()

            if valor_texto == "":
                return False, f"El valor en ({f+1},{c+1}) está vacío."

            if not esNumero(valor_texto):
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) no es un número válido."

            # Validación de tamaño máximo permitido
            partes = valor_texto.split(".")
            entero = partes[0].replace("+", "").replace("-", "")
            decimal = partes[1] if len(partes) == 2 else ""

            if len(entero) > 9:
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) tiene demasiados dígitos enteros (máx 9)."

            if len(decimal) > 4:
                return False, f"El valor '{valor_texto}' en ({f+1},{c+1}) tiene demasiados decimales (máx 4)."

            c += 1

        f += 1

    return True, None