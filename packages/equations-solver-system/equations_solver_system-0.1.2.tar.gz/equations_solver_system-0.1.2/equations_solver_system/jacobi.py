def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    n = len(b)
    x = x0 or [0]*n
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s = sum(A[i][j]*x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if max(abs(x_new[i]-x[i]) for i in range(n)) < tol:
            return x_new
        x = x_new
    return x
