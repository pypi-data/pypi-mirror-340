import numpy as np

def lu_decomposition(A, b):
    from scipy.linalg import lu
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x
