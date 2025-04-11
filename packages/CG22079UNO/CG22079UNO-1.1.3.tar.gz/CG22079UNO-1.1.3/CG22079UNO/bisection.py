def bisection(f, a, b, tol=1e-10, max_iterations=1000):
    # Comprobamos que la función tiene signos opuestos en los extremos del intervalo
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos.")
    
    # Repetimos hasta alcanzar el número máximo de iteraciones o la precisión deseada
    for _ in range(max_iterations):
        c = (a + b) / 2  # Punto medio del intervalo
        if abs(f(c)) < tol:  # Si el valor absoluto de la función en c es suficientemente pequeño, retornamos la raíz
            return c
        elif f(a) * f(c) < 0:  # Si la raíz está en el intervalo [a, c]
            b = c
        else:  # Si la raíz está en el intervalo [c, b]
            a = c
    
    # Si no se encuentra la raíz en el número máximo de iteraciones, retornamos el punto medio
    return (a + b) / 2

# Ejemplo de uso
def funcion(x):
    return x**2 - 4  # La función f(x) = x^2 - 4

# Intervalo [1, 3] donde buscamos la raíz
resultado = bisection(funcion, 1, 3)
print("Resultado con Bisección:", resultado)
