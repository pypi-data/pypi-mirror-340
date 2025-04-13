import numpy as np

# Método de Cramer
def cramer(a, b):
    """
    Resuelve un sistema lineal con la Regla de Cramer.
    """
    det_a = np.linalg.det(a)
    if det_a == 0:
        raise ValueError("El sistema no tiene solución única.")

    n = len(b)
    x = []
    for i in range(n):
        temp = np.copy(a)
        temp[:, i] = b
        x.append(np.linalg.det(temp) / det_a)
    return x
