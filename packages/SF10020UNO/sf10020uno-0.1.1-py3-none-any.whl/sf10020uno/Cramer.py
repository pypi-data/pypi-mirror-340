import numpy as np
from fractions import Fraction

# Matriz de coeficientes
A = np.array([
    [1, 2, 1],
    [3, 1, 1],
    [2, 3, -1]
], dtype=float)

#Términos independientes
b = np.array([7, 5, 3], dtype=float)

#Método de Cramer
def cramer_method(A, b):
    n = len(b)
    det_A = np.linalg.det(A)

    print(f"Determinante de A: {det_A}")
    if abs(det_A) < 1e-10:
        raise ValueError("El sistema no tiene solución única (determinante cero).")

    solutions = []

    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        det_Ai = np.linalg.det(A_i)
        print(f"Determinante de A reemplazando columna {i+1}: {det_Ai}")
        x_i = det_Ai / det_A
        solutions.append(x_i)

    return solutions

#Usando el método de Cramer
solution = cramer_method(A, b)

# Convirtiendo a fracciones
solution_fractions = [Fraction(val).limit_denominator() for val in solution]

print("\nSolución encontrada:")
print(f"x₁ = {solution_fractions[0]}")
print(f"x₂ = {solution_fractions[1]}")
print(f"x₃ = {solution_fractions[2]}")

# Verificación
print("\nVerificación:")
for i, row in enumerate(A):
    result = np.dot(row, solution)
    print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

# Comparación con NumPy
numpy_solution = np.linalg.solve(A, b)
print("\nSolución Definitiva")
print(f"x₁ = {Fraction(numpy_solution[0]).limit_denominator()}")
print(f"x₂ = {Fraction(numpy_solution[1]).limit_denominator()}")
print(f"x₃ = {Fraction(numpy_solution[2]).limit_denominator()}")
