import numpy as np
class Fraccion:
    def __init__(self, numerador, denominador=1):
        if denominador == 0:
            raise ValueError("El denominador no puede ser cero")
        self.n = numerador.numerator
        self.d = numerador.denominator * denominador.numerator
        if self.d < 0:
            self.n = -self.n
            self.d = -self.d
        self.simplificar()
    
    def simplificar(self):
        gcd = np.gcd(self.n, self.d)
        self.n //= gcd
        self.d //= gcd
    
    def __add__(self, otro):
        if isinstance(otro, int):
            otro = Fraccion(otro)
        return Fraccion(self.n * otro.d + otro.n * self.d, self.d * otro.d)
    
    def __sub__(self, otro):
        return Fraccion(self.n * otro.d - otro.n * self.d, self.d * otro.d)
    
    def __mul__(self, otro):
        if isinstance(otro, int):
            otro = Fraccion(otro)
        return Fraccion(self.n * otro.n, self.d * otro.d)
    
    def __truediv__(self, otro):
        if isinstance(otro, int):
            otro = Fraccion(otro)
        return Fraccion(self.n * otro.d, self.d * otro.n)
    
    def __neg__(self):
        return Fraccion(-self.n, self.d)
    
    def __repr__(self):
        return f"{self.n}/{self.d}" if self.d != 1 else str(self.n)