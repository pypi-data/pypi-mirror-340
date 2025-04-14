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

# Parámetros
x0 = np.zeros(len(b))  # Valores iniciales x1=0, x2=0, x3=0
max_iter = 10  # Máximo número de iteraciones
tolerance = 1e-10  # Tolerancia del error permitido

def gauss_seidel(A, b, x0, max_iter, tolerance):
    n = len(b)
    x = x0.copy()

    print("Iteraciones Método de Gauss-Seidel:\n")

    for k in range(max_iter):
        x_old = x.copy()

        print(f"Iteración {k+1}:")
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i][i]
            print(f"x{i+1} = {x[i]}")

        print()

        # Comprobación de convergencia
        error = np.linalg.norm(x - x_old, ord=np.inf)
        if error < tolerance:
            print(f"Convergencia alcanzada en la iteración {k+1}")
            break

    return x

# Ejecutar método
solution = gauss_seidel(A, b, x0, max_iter, tolerance)

# Convertir solución a fracciones
solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

print("Solución encontrada:")
print(f"x₁ = {solution_fractions[0]}")
print(f"x₂ = {solution_fractions[1]}")
print(f"x₃ = {solution_fractions[2]}")

# Verificación
print("\nVerificación:")
for i, row in enumerate(A):
    result = np.dot(row, solution)
    print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-6 else '✗'}")

# Comparar con np.linalg.solve()
numpy_solution = np.linalg.solve(A, b)
print("\nSolución:")
print(f"x₁ = {Fraction(numpy_solution[0]).limit_denominator()}")
print(f"x₂ = {Fraction(numpy_solution[1]).limit_denominator()}")
print(f"x₃ = {Fraction(numpy_solution[2]).limit_denominator()}")
