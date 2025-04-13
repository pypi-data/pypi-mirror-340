import numpy as np

def cramer(a, b):
    det_a = np.linalg.det(a)
    if det_a == 0:
        raise ValueError("El sistema no tiene solución única.")
    n = len(b)
    x = []
    for i in range(n):
        ai = np.copy(a)
        ai[:, i] = b
        x.append(np.linalg.det(ai) / det_a)
    return x
