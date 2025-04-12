import numpy as np
from scipy.linalg import lu
from numpy import linalg

# Método de Eliminación de Gauss
def gauss_elimination(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Eliminación de Gauss.
    Parámetros:
        A: lista de listas (matriz de coeficientes)
        b: lista (vector de términos independientes)
    Retorna:
        x: lista (solución del sistema)
    """
    n = len(A)
    
    # Se forma la matriz aumentada A|b
    for i in range(n):
        A[i] = A[i] + [b[i]]

    # Proceso de eliminación hacia adelante
    for i in range(n):
        # Selecciona la fila con el mayor valor absoluto en la columna actual
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]  # Intercambio de filas
        
        # Eliminación de elementos por debajo del pivote
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n + 1):
                A[j][k] -= factor * A[i][k]

    # Sustitución hacia atrás
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (A[i][n] - suma) / A[i][i]
    return x


# Método de Gauss-Jordan
def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Gauss-Jordan.
    Parámetros:
        A: lista de listas (matriz de coeficientes)
        b: lista (vector de términos independientes)
    Retorna:
        x: lista (solución del sistema)
    """
    n = len(A)
    # Matriz aumentada A|b
    M = [A[i] + [b[i]] for i in range(n)]

    # Proceso de reducción por filas
    for i in range(n):
        # Selección del pivote máximo
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]

        # Normalización del pivote
        pivot = M[i][i]
        M[i] = [x / pivot for x in M[i]]

        # Eliminación en las demás filas
        for j in range(n):
            if i != j:
                factor = M[j][i]
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]

    # Extracción de la solución
    return [M[i][-1] for i in range(n)]


# Regla de Cramer
def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la Regla de Cramer.
    Parámetros:
        A: lista de listas o ndarray (matriz de coeficientes)
        b: lista o ndarray (vector de términos independientes)
    Retorna:
        x: lista (solución del sistema)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    det_A = linalg.det(A)

    if det_A == 0:
        raise ValueError("El sistema no tiene solución única (determinante es 0)")

    n = len(b)
    x = []
    # Se reemplaza cada columna de A por el vector b para calcular los determinantes individuales
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x.append(linalg.det(Ai) / det_A)
    return [float(xi) for xi in x]


# Descomposición LU
def lu_decomposition(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando descomposición LU.
    Parámetros:
        A: lista de listas o ndarray (matriz de coeficientes)
        b: lista o ndarray (vector de términos independientes)
    Retorna:
        x: lista (solución del sistema)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Descomposición de A en P, L, U (PA = LU)
    P, L, U = lu(A)
    
    # Se resuelve Ly = Pb usando sustitución hacia adelante
    Pb = P @ b
    y = np.zeros_like(b)
    for i in range(len(y)):
        y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

    # Se resuelve Ux = y usando sustitución hacia atrás
    x = np.zeros_like(y)
    for i in reversed(range(len(y))):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

    return x.tolist()
