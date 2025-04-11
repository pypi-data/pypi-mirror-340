import numpy as np

def jacobi(A, b, x0=None, tol=1e-10, max_iterations=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros_like(b) if x0 is None else np.array(x0, dtype=float)

    for _ in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.allclose(x, x_new, atol=tol):
            return x_new
        x = x_new
    return x

# Ejemplo de uso
A = [
    [4, -1, -1],
    [1, -4, 1],
    [1, 1, -4]
]
b = [150, -80, -90]

resultado = jacobi(A, b)
print("Resultado con Jacobi:", resultado)
