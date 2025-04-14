import numpy as np

def resolver_biseccion(f, a, b, tol=1e-10, max_iter=1000):
    """
    Encuentra una raíz de f en el intervalo [a, b] usando el método de bisección.
    """
    a = float(a)
    b = float(b)
    
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a)/2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    raise ValueError("El método de bisección no convergió")