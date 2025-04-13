def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) >= 0:
        raise ValueError("No hay cambio de signo en el intervalo.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or abs(b - a) < tol:
            return c
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2
