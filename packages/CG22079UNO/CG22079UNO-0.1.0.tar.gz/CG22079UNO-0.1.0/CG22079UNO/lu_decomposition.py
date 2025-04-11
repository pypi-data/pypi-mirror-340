import numpy as np

def lu_decomposition(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(A)
    L = np.zeros_like(A)
    U = np.zeros_like(A)
    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k]*U[k][j] for k in range(i))
        for j in range(i+1, n):
            L[j][i] = (A[j][i] - sum(L[j][k]*U[k][i] for k in range(i))) / U[i][i]
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j]*y[j] for j in range(i))
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i][j]*x[j] for j in range(i+1, n))) / U[i][i]
    return x
