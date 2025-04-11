import numpy as np

def gauss_jordan(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    # Formar la matriz aumentada
    Ab = np.hstack([A, b.reshape(-1, 1)])

    for i in range(n):
        # Hacer que el pivote sea 1
        Ab[i] = Ab[i] / Ab[i, i]
        # Hacer ceros en la columna del pivote
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]

    return Ab[:, -1]

# Ejemplo de uso:
A = [
    [1.0, 1.0, 1.0],
    [0.0, 2.0, 5.0],
    [2.0, 3.0, 1.0]
]
b = [6.0, -4.0, 4.0]

resultado = gauss_jordan(A, b)
print("Resultado con Gauss-Jordan:", resultado)
