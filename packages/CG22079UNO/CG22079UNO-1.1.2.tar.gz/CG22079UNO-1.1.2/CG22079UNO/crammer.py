import numpy as np

def crammer(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    detA = np.linalg.det(A)
    if detA == 0:
        raise ValueError("El sistema no tiene solución única.")

    n = len(b)
    x = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x.append(np.linalg.det(Ai) / detA)

    return x
