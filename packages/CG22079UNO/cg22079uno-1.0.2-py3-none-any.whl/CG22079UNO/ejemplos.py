from .metodos import (
    gauss_elimination,
    gauss_jordan,
    crammer,
    lu_decomposition,
    jacobi,
    gauss_seidel,
    biseccion
)

# 1. Eliminación de Gauss
def ejemplo_gauss():
    A = [[2, 1, -1],
         [-3, -1, 2],
         [-2, 1, 2]]
    b = [8, -11, -3]
    print("\n--- Eliminación de Gauss ---")
    print("Ejemplo:")
    print("2x +  y -  z = 8")
    print("-3x - y + 2z = -11")
    print("-2x + y + 2z = -3\n")
    resultado = gauss_elimination(A, b)
    print("Resultado:")
    print("x =", round(resultado[0], 4), "y =", round(resultado[1], 4), "z =", round(resultado[2], 4))


# 2. Gauss-Jordan
def ejemplo_gauss_jordan():
    A = [[1, 1, 1],
         [2, 3, 5],
         [4, 0, 5]]
    b = [6, -4, 27]
    print("\n--- Gauss-Jordan ---")
    print("Ejemplo:")
    print("x + y + z = 6")
    print("2x + 3y + 5z = -4")
    print("4x + 0y + 5z = 27\n")
    resultado = gauss_jordan(A, b)
    print("Resultado:")
    print("x =", round(resultado[0], 4), "y =", round(resultado[1], 4), "z =", round(resultado[2], 4))


# 3. Crammer
def ejemplo_crammer():
    A = [[3, -2, 5],
         [4, 5, 8],
         [1, 1, 3]]
    b = [2, 7, 1]
    print("\n--- Regla de Crammer ---")
    print("Ejemplo:")
    print("3x - 2y + 5z = 2")
    print("4x + 5y + 8z = 7")
    print("x + y + 3z = 1\n")
    resultado = crammer(A, b)
    print("Resultado:")
    print("x =", round(resultado[0], 4), "y =", round(resultado[1], 4), "z =", round(resultado[2], 4))


# 4. LU
def ejemplo_lu():
    A = [[2, 3, 1],
         [4, 7, 7],
         [-2, 4, 5]]
    b = [1, 2, 3]
    print("\n--- Descomposición LU ---")
    print("Ejemplo:")
    print("2x + 3y + z = 1")
    print("4x + 7y + 7z = 2")
    print("-2x + 4y + 5z = 3\n")
    resultado = lu_decomposition(A, b)
    print("Resultado:")
    print("x =", round(resultado[0], 4), "y =", round(resultado[1], 4), "z =", round(resultado[2], 4))


# 5. Jacobi
def ejemplo_jacobi():
    A = [[10, -1, 2, 0],
         [-1, 11, -1, 3],
         [2, -1, 10, -1],
         [0, 3, -1, 8]]
    b = [6, 25, -11, 15]
    print("\n--- Método de Jacobi ---")
    print("Ejemplo:")
    print("10x1 - x2 + 2x3       = 6")
    print("-x1 + 11x2 - x3 + 3x4 = 25")
    print("2x1 - x2 + 10x3 - x4  = -11")
    print("3x2 - x3 + 8x4        = 15\n")
    resultado = jacobi(A, b, tol=1e-10)
    print("Resultado:")
    for i, val in enumerate(resultado):
        print(f"x{i+1} =", round(val, 6))


# 6. Gauss-Seidel
def ejemplo_gauss_seidel():
    A = [[4, 1, 2],
         [3, 5, 1],
         [1, 1, 3]]
    b = [4, 7, 3]
    print("\n--- Método de Gauss-Seidel ---")
    print("Ejemplo:")
    print("4x + y + 2z = 4")
    print("3x + 5y + z = 7")
    print("x + y + 3z = 3\n")
    resultado = gauss_seidel(A, b, tol=1e-10)
    print("Resultado:")
    for i, val in enumerate(resultado):
        print(f"x{i+1} =", round(val, 6))


# 7. Bisección
def ejemplo_biseccion():
    f = lambda x: x**3 - x - 2
    print("\n--- Método de Bisección ---")
    print("Función:")
    print("f(x) = x^3 - x - 2")
    print("Intervalo inicial: [1, 2]\n")
    raiz = biseccion(f, 1, 2, tol=1e-10)
    print("Raíz aproximada:", round(raiz, 10))
