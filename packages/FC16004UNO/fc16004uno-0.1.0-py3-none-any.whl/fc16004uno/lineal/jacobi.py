def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(A)
    x = x0 or [0.0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = [0.0 for _ in range(n)]
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new
        x = x_new
    return x