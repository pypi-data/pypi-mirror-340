import numpy as np
from scipy.linalg import lu

def eliminacion_gauss(A, b):
    """
    Resuelve Ax = b usando eliminación de Gauss.
    
    Parámetros:
        A: Matriz de coeficientes (lista o array NumPy)
        b: Vector de términos independientes (lista o array NumPy)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).flatten()
    
    n = len(b)
    if A.shape != (n, n):
        raise ValueError("Dimensiones incorrectas: A debe ser cuadrada y coincidir con b")
    
    Ab = np.hstack([A, b.reshape(-1, 1)])
    for i in range(n):
        # Pivoteo parcial para evitar división por cero
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]
        
        if Ab[i, i] == 0:
            raise ValueError("Matriz singular: sistema sin solución única")
            
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
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    
    n = len(b)
    Ab = np.hstack([A, b])
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]
        
        pivot = Ab[i, i]
        if pivot == 0:
            raise ValueError("Matriz singular: sistema sin solución única")
            
        Ab[i] = Ab[i] / pivot
        for j in range(n):
            if i != j:
                Ab[j] -= Ab[j, i] * Ab[i]
    
    return Ab[:, -1].flatten()

def cramer(A, b):
    """
    Resuelve Ax = b usando la regla de Cramer.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("Matriz singular: sistema sin solución única")
    
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
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    
    return x

def jacobi(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Resuelve Ax = b usando el método iterativo de Jacobi.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    x = x0.copy() if x0 is not None else np.zeros(n)
    
    D = np.diag(A)
    if np.any(D == 0):
        raise ValueError("La matriz A tiene ceros en la diagonal")
    
    R = A - np.diagflat(D)
    
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    
    raise ValueError("El método de Jacobi no convergió")

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Resuelve Ax = b usando el método iterativo de Gauss-Seidel.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    x = x0.copy() if x0 is not None else np.zeros(n)
    
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            if A[i, i] == 0:
                raise ValueError("Elemento diagonal cero en A")
                
            x_new[i] = (b[i] - np.dot(A[i, :i], x_new[:i]) - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    
    raise ValueError("El método de Gauss-Seidel no convergió")