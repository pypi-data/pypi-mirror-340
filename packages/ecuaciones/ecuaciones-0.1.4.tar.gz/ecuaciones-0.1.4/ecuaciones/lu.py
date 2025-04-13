import numpy as np
from scipy.linalg import lu

# Descomposición LU
def lu(a, b):
    """
    Resuelve un sistema de ecuaciones lineales mediante descomposición LU.
    """
    P, L, U = lu(a)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x
