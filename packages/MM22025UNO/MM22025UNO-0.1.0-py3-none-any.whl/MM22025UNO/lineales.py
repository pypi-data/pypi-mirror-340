import numpy as np
from scipy.linalg import lu

def eliminacion_gauss(A, b):
    """
    Resuelve Ax = b usando eliminación de Gauss.
    """
    n = len(b)
    Ab = np.hstack([A, b.reshape(-1, 1)])
    for i in range(n):
        for j in range(i+1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    return x

def gauss_jordan(A, b):
    """
    Resuelve Ax = b usando el método de Gauss-Jordan.
    """
    n = len(b)
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1)])
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] -= Ab[j, i] * Ab[i]
    return Ab[:, -1]

def cramer(A, b):
    """
    Resuelve Ax = b usando la regla de Cramer.
    """
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El determinante de A es cero; el sistema no tiene solución única.")
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    return x

def descomposicion_lu(A, b):
    """
    Resuelve Ax = b usando descomposición LU.
    """
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x