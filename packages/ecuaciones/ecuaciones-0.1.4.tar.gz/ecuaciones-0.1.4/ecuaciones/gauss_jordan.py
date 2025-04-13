# Método de Gauss-Jordan
def gauss_jordan(a, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    """
    n = len(a)
    for i in range(n):
        # Pivoteo
        factor = a[i][i]
        for j in range(n):
            a[i][j] /= factor
        b[i] /= factor

        for k in range(n):
            if k != i:
                factor = a[k][i]
                for j in range(n):
                    a[k][j] -= factor * a[i][j]
                b[k] -= factor * b[i]
    return b
