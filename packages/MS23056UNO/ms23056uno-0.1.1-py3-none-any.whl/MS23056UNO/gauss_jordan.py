def gauss_jordan(a, b):
    n = len(b)
    for i in range(n):
        factor = a[i][i]
        for j in range(n):
            a[i][j] /= factor
        b[i] /= factor

        for k in range(n):
            if k != i:
                factor = a[k][i]
                for j in range(n):
                    a[k][j] -= factor * a[i][j]
                b[k] -= factor * b[i]
    return b
