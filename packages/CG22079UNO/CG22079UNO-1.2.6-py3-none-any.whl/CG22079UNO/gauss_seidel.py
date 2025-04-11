import numpy as np

def gauss_seidel(a, b, x0=None, tol=1e-10, max_iterations=1000):
    n = len(a)
    x = np.zeros(n) if x0 is None else x0
    for _ in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(a[i][j] * x_new[j] for j in range(i))
            s2 = sum(a[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / a[i][i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x
