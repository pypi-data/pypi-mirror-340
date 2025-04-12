import numpy as np

# Método de Bisección
def biseccion(f, a, b, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] utilizando el método de bisección.
    
    Parámetros:
        f: función (la función para la cual se busca una raíz)
        a: float (extremo izquierdo del intervalo)
        b: float (extremo derecho del intervalo)
        tol: float (tolerancia para el criterio de parada)
        max_iter: int (número máximo de iteraciones)
    
    Retorna:
        Una aproximación de la raíz de la función f.
    """
    # Comprobación inicial: f(a) y f(b) deben tener signos opuestos
    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo [a, b] no es válido. f(a) y f(b) deben tener signos opuestos.")

    for _ in range(max_iter):
        # Punto medio del intervalo
        c = (a + b) / 2.0

        # Si la función en c es suficientemente cercana a cero o el intervalo es suficientemente pequeño
        if abs(f(c)) < tol or abs(b - a) < tol:
            return c

        # Elegir el subintervalo que contiene el cambio de signo
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    raise ValueError("El método de bisección no convergió dentro del número de iteraciones dado.")
