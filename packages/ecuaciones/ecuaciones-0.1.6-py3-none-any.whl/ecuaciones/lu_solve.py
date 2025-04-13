import numpy as np
from scipy.linalg import lu as scipy_lu  

# Descomposición LU
def lu_solve(a, b):
    """
    Resuelve un sistema de ecuaciones lineales mediante descomposición LU.
    """
    P, L, U = scipy_lu(a)  
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x
