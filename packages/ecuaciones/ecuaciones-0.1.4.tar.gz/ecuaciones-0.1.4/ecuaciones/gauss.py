# Método de Eliminación de Gauss
def gauss(a, b):
    """
    Resuelve un sistema de ecuaciones lineales usando eliminación de Gauss.
    a: matriz de coeficientes
    b: vector de constantes
    """
    n = len(b)
    for i in range(n):
        # Pivoteo parcial
        max_row = max(range(i, n), key=lambda r: abs(a[r][i]))
        a[i], a[max_row] = a[max_row], a[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminación
        for j in range(i + 1, n):
            factor = a[j][i] / a[i][i]
            for k in range(i, n):
                a[j][k] -= factor * a[i][k]
            b[j] -= factor * b[i]

    # Sustitución hacia atrás
    x = [0] * n
    for i in range(n - 1, -1, -1):
        suma = sum(a[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - suma) / a[i][i]
    return x
