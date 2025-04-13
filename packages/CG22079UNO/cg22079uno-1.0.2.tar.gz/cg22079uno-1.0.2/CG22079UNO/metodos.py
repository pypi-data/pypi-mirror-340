import numpy as np

# ----------------- Método 1: Eliminación de Gauss -----------------
def gauss_elimination(A, b):
    n = len(b)
    A = [row[:] for row in A]
    b = b[:]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= ratio * A[i][k]
            b[j] -= ratio * b[i]
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

# ----------------- Método 2: Gauss-Jordan -----------------
def gauss_jordan(A, b):
    n = len(A)
    A = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        factor = A[i][i]
        for j in range(i, n + 1):
            A[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n + 1):
                    A[k][j] -= factor * A[i][j]
    return [A[i][n] for i in range(n)]

# ----------------- Método 3: Crammer -----------------
def crammer(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única")
    n = len(b)
    x = []
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        xi = np.linalg.det(Ai) / det_A
        x.append(xi)
    return x

# ----------------- Método 4: Descomposición LU -----------------
def lu_decomposition(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i + 1, n):
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

# ----------------- Método 5: Jacobi -----------------
def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(A)
    x = x0 or [0.0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = []
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new.append((b[i] - s) / A[i][i])
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new
        x = x_new
    return x

# ----------------- Método 6: Gauss-Seidel -----------------
def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(A)
    x = x0 or [0.0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new
        x = x_new
    return x

# ----------------- Método 7: Bisección -----------------
def biseccion(f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or abs(b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
