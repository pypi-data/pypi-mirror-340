
import numpy as np
from scipy.linalg import lu_factor, lu_solve

def eliminacion_gauss(A, b):
    A = A.astype(float)
    b = b.astype(float)
    n = len(b)
    for k in range(n - 1):
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
    return x

def gauss_jordan(A, b):
    A = A.astype(float)
    b = b.astype(float).reshape(-1, 1)
    Ab = np.hstack([A, b])
    n = len(b)
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[i] * Ab[j, i]
    return Ab[:, -1]

def cramer(A, b):
    from numpy.linalg import det
    n = len(b)
    detA = det(A)
    if detA == 0:
        raise ValueError("El sistema no tiene solución única")
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = det(Ai) / detA
    return x

def descomposicion_lu(A, b):
    lu, piv = lu_factor(A)
    return lu_solve((lu, piv), b)

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s) / A[i, i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0.copy()
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x

def biseccion(f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c

# Ejemplos de uso
if __name__ == "__main__":
    A = np.array([[2.0, 1.0], [5.0, 7.0]])
    b = np.array([11.0, 13.0])
    print("Gauss:", eliminacion_gauss(A.copy(), b.copy()))
    print("Gauss-Jordan:", gauss_jordan(A.copy(), b.copy()))
    print("Cramer:", cramer(A.copy(), b.copy()))
    print("LU:", descomposicion_lu(A.copy(), b.copy()))
    print("Jacobi:", jacobi(A.copy(), b.copy()))
    print("Gauss-Seidel:", gauss_seidel(A.copy(), b.copy()))
    raiz = biseccion(lambda x: x**2 - 4, 0, 3)
    print("Bisección (raíz de x^2 - 4):", raiz)
