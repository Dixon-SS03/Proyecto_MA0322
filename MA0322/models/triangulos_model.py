import math  # Solo para las funciones trigonométricas permitidas: sin, cos, tan, atan, atan2


class Triangulo:
    """
    Modelo sencillo para manejar triángulos dados 3 puntos en 2D.
    Calcula: lados, ángulos y clasificación por lados y ángulos.
    Implementa métodos matemáticos básicos sin usar funciones prohibidas.
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
    # Métodos matemáticos básicos implementados manualmente
    # -------------------------
    def _raiz_cuadrada(self, n, precision=1e-10):
        """
        Calcula la raíz cuadrada usando el método de Newton-Raphson.
        
        Args:
            n: Número del cual calcular la raíz
            precision: Precisión deseada
            
        Returns:
            Raíz cuadrada de n
        """
        if n < 0:
            raise ValueError("No se puede calcular raíz cuadrada de número negativo")
        if n == 0:
            return 0
        
        # Estimación inicial
        x = n
        
        # Iteración de Newton: x_nuevo = (x + n/x) / 2
        while True:
            x_nuevo = (x + n / x) / 2
            if abs(x_nuevo - x) < precision:
                return x_nuevo
            x = x_nuevo

    def _valor_absoluto(self, x):
        """
        Calcula el valor absoluto de un número.
        
        Args:
            x: Número
            
        Returns:
            |x|
        """
        if x < 0:
            return -x
        return x

    def _potencia(self, base, exponente):
        """
        Calcula base^exponente usando multiplicación iterativa.
        Solo funciona para exponentes enteros positivos.
        
        Args:
            base: Número base
            exponente: Exponente (entero positivo)
            
        Returns:
            base^exponente
        """
        if exponente == 0:
            return 1
        if exponente < 0:
            return 1 / self._potencia(base, -exponente)
        
        resultado = 1
        for _ in range(int(exponente)):
            resultado *= base
        return resultado

    def _grados_a_radianes(self, grados):
        """
        Convierte grados a radianes.
        
        Args:
            grados: Ángulo en grados
            
        Returns:
            Ángulo en radianes
        """
        PI = 3.141592653589793
        return grados * PI / 180

    def _radianes_a_grados(self, radianes):
        """
        Convierte radianes a grados.
        
        Args:
            radianes: Ángulo en radianes
            
        Returns:
            Ángulo en grados
        """
        PI = 3.141592653589793
        return radianes * 180 / PI

    # -------------------------
    # Utilidades internas
    # -------------------------
    def _distancia(self, P, Q):
        """
        Calcula la distancia euclidiana entre dos puntos.
        Usa método propio de raíz cuadrada.
        
        Args:
            P: Punto (x, y)
            Q: Punto (x, y)
            
        Returns:
            Distancia entre P y Q
        """
        dx = Q[0] - P[0]
        dy = Q[1] - P[1]
        
        # Calcular dx² + dy² usando multiplicación
        suma_cuadrados = dx * dx + dy * dy
        
        # Usar nuestra implementación de raíz cuadrada
        dist = self._raiz_cuadrada(suma_cuadrados)
        
        self.pasos.append(f"Distancia entre {P} y {Q}: √(({dx})² + ({dy})²) = √{suma_cuadrados:.4f} = {dist:.4f}")
        return dist

    def _producto_cruz_2d(self, U, V):
        """
        Producto cruz 2D (retorna componente escalar z).
        
        Args:
            U: Vector (x, y)
            V: Vector (x, y)
            
        Returns:
            Componente z del producto cruz
        """
        cross = U[0] * V[1] - U[1] * V[0]
        self.pasos.append(f"Producto cruz 2D {U} × {V} = ({U[0]}·{V[1]}) - ({U[1]}·{V[0]}) = {cross:.4f}")
        return cross

    def _producto_punto(self, u, v):
        """
        Calcula el producto punto entre dos vectores.
        
        Args:
            u: Vector (x, y)
            v: Vector (x, y)
            
        Returns:
            u · v
        """
        return u[0] * v[0] + u[1] * v[1]

    def _angulo(self, u, v):
        """
        Ángulo entre vectores u y v en grados.
        Usa atan2 (función trigonométrica básica permitida).
        
        Args:
            u: Vector (x, y)
            v: Vector (x, y)
            
        Returns:
            Ángulo en grados
        """
        dot = self._producto_punto(u, v)
        cross = self._producto_cruz_2d(u, v)
        
        # atan2 es una función trigonométrica básica permitida
        ang_rad = math.atan2(self._valor_absoluto(cross), dot)
        ang_deg = self._radianes_a_grados(ang_rad)
        
        self.pasos.append(f"Ángulo entre {u} y {v}: atan2(|{cross:.4f}|, {dot:.4f}) = {ang_rad:.4f} rad = {ang_deg:.4f}°")
        return ang_deg

    # -------------------------
    # Funciones principales
    # -------------------------
    def calcular_lados(self):
        """
        Calcula los tres lados del triángulo.
        Convención: a opuesto a A (BC), b opuesto a B (AC), c opuesto a C (AB)
        
        Returns:
            Diccionario con los lados {a, b, c}
        """
        self.pasos.append("\n=== CÁLCULO DE LADOS ===")
        self.lados['a'] = self._distancia(self.B, self.C)  # Lado BC (opuesto a A)
        self.lados['b'] = self._distancia(self.A, self.C)  # Lado AC (opuesto a B)
        self.lados['c'] = self._distancia(self.A, self.B)  # Lado AB (opuesto a C)
        return self.lados

    def calcular_colinealidad(self):
        """
        Verifica si los tres puntos son colineales usando el área del triángulo.
        Si el área es 0 (o muy cercana a 0), los puntos están en línea recta.
        
        Returns:
            True si son colineales, False si forman un triángulo
        """
        self.pasos.append("\n=== VERIFICACIÓN DE COLINEALIDAD ===")
        
        # Vectores desde A hacia B y C
        BA = (self.B[0] - self.A[0], self.B[1] - self.A[1])
        CA = (self.C[0] - self.A[0], self.C[1] - self.A[1])
        
        # Área = 0.5 * |producto cruz|
        producto_cruz = self._producto_cruz_2d(BA, CA)
        area = 0.5 * self._valor_absoluto(producto_cruz)
        
        self.pasos.append(f"Área del triángulo: ½·|{producto_cruz:.4f}| = {area:.4f}")
        
        # Tolerancia para considerar colineales
        self.colineal = area < 1e-9
        
        if self.colineal:
            self.pasos.append("⚠️ Los puntos son colineales, no forman triángulo.")
        else:
            self.pasos.append("✓ Los puntos forman un triángulo válido.")
        
        return self.colineal

    def calcular_angulos(self):
        """
        Calcula los tres ángulos internos del triángulo.
        
        Returns:
            Diccionario con los ángulos {A, B, C} en grados
        """
        self.pasos.append("\n=== CÁLCULO DE ÁNGULOS ===")
        
        # Vectores para calcular ángulos
        # Ángulo A: vectores AB y AC desde A
        AB = (self.B[0] - self.A[0], self.B[1] - self.A[1])
        AC = (self.C[0] - self.A[0], self.C[1] - self.A[1])
        
        # Ángulo B: vectores BA y BC desde B
        BA = (-AB[0], -AB[1])
        BC = (self.C[0] - self.B[0], self.C[1] - self.B[1])
        
        # Ángulo C: vectores CA y CB desde C
        CA = (-AC[0], -AC[1])
        CB = (-BC[0], -BC[1])

        self.pasos.append(f"Vectores desde A: AB={AB}, AC={AC}")
        self.angulos['A'] = self._angulo(AB, AC)
        
        self.pasos.append(f"Vectores desde B: BA={BA}, BC={BC}")
        self.angulos['B'] = self._angulo(BA, BC)
        
        self.pasos.append(f"Vectores desde C: CA={CA}, CB={CB}")
        self.angulos['C'] = self._angulo(CA, CB)

        # Ajuste para que sumen exactamente 180°
        suma = self.angulos['A'] + self.angulos['B'] + self.angulos['C']
        residuo = 180 - suma
        
        if self._valor_absoluto(residuo) > 1e-6:
            ajuste = residuo / 3
            self.angulos['A'] += ajuste
            self.angulos['B'] += ajuste
            self.angulos['C'] += ajuste
            self.pasos.append(f"Ajuste de ángulos para sumar 180°: residuo {residuo:.6f}°, ajuste por ángulo: {ajuste:.6f}°")
        
        suma_final = self.angulos['A'] + self.angulos['B'] + self.angulos['C']
        self.pasos.append(f"Suma de ángulos: {suma_final:.4f}°")
        
        return self.angulos

    def clasificar_lados(self):
        """
        Clasifica el triángulo según la longitud de sus lados.
        
        Returns:
            "equilátero", "isósceles" o "escaleno"
        """
        self.pasos.append("\n=== CLASIFICACIÓN POR LADOS ===")
        
        a, b, c = self.lados['a'], self.lados['b'], self.lados['c']
        tol = 1e-6
        
        self.pasos.append(f"Lado a (BC) = {a:.4f}")
        self.pasos.append(f"Lado b (AC) = {b:.4f}")
        self.pasos.append(f"Lado c (AB) = {c:.4f}")
        
        # Comparar lados con tolerancia
        a_igual_b = self._valor_absoluto(a - b) < tol
        b_igual_c = self._valor_absoluto(b - c) < tol
        a_igual_c = self._valor_absoluto(a - c) < tol
        
        if a_igual_b and b_igual_c:
            tipo = "equilátero"
            self.pasos.append("Los tres lados son iguales → EQUILÁTERO")
        elif a_igual_b or b_igual_c or a_igual_c:
            tipo = "isósceles"
            self.pasos.append("Dos lados son iguales → ISÓSCELES")
        else:
            tipo = "escaleno"
            self.pasos.append("Todos los lados son diferentes → ESCALENO")
        
        return tipo

    def clasificar_angulos(self):
        """
        Clasifica el triángulo según sus ángulos internos.
        
        Returns:
            "rectángulo", "obtusángulo" o "acutángulo"
        """
        self.pasos.append("\n=== CLASIFICACIÓN POR ÁNGULOS ===")
        
        angA = self.angulos['A']
        angB = self.angulos['B']
        angC = self.angulos['C']
        
        self.pasos.append(f"Ángulo A = {angA:.4f}°")
        self.pasos.append(f"Ángulo B = {angB:.4f}°")
        self.pasos.append(f"Ángulo C = {angC:.4f}°")
        
        tol = 1e-6
        
        # Verificar si hay ángulo recto (90°)
        tiene_recto = (
            self._valor_absoluto(angA - 90) < tol or 
            self._valor_absoluto(angB - 90) < tol or 
            self._valor_absoluto(angC - 90) < tol
        )
        
        # Verificar si hay ángulo obtuso (> 90°)
        tiene_obtuso = angA > 90 + tol or angB > 90 + tol or angC > 90 + tol
        
        if tiene_recto:
            tipo = "rectángulo"
            self.pasos.append("Tiene un ángulo de 90° → RECTÁNGULO")
        elif tiene_obtuso:
            tipo = "obtusángulo"
            self.pasos.append("Tiene un ángulo mayor a 90° → OBTUSÁNGULO")
        else:
            tipo = "acutángulo"
            self.pasos.append("Todos los ángulos son menores a 90° → ACUTÁNGULO")
        
        return tipo

    # -------------------------
    # Función que orquesta todo
    # -------------------------
    def analizar(self):
        """
        Realiza el análisis completo del triángulo.
        
        Returns:
            Diccionario con toda la información del triángulo
        """
        resultado = {
            "puntos": {"A": self.A, "B": self.B, "C": self.C}, 
            "pasos": []
        }

        # Verificar puntos coincidentes
        if self.A == self.B or self.A == self.C or self.B == self.C:
            resultado["mensaje"] = "⚠️ Dos o más puntos coinciden, no se puede formar triángulo."
            resultado["colineal"] = True
            resultado["pasos"] = ["ERROR: Puntos coincidentes detectados."]
            return resultado

        # Calcular lados
        self.calcular_lados()
        
        # Verificar colinealidad
        self.calcular_colinealidad()
        if self.colineal:
            resultado["colineal"] = True
            resultado["pasos"] = self.pasos
            resultado["mensaje"] = "⚠️ Los puntos son colineales, no forman un triángulo."
            return resultado

        # Calcular ángulos
        self.calcular_angulos()
        
        # Clasificar
        resultado["clasificacion_lados"] = self.clasificar_lados()
        resultado["clasificacion_angulos"] = self.clasificar_angulos()

        # Agregar medidas
        resultado["lados"] = self.lados
        resultado["angulos"] = self.angulos
        resultado["colineal"] = self.colineal
        resultado["pasos"] = self.pasos
        
        return resultado
