import numpy as np

def crammer(a, b):
    det_a = np.linalg.det(a)
    if det_a == 0:
        return "No tiene solución única"
    n = len(b)
    x = []
    for i in range(n):
        temp = a.copy()
        temp[:, i] = b
        x.append(round(np.linalg.det(temp)/det_a, 3))
    return x
