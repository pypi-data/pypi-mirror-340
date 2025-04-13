# RS13036UNO/gauss.py
import numpy as np

def gauss_elimination(a, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b mediante eliminación de Gauss.
    """
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)

    for k in range(n - 1):
        for i in range(k + 1, n):
            if a[k][k] == 0:
                raise ValueError("División por cero en eliminación de Gauss")
            factor = a[i][k] / a[k][k]
            a[i, k:] -= factor * a[k, k:]
            b[i] -= factor * b[k]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(a[i, i + 1:], x[i + 1:])) / a[i][i]
    return x
