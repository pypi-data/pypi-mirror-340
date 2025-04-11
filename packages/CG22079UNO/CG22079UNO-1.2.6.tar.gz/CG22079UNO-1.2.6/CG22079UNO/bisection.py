def bisection(f, a, b, tol=1e-6, max_iter=1000):
    if f(a) * f(b) >= 0:
        return "No cumple condición de signos"
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or abs(b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c

