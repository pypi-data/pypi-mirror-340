from CG22079UNO.ejemplos import (
    ejemplo_gauss,
    ejemplo_gauss_jordan,
    ejemplo_crammer,
    ejemplo_lu,
    ejemplo_jacobi,
    ejemplo_gauss_seidel,
    ejemplo_biseccion
)

def menu():
    while True:
        print("\n=== Métodos para resolver sistemas de ecuaciones ===")
        print("1. Eliminación de Gauss")
        print("2. Gauss-Jordan")
        print("3. Regla de Crammer")
        print("4. Descomposición LU")
        print("5. Método de Jacobi")
        print("6. Método de Gauss-Seidel")
        print("7. Método de Bisección")
        print("0. Salir")

        opcion = input("Seleccione un método: ")

        if opcion == '1':
            ejemplo_gauss()
        elif opcion == '2':
            ejemplo_gauss_jordan()
        elif opcion == '3':
            ejemplo_crammer()
        elif opcion == '4':
            ejemplo_lu()
        elif opcion == '5':
            ejemplo_jacobi()
        elif opcion == '6':
            ejemplo_gauss_seidel()
        elif opcion == '7':
            ejemplo_biseccion()
        elif opcion == '0':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
