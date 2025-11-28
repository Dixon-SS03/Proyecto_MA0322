import math

class Triangulo:
    """
    Modelo sencillo para manejar triángulos dados 3 puntos en 2D.
    Calcula: lados, ángulos y clasificación por lados y ángulos.
    """

    def __init__(self, A, B, C):
        self.A = tuple(A)
        self.B = tuple(B)
        self.C = tuple(C)
        self.lados = {}      # a, b, c
        self.angulos = {}    # A, B, C
        self.colineal = False
        self.pasos = []

    # -------------------------
    # Utilidades internas
    # -------------------------
    def _distancia(self, P, Q):
        dx = Q[0] - P[0]
        dy = Q[1] - P[1]
        dist = math.sqrt(dx*dx + dy*dy)
        self.pasos.append(f"Distancia entre {P} y {Q}: sqrt(({dx})^2 + ({dy})^2) = {dist:.4f}")
        return dist

    def _producto_cruz_2d(self, U, V):
        # Producto cruz 2D (scalar z)
        cross = U[0]*V[1] - U[1]*V[0]
        self.pasos.append(f"Producto cruz 2D {U} x {V} = {cross:.4f}")
        return cross

    def _angulo(self, u, v):
        # Ángulo entre vectores u y v en grados
        dot = u[0]*v[0] + u[1]*v[1]
        cross = self._producto_cruz_2d(u, v)
        ang_rad = math.atan2(abs(cross), dot)
        ang_deg = math.degrees(ang_rad)
        self.pasos.append(f"Ángulo entre {u} y {v}: {ang_deg:.4f}°")
        return ang_deg

    # -------------------------
    # Funciones principales
    # -------------------------
    def calcular_lados(self):
        # Convención: a opuesto a A (BC), b opuesto a B (AC), c opuesto a C (AB)
        self.lados['a'] = self._distancia(self.B, self.C)
        self.lados['b'] = self._distancia(self.A, self.C)
        self.lados['c'] = self._distancia(self.A, self.B)
        return self.lados

    def calcular_colinealidad(self):
        # Usamos área = 0.5*| (B-A)x(C-A) |
        BA = (self.B[0]-self.A[0], self.B[1]-self.A[1])
        CA = (self.C[0]-self.A[0], self.C[1]-self.A[1])
        area = 0.5 * abs(self._producto_cruz_2d(BA, CA))
        self.pasos.append(f"Área del triángulo: {area:.4f}")
        self.colineal = area < 1e-9
        if self.colineal:
            self.pasos.append("Los puntos son colineales, no forman triángulo.")
        else:
            self.pasos.append("Los puntos forman un triángulo.")
        return self.colineal

    def calcular_angulos(self):
        # Vectores para ángulos
        AB = (self.B[0]-self.A[0], self.B[1]-self.A[1])
        AC = (self.C[0]-self.A[0], self.C[1]-self.A[1])
        BA = (-AB[0], -AB[1])
        BC = (self.C[0]-self.B[0], self.C[1]-self.B[1])
        CA = (-AC[0], -AC[1])
        CB = (-BC[0], -BC[1])

        self.angulos['A'] = self._angulo(AB, AC)
        self.angulos['B'] = self._angulo(BA, BC)
        self.angulos['C'] = self._angulo(CA, CB)

        # Ajuste simple para que sumen 180°
        suma = sum(self.angulos.values())
        residuo = 180 - suma
        if abs(residuo) > 1e-6:
            for k in self.angulos:
                self.angulos[k] += residuo/3
            self.pasos.append(f"Ajuste de ángulos para sumar 180°: residuo {residuo:.4f}")
        return self.angulos

    def clasificar_lados(self):
        a, b, c = self.lados['a'], self.lados['b'], self.lados['c']
        tol = 1e-6
        if abs(a-b) < tol and abs(b-c) < tol:
            tipo = "equilátero"
        elif abs(a-b) < tol or abs(b-c) < tol or abs(a-c) < tol:
            tipo = "isósceles"
        else:
            tipo = "escaleno"
        self.pasos.append(f"Clasificación por lados: {tipo}")
        return tipo

    def clasificar_angulos(self):
        angs = self.angulos.values()
        tol = 1e-6
        recto = any(abs(a-90) < tol for a in angs)
        obtuso = any(a > 90+tol for a in angs)
        if recto:
            tipo = "rectángulo"
        elif obtuso:
            tipo = "obtusángulo"
        else:
            tipo = "acutángulo"
        self.pasos.append(f"Clasificación por ángulos: {tipo}")
        return tipo

    # -------------------------
    # Función que orquesta todo
    # -------------------------
    def analizar(self):
        resultado = {"puntos": {"A": self.A, "B": self.B, "C": self.C}, "pasos": []}

        if self.A == self.B or self.A == self.C or self.B == self.C:
            resultado["mensaje"] = "Dos o más puntos coinciden, no se puede formar triángulo."
            resultado["colineal"] = True
            return resultado

        self.calcular_lados()
        self.calcular_colinealidad()
        if self.colineal:
            resultado["colineal"] = True
            resultado["pasos"] = self.pasos
            resultado["mensaje"] = "Puntos colineales."
            return resultado

        self.calcular_angulos()
        resultado["clasificacion_lados"] = self.clasificar_lados()
        resultado["clasificacion_angulos"] = self.clasificar_angulos()

        resultado["lados"] = self.lados
        resultado["angulos"] = self.angulos
        resultado["colineal"] = self.colineal
        resultado["pasos"] = self.pasos
        return resultado
