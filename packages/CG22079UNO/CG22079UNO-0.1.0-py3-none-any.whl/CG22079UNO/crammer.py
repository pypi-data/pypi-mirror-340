import numpy as np

def cramer(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única")
    n = len(b)
    x = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x.append(np.linalg.det(Ai) / det_A)
    return x
