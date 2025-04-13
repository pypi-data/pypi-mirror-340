# MM22025UNO

**MM22025UNO** es una librería en Python para resolver sistemas de ecuaciones **lineales y no lineales** mediante distintos métodos numéricos clásicos.

## 📦 Instalación

```bash
pip install MM22025UNO
```

> Asegúrate de tener `numpy` y `scipy` instalados. Si no, se instalarán automáticamente con la librería.

---

## 📘 Métodos implementados

### Métodos lineales:
- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Método de Jacobi
- Método de Gauss-Seidel

### Métodos no lineales:
- Método de Bisección

---

## 📌 Ejemplos por método

### 🔹 Eliminación de Gauss

```python
from MM22025UNO.lineales import eliminacion_gauss

A = [[2, 1], [1, 3]]
b = [8, 13]
sol = eliminacion_gauss(A, b)
print(sol)
```

---

### 🔹 Gauss-Jordan

```python
from MM22025UNO.lineales import gauss_jordan

A = [[2, 1], [1, 3]]
b = [8, 13]
sol = gauss_jordan(A, b)
print(sol)
```

---

### 🔹 Cramer

```python
from MM22025UNO.lineales import cramer

A = [[2, 1], [1, 3]]
b = [8, 13]
sol = cramer(A, b)
print(sol)
```

---

### 🔹 Descomposición LU

```python
from MM22025UNO.lineales import descomposicion_lu

A = [[2, 1], [1, 3]]
b = [8, 13]
sol = descomposicion_lu(A, b)
print(sol)
```

---

### 🔹 Jacobi

```python
from MM22025UNO.lineales import jacobi

A = [[4, 1], [2, 3]]
b = [1, 2]
x0 = [0, 0]
sol = jacobi(A, b, x0)
print(sol)
```

---

### 🔹 Gauss-Seidel

```python
from MM22025UNO.lineales import gauss_seidel

A = [[4, 1], [2, 3]]
b = [1, 2]
x0 = [0, 0]
sol = gauss_seidel(A, b, x0)
print(sol)
```

---

### 🔹 Bisección

```python
from MM22025UNO.no_lineales import resolver_biseccion

f = lambda x: x**3 - x - 2
raiz = resolver_biseccion(f, 1, 2)
print(raiz)
```

---

## 📤 Licencia

Este proyecto está licenciado bajo los términos de la **MIT License**.