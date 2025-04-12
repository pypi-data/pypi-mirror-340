import numpy as np

# Método de Jacobi
def jacobi(A, b, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Jacobi.
    Parámetros:
        A: lista de listas o ndarray (matriz de coeficientes)
        b: lista o ndarray (vector de términos independientes)
        tol: tolerancia para el criterio de convergencia
        max_iter: número máximo de iteraciones
    Retorna:
        x: lista (solución aproximada del sistema)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    # Inicialización del vector solución con ceros
    x = np.zeros_like(b)

    # Diagonal de A y el resto (parte residual R = A - D)
    D = np.diag(A)
    R = A - np.diagflat(D)

    for _ in range(max_iter):
        # Cálculo del nuevo valor de x en esta iteración
        x_new = (b - np.dot(R, x)) / D

        # Verificación de convergencia: norma infinita de la diferencia entre iteraciones
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        
        # Actualizar x para la próxima iteración
        x = x_new

    # Si no converge en el número máximo de iteraciones
    raise ValueError("El método de Jacobi no convergió")


# Método de Gauss-Seidel
def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Gauss-Seidel.
    Parámetros:
        A: lista de listas o ndarray (matriz de coeficientes)
        b: lista o ndarray (vector de términos independientes)
        tol: tolerancia para el criterio de convergencia
        max_iter: número máximo de iteraciones
    Retorna:
        x: lista (solución aproximada del sistema)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Inicialización del vector solución con ceros
    x = np.zeros_like(b)
    n = len(b)

    for _ in range(max_iter):
        x_new = np.copy(x)

        # Iteración sobre cada fila del sistema
        for i in range(n):
            # Suma de los términos ya actualizados y los aún no actualizados
            suma = np.dot(A[i, :i], x_new[:i]) + np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - suma) / A[i, i]

        # Verificación de convergencia
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()

        # Actualizar x para la próxima iteración
        x = x_new

    raise ValueError("El método de Gauss-Seidel no convergió")
