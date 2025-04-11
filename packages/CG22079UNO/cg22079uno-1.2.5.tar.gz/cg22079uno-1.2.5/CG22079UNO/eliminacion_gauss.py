def gauss_elimination(a, b):
    n = len(b)
    for i in range(n):
        for j in range(i+1, n):
            ratio = a[j][i]/a[i][i]
            for k in range(n):
                a[j][k] -= ratio * a[i][k]
            b[j] -= ratio * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= a[i][j]*x[j]
        x[i] = x[i]/a[i][i]
    return x
