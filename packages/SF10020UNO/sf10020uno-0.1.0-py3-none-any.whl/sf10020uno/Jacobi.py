import numpy as np
from fractions import Fraction

# Matriz de coeficientes
A = np.array([
    [2, 6, 1],
    [1, 2, -1],
    [5, 7, -4]
], dtype=float)

# Vector de términos independientes
b = np.array([7, -1, 9], dtype=float)

# Valores iniciales (pueden ser 0)
x0 = np.zeros(len(b))

# Parámetros del método
max_iter = 100  # Número máximo de iteraciones
tolerance = 1e-6  # Tolerancia del error permitido


def jacobi_method(A, b, x0, max_iter, tolerance):
    n = len(b)
    x = x0.copy()

    print("Iteraciones del Método de Jacobi:\n")

    for k in range(max_iter):
        x_new = np.zeros(n)

        print(f"Iteración {k+1}:")
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
            print(f"x{i+1} = {x_new[i]}")

        print()

        error = np.linalg.norm(x_new - x, ord=np.inf)

        if error < tolerance:
            print(f"Convergencia alcanzada en la iteración {k+1}")
            break

        x = x_new.copy()

    return x


# Resolver usando Jacobi
solution = jacobi_method(A, b, x0, max_iter, tolerance)

# Mostrar resultados como fracciones
solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

print("Solución encontrada:")
print(f"x₁ = {solution_fractions[0]}")
print(f"x₂ = {solution_fractions[1]}")
print(f"x₃ = {solution_fractions[2]}")

# Verificación de la solución
print("\nVerificación:")
for i, row in enumerate(A):
    result = np.dot(row, solution)
    print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-6 else '✗'}")

# Comparar con numpy
numpy_solution = np.linalg.solve(A, b)
print("\nSolución Definitiva:")
print(f"x₁ = {Fraction(numpy_solution[0]).limit_denominator()}")
print(f"x₂ = {Fraction(numpy_solution[1]).limit_denominator()}")
print(f"x₃ = {Fraction(numpy_solution[2]).limit_denominator()}")