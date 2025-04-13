from RS13036UNO import (
    gauss_elimination,
    gauss_jordan,
    cramer,
    lu_decomposition,
    jacobi,
    gauss_seidel,
    biseccion
)

# ------------------------------
print("=== Eliminación de Gauss ===")
A = [[2, 1], [1, 3]]
b = [8, 13]
sol = gauss_elimination(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Gauss-Jordan ===")
A = [[2, 1], [1, 3]]
b = [8, 13]
sol = gauss_jordan(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Cramer ===")
A = [[2, 1], [1, 3]]
b = [8, 13]
sol = cramer(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Descomposición LU ===")
A = [[4, 3], [6, 3]]
b = [10, 12]
sol = lu_decomposition(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Jacobi ===")
A = [[10, -1, 2, 0],
     [-1, 11, -1, 3],
     [2, -1, 10, -1],
     [0, 3, -1, 8]]
b = [6, 25, -11, 15]
sol = jacobi(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Gauss-Seidel ===")
A = [[10, -1, 2, 0],
     [-1, 11, -1, 3],
     [2, -1, 10, -1],
     [0, 3, -1, 8]]
b = [6, 25, -11, 15]
sol = gauss_seidel(A, b)
print("Solución:", sol)

# ------------------------------
print("\n=== Bisección ===")
def f(x):
    return x**3 - 4*x - 9

sol = biseccion(f, a=2, b=3, tol=1e-6)
print("Raíz aproximada:", sol)
