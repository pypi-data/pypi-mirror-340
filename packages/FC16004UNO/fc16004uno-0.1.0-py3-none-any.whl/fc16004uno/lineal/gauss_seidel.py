def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(A)
    x = x0 or [0.0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new
        x = x_new
    return x