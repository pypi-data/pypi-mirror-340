import numpy as np

# Método de Jacobi
def jacobi(a, b, tol=1e-10, max_iter=100):
    """
    Método iterativo de Jacobi para sistemas de ecuaciones lineales.
    """
    n = len(a)
    x = np.zeros(n)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s = sum(a[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / a[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        x = x_new
    return x.tolist()
