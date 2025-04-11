import numpy as np

def crammer(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("La matriz A es singular y no tiene solución única.")
    n = len(b)
    soluciones = np.zeros(n)
    for i in range(n):
        A_copy = A.copy()
        A_copy[:, i] = b
        soluciones[i] = np.linalg.det(A_copy) / det_A
    return soluciones

# Ejemplo de uso:
A = [
    [3.0, 1.0],
    [2.0, 3.0]
]
b = [9.0, 13.0]

resultado = crammer(A, b)
print("Resultado con Regla de Crammer:", resultado)
