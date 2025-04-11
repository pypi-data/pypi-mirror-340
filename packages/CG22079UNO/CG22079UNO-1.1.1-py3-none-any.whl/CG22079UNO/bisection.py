def bisection(f, a, b, tol=1e-10):
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo.")

    while (b - a) / 2 > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
