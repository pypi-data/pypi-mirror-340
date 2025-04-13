import numpy as np
from scipy.optimize import fsolve

def jacobi(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Resuelve Ax = b usando el método iterativo de Jacobi.
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    D = np.diag(A)
    R = A - np.diagflat(D)
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("El método de Jacobi no convergió.")

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Resuelve Ax = b usando el método iterativo de Gauss-Seidel.
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("El método de Gauss-Seidel no convergió.")

def biseccion(f, a, b, tol=1e-10, max_iter=1000):
    """
    Encuentra una raíz de f en el intervalo [a, b] usando el método de bisección.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    raise ValueError("El método de bisección no convergió.")