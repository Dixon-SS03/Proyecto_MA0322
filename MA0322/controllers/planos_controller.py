import sys
import os
from fractions import Fraction

# Agregar el directorio padre al path para los imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.plano import Plano
from utils.matematicas import (
    gauss_jordan, 
    son_paralelos, 
    son_coincidentes,
    distancia_entre_planos_paralelos,
    producto_vectorial
)
from utils.validaciones import validar_formato_entrada, limpiar_entrada_plano, ordenar_ecuacion


def formatear_numero(num):
    if isinstance(num, Fraction):
        if num.denominator == 1:
            return str(num.numerator)
        else:
            return f"{num.numerator}/{num.denominator}"
    elif isinstance(num, (int, float)):
        frac = Fraction(num).limit_denominator(10000)
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    return str(num)


def calcular_interseccion_planos(data):
  
    es_valido, errores = validar_formato_entrada(data)
    if not es_valido:
        return {
            'exito': False,
            'error': 'Datos de entrada inválidos',
            'detalles': errores
        }
    
    datos_p1 = ordenar_ecuacion(data['plano1'])
    datos_p2 = ordenar_ecuacion(data['plano2'])
    
    datos_p1 = limpiar_entrada_plano(datos_p1)
    datos_p2 = limpiar_entrada_plano(datos_p2)
    
    datos_p1['nombre'] = 'Plano 1'
    datos_p2['nombre'] = 'Plano 2'
    
    plano1 = Plano.from_dict(datos_p1)
    plano2 = Plano.from_dict(datos_p2)
    
    if not plano1.es_valido():
        return {
            'exito': False,
            'error': 'El Plano 1 no es válido (coeficientes a, b, c son todos cero)'
        }
    
    if not plano2.es_valido():
        return {
            'exito': False,
            'error': 'El Plano 2 no es válido (coeficientes a, b, c son todos cero)'
        }
    
    resultado = {
        'exito': True,
        'plano1': plano1.to_dict(),
        'plano2': plano2.to_dict()
    }
    
    if son_coincidentes(plano1, plano2):
        resultado['tipo_interseccion'] = 'coincidentes'
        resultado['descripcion'] = 'Los planos son coincidentes (el mismo plano)'
        resultado['mensaje'] = 'Los planos son idénticos, por lo tanto se intersecan en todos sus puntos.'
        return resultado
    
    if son_paralelos(plano1, plano2):
        resultado['tipo_interseccion'] = 'paralelos'
        resultado['descripcion'] = 'Los planos son paralelos y no se intersecan'
        
        distancia = distancia_entre_planos_paralelos(plano1, plano2)
        resultado['distancia'] = str(distancia) if not isinstance(distancia, Fraction) else formatear_numero(distancia)
        
        dist_str = resultado['distancia']
        resultado['mensaje'] = f'Los planos son paralelos. La distancia entre ellos es: {dist_str}'
        
        d1_fmt = formatear_numero(plano1.d)
        d2_fmt = formatear_numero(plano2.d)
        a_fmt = formatear_numero(plano1.a)
        b_fmt = formatear_numero(plano1.b)
        c_fmt = formatear_numero(plano1.c)
        
        resultado['justificacion'] = (
            f"Los vectores normales son proporcionales:\n"
            f"N₁ = ({a_fmt}, {b_fmt}, {c_fmt})\n"
            f"N₂ = ({formatear_numero(plano2.a)}, {formatear_numero(plano2.b)}, {formatear_numero(plano2.c)})\n\n"
            f"Fórmula de distancia entre planos paralelos:\n"
            f"d = |d₂ - d₁| / √(a² + b² + c²)\n"
            f"d = |{d2_fmt} - {d1_fmt}| / √({a_fmt}² + {b_fmt}² + {c_fmt}²)\n"
            f"d = {dist_str}"
        )
        
        return resultado
    
    resultado['tipo_interseccion'] = 'recta'
    resultado['descripcion'] = 'Los planos se intersecan en una recta'
    
    pasos = []
    matriz_aumentada = [
        [plano1.a, plano1.b, plano1.c, plano1.d],
        [plano2.a, plano2.b, plano2.c, plano2.d]
    ]
    
    matriz_reducida, rango, pasos_gj = gauss_jordan(matriz_aumentada, pasos)
    
    pasos_formateados = []
    for paso in pasos_gj:
        pasos_formateados.append({
            'descripcion': paso['descripcion'],
            'matriz': [[formatear_numero(elem) for elem in fila] for fila in paso['matriz']]
        })
    
    resultado['gauss_jordan'] = {
        'pasos': pasos_formateados,
        'matriz_final': [[formatear_numero(elem) for elem in fila] for fila in matriz_reducida],
        'rango': rango
    }
    
    ecuacion_parametrica = obtener_ecuacion_parametrica(matriz_reducida, plano1, plano2)
    resultado['ecuacion_parametrica'] = ecuacion_parametrica
    
    resultado['mensaje'] = (
        f"Los planos se intersecan en una recta.\n"
        f"Ecuación paramétrica:\n"
        f"x = {ecuacion_parametrica['x']}\n"
        f"y = {ecuacion_parametrica['y']}\n"
        f"z = {ecuacion_parametrica['z']}"
    )
    
    return resultado


def obtener_ecuacion_parametrica(matriz_reducida, plano1, plano2):

    n1 = (plano1.a, plano1.b, plano1.c)
    n2 = (plano2.a, plano2.b, plano2.c)
    v = producto_vectorial(n1, n2)
    
    punto = encontrar_punto_en_recta(matriz_reducida)
    
    punto_frac = [Fraction(p).limit_denominator(1000) for p in punto]
    v_frac = [Fraction(vi).limit_denominator(1000) for vi in v]
    
    def construir_ecuacion(p, v):
        p_str = formatear_numero(p)
        v_str = formatear_numero(v)
        
        if v < 0:
            v_str_abs = formatear_numero(abs(v))
            if p == 0:
                return f"-{v_str_abs}t"
            else:
                return f"{p_str} - {v_str_abs}t"
        elif v == 0:
            return p_str
        elif p == 0:
            return f"{v_str}t"
        else:
            return f"{p_str} + {v_str}t"
    
    return {
        'punto': [formatear_numero(p) for p in punto_frac],
        'vector_direccion': [formatear_numero(vi) for vi in v_frac],
        'x': construir_ecuacion(punto_frac[0], v_frac[0]),
        'y': construir_ecuacion(punto_frac[1], v_frac[1]),
        'z': construir_ecuacion(punto_frac[2], v_frac[2])
    }


def encontrar_punto_en_recta(matriz):
   
    
    if len(matriz) < 2:
        return (Fraction(0), Fraction(0), Fraction(0))
    
    z = Fraction(0)
    
    a1, b1, c1, d1 = matriz[0][0], matriz[0][1], matriz[0][2], matriz[0][3]
    a2, b2, c2, d2 = matriz[1][0], matriz[1][1], matriz[1][2], matriz[1][3]
    
    
    d1_ajustado = d1 - c1 * z
    d2_ajustado = d2 - c2 * z
    
    det = a1 * b2 - a2 * b1
    
    if det != 0:
        x = (d1_ajustado * b2 - d2_ajustado * b1) / det
        y = (a1 * d2_ajustado - a2 * d1_ajustado) / det
        return (x, y, z)
    else:
        y = Fraction(0)
        if a1 != 0:
            x = (d1 - b1 * y - c1 * z) / a1
            return (x, y, z)
        elif a2 != 0:
            x = (d2 - b2 * y - c2 * z) / a2
            return (x, y, z)
        else:
            x = Fraction(0)
            if b1 != 0:
                y = (d1 - a1 * x - c1 * z) / b1
                return (x, y, z)
            elif b2 != 0:
                y = (d2 - a2 * x - c2 * z) / b2
                return (x, y, z)
    
    return (Fraction(0), Fraction(0), Fraction(0))
