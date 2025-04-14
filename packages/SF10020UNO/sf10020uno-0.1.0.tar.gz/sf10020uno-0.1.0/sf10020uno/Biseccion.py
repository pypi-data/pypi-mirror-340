from fractions import Fraction

# Definir la función f(x)
def f(x):
    # Ejemplo: x^3 + 4x^2 - 10
    return x**3 + 4*x**2 - 10

# Parámetros iniciales
a = 1  # Límite inferior
b = 2  # Límite superior
tolerance = 1e-10  # Tolerancia permitida
max_iter = 10  # Máximo número de iteraciones

def bisection_method(f, a, b, tolerance, max_iter):
    if f(a) * f(b) >= 0:
        print("El método de bisección no garantiza una raíz en el intervalo dado.")
        return None

    print("Iteraciones Método de Bisección:\n")

    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        print(f"Iteración {k}: a={a}, b={b}, c={c}, f(c)={f(c)}")

        if abs(f(c)) < tolerance or (b - a) / 2 < tolerance:
            print(f"\nConvergencia alcanzada en la iteración {k}")
            return c

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    print("\nSe alcanzó el número máximo de iteraciones sin convergencia.")
    return (a + b) / 2

# Ejecutar método
root = bisection_method(f, a, b, tolerance, max_iter)

# Mostrar resultado
if root is not None:
    print(f"\nRaíz encontrada: x = {Fraction(root).limit_denominator()}")

    print(f"Valor de f(x) en la raíz encontrada: {f(root)}")
