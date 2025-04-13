def gauss_jordan(A, b):
    n = len(b)
    for i in range(n):
        divisor = A[i][i]
        for j in range(n):
            A[i][j] /= divisor
        b[i] /= divisor
        for k in range(n):
            if i != k:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return b
