import numpy as np

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0
    for _ in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x
