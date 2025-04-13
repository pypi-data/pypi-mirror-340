# RS13036UNO/gauss_jordan.py
import numpy as np

def gauss_jordan(a, b):
    """
    Resuelve un sistema Ax = b usando el método de Gauss-Jordan.
    """
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)
    aug = np.hstack([a, b.reshape(-1, 1)])

    for i in range(n):
        aug[i] = aug[i] / aug[i][i]
        for j in range(n):
            if i != j:
                aug[j] -= aug[j][i] * aug[i]

    return aug[:, -1]
