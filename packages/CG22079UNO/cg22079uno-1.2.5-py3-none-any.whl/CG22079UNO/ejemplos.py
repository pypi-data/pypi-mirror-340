from . import gauss_elimination, gauss_jordan, crammer, lu_decomposition, jacobi, gauss_seidel, bisection
import numpy as np

def mostrar_ejemplo(metodo):
    if metodo == "gauss_elimination":
        a = [[3,2,-4],[2,3,3],[5,-3,1]]
        b = [3,15,14]
        print("Gauss Elimination:\nSistema:")
        print(a, b)
        print("Resultado:", gaussgauss_elimination.gauss_elimination(a,b))

    elif metodo == "gauss_jordan":
        a = [[3,2,-4],[2,3,3],[5,-3,1]]
        b = [3,15,14]
        print("Gauss-Jordan:\nSistema:")
        print(a, b)
        print("Resultado:", gauss_jordan.gauss_jordan(a, b))

    elif metodo == "crammer":
        a = np.array([[2, -1, 5], [3, 2, 2], [1, 3, 3]])
        b = np.array([8, 14, 14])
        print("Crammer:\nSistema:")
        print(a, b)
        print("Resultado:", crammer.crammer(a,b))

    elif metodo == "lu_decomposition":
        a = np.array([[2, -1, 5], [3, 2, 2], [1, 3, 3]])
        b = np.array([8, 14, 14])
        print("LU Descomposición:\nSistema:")
        print(a, b)
        print("Resultado:", lu_decomposition.lu_decomposition(a, b))

    elif metodo == "jacobi":
        a = np.array([[10, -1, 2, 0],
                      [-1, 11, -1, 3],
                      [2, -1, 10, -1],
                      [0, 3, -1, 8]])
        b = np.array([6, 25, -11, 15])
        print("Jacobi:\nSistema:")
        print(a, b)
        print("Resultado:", jacobi.jacobi(a,b))

    elif metodo == "gauss_seidel":
        a = np.array([[4,1,2],[3,5,1],[1,1,3]])
        b = np.array([4,7,3])
        print("Gauss-Seidel:\nSistema:")
        print(a, b)
        print("Resultado:", gauss_seidel.gauss_seidel(a,b))

    elif metodo == "bisection":
        f = lambda x: x**3 - x - 2
        print("Bisección:\nf(x) = x^3 - x - 2")
        print("Resultado:", bisection.bisection(f, 1, 2))
