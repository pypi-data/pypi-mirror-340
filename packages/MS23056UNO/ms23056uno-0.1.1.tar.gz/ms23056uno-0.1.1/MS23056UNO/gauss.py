import numpy as np

def gauss_elimination(a, b):
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)

    for k in range(n-1):
        for i in range(k+1, n):
            if a[k][k] == 0:
                raise ValueError("División por cero")
            factor = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]

    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        s = sum(a[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - s) / a[i][i]
    return x.tolist()