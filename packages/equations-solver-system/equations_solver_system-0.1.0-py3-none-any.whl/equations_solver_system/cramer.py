def cramer(A, b):
    from copy import deepcopy
    def determinant(M):
        if len(M) == 2:
            return M[0][0]*M[1][1] - M[0][1]*M[1][0]
        return sum((-1)**j * M[0][j] * determinant([row[:j] + row[j+1:] for row in M[1:]]) for j in range(len(M)))
    detA = determinant(A)
    if detA == 0:
        raise ValueError("Sistema sin solución única.")
    n = len(b)
    x = []
    for i in range(n):
        Ai = deepcopy(A)
        for j in range(n):
            Ai[j][i] = b[j]
        x.append(determinant(Ai) / detA)
    return x
