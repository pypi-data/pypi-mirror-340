# RS13036UNO/jacobi.py
import numpy as np

def jacobi(a, b, x0=None, tol=1e-10, max_iter=100):
    """
    Método de Jacobi para resolver Ax = b.
    """
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, float)

    for _ in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(a[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / a[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise ValueError("El método de Jacobi no convergió")
