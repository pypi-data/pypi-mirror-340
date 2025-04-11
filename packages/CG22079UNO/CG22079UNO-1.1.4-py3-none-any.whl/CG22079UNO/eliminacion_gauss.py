import numpy as np

def gauss_elimination(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    for i in range(n):
        for j in range(i+1, n):
            if A[i][i] == 0:
                raise ZeroDivisionError("División por cero en gauss_elimination")
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - suma) / A[i][i]

    return x

# Ejemplo de uso:
A = [
    [2.0, 3.0, -1.0],
    [1.0, -1.0, 2.0],
    [3.0, 2.0, 1.0]
]
b = [4.0, -1.0, 6.0]

resultado = gauss_elimination(A, b)
print("Resultado con Eliminación de Gauss:", resultado)
