# RS13036UNO/gauss_seidel.py
import numpy as np

def gauss_seidel(a, b, x0=None, tol=1e-10, max_iter=100):
    """
    Método de Gauss-Seidel para resolver Ax = b.
    """
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, float)

    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(a[i][j] * x_new[j] for j in range(i))
            s2 = sum(a[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / a[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise ValueError("El método de Gauss-Seidel no convergió")
