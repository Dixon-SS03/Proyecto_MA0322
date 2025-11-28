
from fractions import Fraction


def formatear_coeficiente(coef):
    if isinstance(coef, Fraction):
        if coef.denominator == 1:
            return str(coef.numerator)
        else:
            return f"{coef.numerator}/{coef.denominator}"
    elif isinstance(coef, (int, float)):
        frac = Fraction(coef).limit_denominator(10000)
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    return str(coef)


class Plano:
    def __init__(self, a=0, b=0, c=0, d=0, nombre=""):
     
        self.a = Fraction(a) if not isinstance(a, Fraction) else a
        self.b = Fraction(b) if not isinstance(b, Fraction) else b
        self.c = Fraction(c) if not isinstance(c, Fraction) else c
        self.d = Fraction(d) if not isinstance(d, Fraction) else d
        self.nombre = nombre
    
    def to_dict(self):
   
        return {
            'a': formatear_coeficiente(self.a),
            'b': formatear_coeficiente(self.b),
            'c': formatear_coeficiente(self.c),
            'd': formatear_coeficiente(self.d),
            'nombre': self.nombre,
            'ecuacion': self.get_ecuacion_str()
        }
    
    @classmethod
    def from_dict(cls, data):
      
        return cls(
            a=data.get('a', 0),
            b=data.get('b', 0),
            c=data.get('c', 0),
            d=data.get('d', 0),
            nombre=data.get('nombre', '')
        )
    
    def es_valido(self):
       
        return not (self.a == 0 and self.b == 0 and self.c == 0)
    
    def get_ecuacion_str(self):
        
        partes = []
        
        if self.a != 0:
            a_fmt = formatear_coeficiente(self.a)
            if self.a == 1:
                partes.append("x")
            elif self.a == -1:
                partes.append("-x")
            else:
                partes.append(f"{a_fmt}x")
        
        if self.b != 0:
            b_fmt = formatear_coeficiente(self.b)
            if self.b == 1:
                partes.append("+ y" if partes else "y")
            elif self.b == -1:
                partes.append("- y")
            elif self.b > 0 and partes:
                partes.append(f"+ {b_fmt}y")
            else:
                partes.append(f"{b_fmt}y")
        
        if self.c != 0:
            c_fmt = formatear_coeficiente(self.c)
            if self.c == 1:
                partes.append("+ z" if partes else "z")
            elif self.c == -1:
                partes.append("- z")
            elif self.c > 0 and partes:
                partes.append(f"+ {c_fmt}z")
            else:
                partes.append(f"{c_fmt}z")
        
        ecuacion = " ".join(partes) if partes else "0"
        d_fmt = formatear_coeficiente(self.d)
        return f"{ecuacion} = {d_fmt}"
    
    def get_vector_normal(self):
       
        return (self.a, self.b, self.c)
    
    def evaluar_punto(self, x, y, z):
      
        return self.a * x + self.b * y + self.c * z - self.d
    
    @classmethod
    def from_equation_any_order(cls, coeficientes, nombre=""):
        
        a = coeficientes.get('x', 0) or coeficientes.get('a', 0)
        b = coeficientes.get('y', 0) or coeficientes.get('b', 0)
        c = coeficientes.get('z', 0) or coeficientes.get('c', 0)
        d = coeficientes.get('d', 0)
        
        return cls(a=a, b=b, c=c, d=d, nombre=nombre)
    
    def normalizar(self):
       
        divisor = None
        if self.a != 0:
            divisor = self.a
        elif self.b != 0:
            divisor = self.b
        elif self.c != 0:
            divisor = self.c
        
        if divisor is None or divisor == 0:
            return Plano(self.a, self.b, self.c, self.d, self.nombre)
        
        return Plano(
            a=self.a / divisor,
            b=self.b / divisor,
            c=self.c / divisor,
            d=self.d / divisor,
            nombre=self.nombre
        )
