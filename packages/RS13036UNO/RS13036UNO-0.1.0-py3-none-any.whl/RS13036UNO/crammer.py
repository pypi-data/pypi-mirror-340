# RS13036UNO/crammer.py
import numpy as np

def cramer(a, b):
    """
    Resuelve un sistema Ax = b usando la regla de Cramer.
    """
    a = np.array(a, float)
    b = np.array(b, float)
    det_a = np.linalg.det(a)
    if det_a == 0:
        raise ValueError("El sistema no tiene solución única (determinante = 0)")

    n = len(b)
    x = np.zeros(n)

    for i in range(n):
        a_temp = np.copy(a)
        a_temp[:, i] = b
        x[i] = np.linalg.det(a_temp) / det_a

    return x
