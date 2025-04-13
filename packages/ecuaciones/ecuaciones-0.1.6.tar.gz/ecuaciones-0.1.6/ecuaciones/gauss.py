import numpy as np

# Método de Eliminación de Gauss
def gauss(a, b):
    """
    Resuelve un sistema de ecuaciones lineales usando eliminación de Gauss.
    a: matriz de coeficientes (numpy array)
    b: vector de constantes (numpy array)
    """
    a = a.astype(float)
    b = b.astype(float)
    n = len(b)

    for i in range(n):
        # Pivoteo parcial con NumPy
        max_row = np.argmax(np.abs(a[i:, i])) + i
        if a[max_row, i] == 0:
            raise ValueError("División por cero: pivote nulo encontrado.")

        if max_row != i:
            a[[i, max_row]] = a[[max_row, i]]
            b[[i, max_row]] = b[[max_row, i]]

        # Eliminación
        for j in range(i + 1, n):
            factor = a[j][i] / a[i][i]
            a[j, i:] -= factor * a[i, i:]
            b[j] -= factor * b[i]

    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = np.dot(a[i, i+1:], x[i+1:])
        if a[i][i] == 0:
            raise ValueError("División por cero durante la sustitución.")
        x[i] = (b[i] - suma) / a[i][i]

    return x.tolist()
