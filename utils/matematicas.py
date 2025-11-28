
import math
from fractions import Fraction


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


def gauss_jordan(matriz, pasos=None):
   
    if pasos is None:
        pasos = []
    
    m = [[Fraction(elemento) for elemento in fila] for fila in matriz]
    n_filas = len(m)
    n_cols = len(m[0]) if n_filas > 0 else 0
    
    pasos.append({
        'descripcion': 'Matriz inicial',
        'matriz': [fila[:] for fila in m]
    })
    
    pivote_fila = 0
    
    for col in range(min(n_filas, n_cols - 1)): 
        max_fila = pivote_fila
        max_val = abs(m[pivote_fila][col])
        
        for fila in range(pivote_fila + 1, n_filas):
            if abs(m[fila][col]) > max_val:
                max_val = abs(m[fila][col])
                max_fila = fila
        
        if m[max_fila][col] == 0:
            continue
        
        if max_fila != pivote_fila:
            m[pivote_fila], m[max_fila] = m[max_fila], m[pivote_fila]
            pasos.append({
                'descripcion': f'Intercambiar F{pivote_fila+1} ↔ F{max_fila+1}',
                'matriz': [fila[:] for fila in m]
            })
        
        pivote = m[pivote_fila][col]
        if pivote != 1:  
            for j in range(n_cols):
                m[pivote_fila][j] /= pivote
            pasos.append({
                'descripcion': f'F{pivote_fila+1} = F{pivote_fila+1} / {formatear_numero(pivote)}',
                'matriz': [fila[:] for fila in m]
            })
        
        for fila in range(n_filas):
            if fila != pivote_fila:
                factor = m[fila][col]
                if factor != 0:  
                    for j in range(n_cols):
                        m[fila][j] -= factor * m[pivote_fila][j]
                    
                    if factor > 0:
                        pasos.append({
                            'descripcion': f'F{fila+1} = F{fila+1} - {formatear_numero(factor)} × F{pivote_fila+1}',
                            'matriz': [fila[:] for fila in m]
                        })
                    else:
                        pasos.append({
                            'descripcion': f'F{fila+1} = F{fila+1} + {formatear_numero(abs(factor))} × F{pivote_fila+1}',
                            'matriz': [fila[:] for fila in m]
                        })
        
        pivote_fila += 1
        if pivote_fila >= n_filas:
            break
    
    rango = 0
    for fila in m:
        if any(val != 0 for val in fila[:-1]):  
            rango += 1
    
    pasos.append({
        'descripcion': f'Matriz reducida (Rango = {rango})',
        'matriz': [fila[:] for fila in m]
    })
    
    return m, rango, pasos


def determinante_3x3(matriz):
   
    if len(matriz) != 3 or any(len(fila) != 3 for fila in matriz):
        raise ValueError("La matriz debe ser 3x3")
    
    a = matriz[0][0]
    b = matriz[0][1]
    c = matriz[0][2]
    d = matriz[1][0]
    e = matriz[1][1]
    f = matriz[1][2]
    g = matriz[2][0]
    h = matriz[2][1]
    i = matriz[2][2]
    
    det = a*e*i + b*f*g + c*d*h - c*e*g - a*f*h - b*d*i
    
    return det


def distancia_punto_plano(punto, plano):
 
    x, y, z = punto
    
    numerador = abs(Fraction(plano.a) * Fraction(x) + Fraction(plano.b) * Fraction(y) + 
                   Fraction(plano.c) * Fraction(z) - Fraction(plano.d))
    
    suma_cuadrados = Fraction(plano.a)**2 + Fraction(plano.b)**2 + Fraction(plano.c)**2
    
    if suma_cuadrados == 0:
        raise ValueError("El plano no es válido (coeficientes a, b, c son todos cero)")
    
    raiz_entera = int(suma_cuadrados ** 0.5)
    if raiz_entera * raiz_entera == suma_cuadrados:
        return numerador / raiz_entera
    else:
        if numerador == 0:
            return Fraction(0)
        elif numerador == 1:
            return f"√{suma_cuadrados}/{suma_cuadrados}" if suma_cuadrados != 1 else Fraction(1)
        else:
            return f"{numerador}/√{suma_cuadrados}"


def distancia_entre_planos_paralelos(plano1, plano2):
   
    
    diferencia_d = abs(Fraction(plano2.d) - Fraction(plano1.d))
    suma_cuadrados = Fraction(plano1.a)**2 + Fraction(plano1.b)**2 + Fraction(plano1.c)**2
    
    if suma_cuadrados == 0:
        raise ValueError("El plano no es válido")
    
    raiz_entera = int(suma_cuadrados ** 0.5)
    if raiz_entera * raiz_entera == suma_cuadrados:
        return diferencia_d / raiz_entera
    else:
        if diferencia_d == 0:
            return Fraction(0)
        elif diferencia_d == 1:
            return f"1/√{suma_cuadrados}"
        else:
            return f"{diferencia_d}/√{suma_cuadrados}"


def son_paralelos(plano1, plano2):
  
    a1, b1, c1 = Fraction(plano1.a), Fraction(plano1.b), Fraction(plano1.c)
    a2, b2, c2 = Fraction(plano2.a), Fraction(plano2.b), Fraction(plano2.c)
    
    k = None
    
    if a2 != 0:
        k = a1 / a2
    elif b2 != 0:
        k = b1 / b2
    elif c2 != 0:
        k = c1 / c2
    else:
        return False
    
    if a2 != 0:
        if a1 != k * a2:
            return False
    else:
        if a1 != 0:
            return False
    
    if b2 != 0:
        if b1 != k * b2:
            return False
    else:
        if b1 != 0:
            return False
    
    if c2 != 0:
        if c1 != k * c2:
            return False
    else:
        if c1 != 0:
            return False
    
    return True


def son_coincidentes(plano1, plano2):
   
    if not son_paralelos(plano1, plano2):
        return False
    
    a1, b1, c1, d1 = Fraction(plano1.a), Fraction(plano1.b), Fraction(plano1.c), Fraction(plano1.d)
    a2, b2, c2, d2 = Fraction(plano2.a), Fraction(plano2.b), Fraction(plano2.c), Fraction(plano2.d)
    
    k = None
    if a2 != 0:
        k = a1 / a2
    elif b2 != 0:
        k = b1 / b2
    elif c2 != 0:
        k = c1 / c2
    
    if k is None:
        return False
    
    return d1 == k * d2


def producto_vectorial(v1, v2):
   
    x = v1[1] * v2[2] - v1[2] * v2[1]
    y = v1[2] * v2[0] - v1[0] * v2[2]
    z = v1[0] * v2[1] - v1[1] * v2[0]
    
    return (x, y, z)


def normalizar_vector(v):
    v_frac = [Fraction(x) for x in v]
    suma_cuadrados = v_frac[0]**2 + v_frac[1]**2 + v_frac[2]**2
    
    if suma_cuadrados == 0:
        return (Fraction(0), Fraction(0), Fraction(0))
    
    raiz_entera = int(suma_cuadrados ** 0.5)
    if raiz_entera * raiz_entera == suma_cuadrados:
        return tuple(x / raiz_entera for x in v_frac)
    else:
        return tuple(f"{x}/√{suma_cuadrados}" if x != 0 else "0" for x in v_frac)
