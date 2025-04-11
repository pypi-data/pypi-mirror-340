import numpy as np
from scipy.linalg import lu, solve

def lu_decomposition(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    
    P, L, U = lu(A)
    
    # Resolver Ly = Pb
    Pb = np.dot(P, b)
    y = np.linalg.solve(L, Pb)
    x = np.linalg.solve(U, y)
    return x

# Ejemplo de uso:
A = [
    [1.0, 2.0, 3.0],
    [2.0, 5.0, 2.0],
    [2.0, 3.0, 4.0]
]
b = [14.0, 18.0, 20.0]

resultado = lu_decomposition(A, b)
print("Resultado con Descomposición LU:", resultado)
