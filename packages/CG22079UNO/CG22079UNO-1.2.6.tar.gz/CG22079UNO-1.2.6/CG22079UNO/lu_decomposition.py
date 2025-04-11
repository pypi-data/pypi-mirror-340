import numpy as np
from scipy.linalg import lu_decomposition

def lu_decomposition(a, b):
    P, L, U = lu(a)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x
