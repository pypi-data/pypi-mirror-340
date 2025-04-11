import numpy as np

def jacobi(a, b, x0=None, tol=1e-10, max_iterations=1000):
    n = len(a)
    x = np.zeros(n) if x0 is None else x0
    for _ in range(max_iterations):
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(a[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / a[i][i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x
