import numpy as np
from fractions import Fraction

# Matriz de coeficientes
A = np.array([
    [3, 2, -3],
    [-3, 1, 1],
    [1, -1, 0]
], dtype=float)

#Términos independientes
b = np.array([0, 0, -100], dtype=float)

#Método de Gauss-Jordan
def gauss_jordan_elimination(A, b):
    n = len(b)
    augmented = np.column_stack((A, b))

    print("Matriz aumentada inicial:")
    print(augmented)
    print()

    for i in range(n):
        # Pivoteo parcial
        max_row = i + np.argmax(abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
            print(f"Intercambio de filas {i+1} y {max_row+1}:")
            print(augmented)
            print()

        # Escalar la fila para que el pivote sea 1
        pivot = augmented[i, i]
        augmented[i] = augmented[i] / pivot
        print(f"Fila {i+1} dividida por {pivot}:")
        print(augmented)
        print()

        # Haciendo ceros las demás filas
        for j in range(n):
            if j != i:
                factor = augmented[j, i]
                augmented[j] = augmented[j] - factor * augmented[i]
                print(f"Fila {j+1} = Fila {j+1} - {factor} * Fila {i+1}:")
                print(augmented)
                print()

    # Extraer la solución
    x = augmented[:, -1]
    return x

# Resolver usando Gauss-Jordan
solution = gauss_jordan_elimination(A.copy(), b.copy())

# Convertir a fracciones para mostrar resultados exactos
solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

print("Solución encontrada:")
print(f"Peliculas de Accion = {solution_fractions[0]}")
print(f"Peliculas Western = {solution_fractions[1]}")
print(f"Peliculas de Terror = {solution_fractions[2]}")

# Verificación
print("\nVerificación:")
for i, row in enumerate(A):
    result = np.dot(row, solution)
    print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

# Comparación con NumPy
numpy_solution = np.linalg.solve(A, b)
print("\nSolución Definitiva:")
print(f"Peliculas de Accion = {Fraction(numpy_solution[0]).limit_denominator()}")
print(f"Peliculas Western = {Fraction(numpy_solution[1]).limit_denominator()}")
print(f"Peliculas de Terror = {Fraction(numpy_solution[2]).limit_denominator()}")
