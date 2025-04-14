import numpy as np
from fractions import Fraction

# Definir el sistema de ecuaciones
# 8x₁ + 2x₂ - 2x₃ = -2
# 10x₁ + 2x₂ + 4x₃ = 4
# 12x₁ + 2x₂ + 2x₃ = 6

# Matriz de coeficientes
A = np.array([
    [2, 6, 1],
    [1, 2, -1],
    [5, 7, -4]
], dtype=float)

# Términos independientes
b = np.array([7, -1, 9], dtype=float)

# Función para implementar la eliminación de Gauss manualmente
def gauss_elimination(A, b):
    n = len(b)
    # Crear una matriz aumentada [A|b]
    augmented = np.column_stack((A, b))
    
    # Imprimir la matriz aumentada inicial
    print("Matriz aumentada inicial:")
    print(augmented)
    print()
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial: buscar el elemento máximo en la columna
        max_row = i + np.argmax(abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
            print(f"Intercambio de filas {i+1} y {max_row+1}:")
            print(augmented)
            print()
        
        # Escalar el pivote a 1
        pivot = augmented[i, i]
        augmented[i] = augmented[i] / pivot
        print(f"Fila {i+1} dividida por {pivot}:")
        print(augmented)
        print()
        
        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = augmented[j, i]
            augmented[j] = augmented[j] - factor * augmented[i]
            print(f"Fila {j+1} = Fila {j+1} - {factor} * Fila {i+1}:")
            print(augmented)
            print()
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = augmented[i, -1]
        for j in range(i+1, n):
            x[i] -= augmented[i, j] * x[j]
    
    return x

# Resolver usando nuestra implementación de Gauss
solution = gauss_elimination(A.copy(), b.copy())

# Convertir a fracciones
solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

print("Solución encontrada:")
print(f"x₁ = {solution_fractions[0]}")
print(f"x₂ = {solution_fractions[1]}")
print(f"x₃ = {solution_fractions[2]}")

# Verificar la solución con la respuesta esperada
expected = np.array([3/2, -13/2, 1/2])
print("\nSolución esperada:")
print(f"x₁ = {Fraction(3, 2)}")
print(f"x₂ = {Fraction(-13, 2)}")
print(f"x₃ = {Fraction(1, 2)}")

# Verificar que nuestra solución es correcta
print("\nVerificación:")
for i, row in enumerate(A):
    result = np.dot(row, solution)
    print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

# Alternativamente, resolver usando la función de NumPy para comparar
numpy_solution = np.linalg.solve(A, b)
print("\nSolución Definitiva:")
print(f"x₁ = {Fraction(numpy_solution[0]).limit_denominator()}")
print(f"x₂ = {Fraction(numpy_solution[1]).limit_denominator()}")
print(f"x₃ = {Fraction(numpy_solution[2]).limit_denominator()}")