

def validar_numero(valor):
    try:
        num = float(valor)
        return (True, num, "")
    except (ValueError, TypeError):
        return (False, None, f"'{valor}' no es un número válido")


def validar_plano(datos_plano):
  
    errores = []
    
    campos_requeridos = ['a', 'b', 'c', 'd']
    for campo in campos_requeridos:
        if campo not in datos_plano:
            errores.append(f"Falta el campo '{campo}'")
    
    if errores:
        return (False, errores)
    
    coeficientes = {}
    for campo in campos_requeridos:
        es_valido, num, error = validar_numero(datos_plano[campo])
        if not es_valido:
            errores.append(f"Coeficiente {campo}: {error}")
        else:
            coeficientes[campo] = num
    
    if errores:
        return (False, errores)
    
    if coeficientes['a'] == 0 and coeficientes['b'] == 0 and coeficientes['c'] == 0:
        errores.append("El plano no es válido: los coeficientes a, b y c no pueden ser todos cero")
    
    if errores:
        return (False, errores)
    
    return (True, [])


def validar_formato_entrada(data):
    errores = {}
    
    if 'plano1' not in data:
        errores['plano1'] = ['Falta la información del plano 1']
    
    if 'plano2' not in data:
        errores['plano2'] = ['Falta la información del plano 2']
    
    if errores:
        return (False, errores)
    
    valido1, errores1 = validar_plano(data['plano1'])
    if not valido1:
        errores['plano1'] = errores1
    
    valido2, errores2 = validar_plano(data['plano2'])
    if not valido2:
        errores['plano2'] = errores2
    
    if errores:
        return (False, errores)
    
    return (True, {})


def sanitizar_numero(valor, default=0.0):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return default


def limpiar_entrada_plano(datos):
   
    return {
        'a': sanitizar_numero(datos.get('a', 0)),
        'b': sanitizar_numero(datos.get('b', 0)),
        'c': sanitizar_numero(datos.get('c', 0)),
        'd': sanitizar_numero(datos.get('d', 0)),
        'nombre': str(datos.get('nombre', ''))
    }


def parsear_ecuacion_texto(ecuacion_str):
    import re
    from fractions import Fraction
    
    ecuacion = ecuacion_str.replace(' ', '')
    
    if '=' not in ecuacion:
        raise ValueError("La ecuación debe contener el símbolo '='")
    
    partes = ecuacion.split('=')
    if len(partes) != 2:
        raise ValueError("La ecuación debe tener exactamente un signo '='")
    
    izquierda, derecha = partes
    
    coeficientes = {'a': Fraction(0), 'b': Fraction(0), 'c': Fraction(0), 'd': Fraction(0)}
    
    var_map = {'x': 'a', 'y': 'b', 'z': 'c'}
    
    def parsear_lado(texto, multiplicador=1):
        """Parsea un lado de la ecuación y actualiza coeficientes"""
        patron_var = r'([+-]?)(\d+(?:/\d+)?(?:\.\d+)?)?([xyz])'
        matches = re.findall(patron_var, texto.lower())
        
        for signo, coef_str, var in matches:
            if coef_str == '' or coef_str is None:
                coef = Fraction(1)
            elif '/' in coef_str:
                coef = Fraction(coef_str)
            else:
                coef = Fraction(coef_str)
            
            if signo == '-':
                coef = -coef
            
            coeficientes[var_map[var]] += coef * multiplicador
        
        texto_sin_vars = re.sub(r'[+-]?\d*(?:/\d+)?(?:\.\d+)?[xyz]', '', texto.lower())
        
        if texto_sin_vars:
            if texto_sin_vars[0] not in ['+', '-']:
                texto_sin_vars = '+' + texto_sin_vars
            
            patron_num = r'([+-]\d+(?:/\d+)?(?:\.\d+)?)'
            numeros = re.findall(patron_num, texto_sin_vars)
            
            for num in numeros:
                coeficientes['d'] += Fraction(num) * multiplicador
    
    parsear_lado(izquierda, multiplicador=1)
    
    parsear_lado(derecha, multiplicador=-1)
    
    if coeficientes['a'] == 0 and coeficientes['b'] == 0 and coeficientes['c'] == 0:
        raise ValueError('La ecuación debe contener al menos una variable (x, y, o z) con coeficiente no nulo')
    
    return {
        'a': coeficientes['a'],
        'b': coeficientes['b'],
        'c': coeficientes['c'],
        'd': -coeficientes['d']
    }


def ordenar_ecuacion(coeficientes):
    mapeo_posible = {
        'x': ['x', 'a', 'coef_x', 'X'],
        'y': ['y', 'b', 'coef_y', 'Y'],
        'z': ['z', 'c', 'coef_z', 'Z'],
        'd': ['d', 'termino', 'independiente', 'D']
    }
    
    resultado = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    
    for key_estandar, posibles_keys in mapeo_posible.items():
        for posible_key in posibles_keys:
            if posible_key in coeficientes:
                valor = sanitizar_numero(coeficientes[posible_key])
                if key_estandar == 'x':
                    resultado['a'] = valor
                elif key_estandar == 'y':
                    resultado['b'] = valor
                elif key_estandar == 'z':
                    resultado['c'] = valor
                else:
                    resultado['d'] = valor
                break
    
    for key in ['a', 'b', 'c', 'd']:
        if key in coeficientes:
            resultado[key] = sanitizar_numero(coeficientes[key])
    
    return resultado
