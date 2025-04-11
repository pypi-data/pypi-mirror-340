import numpy as np

def jacobi(A, b, x0=None, tol=1e-10, max_iterations=100):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    for _ in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    return x
