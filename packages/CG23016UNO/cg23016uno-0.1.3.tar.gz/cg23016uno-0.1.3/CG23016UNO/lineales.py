import numpy as np
from scipy.linalg import lu

def gauss_elimination(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    for i in range(n):
        for j in range(i+1, n):
            factor = A[j][i]/A[i][i]
            A[j] = A[j] - factor*A[i]
            b[j] = b[j] - factor*b[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i][i+1:], x[i+1:])) / A[i][i]
    return x.tolist()

def gauss_jordan(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    aug = np.hstack([A, b])
    n = len(b)
    for i in range(n):
        aug[i] = aug[i] / aug[i][i]
        for j in range(n):
            if i != j:
                aug[j] = aug[j] - aug[j][i]*aug[i]
    return aug[:, -1].tolist()

def cramer(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("Sistema sin solución única.")
    x = []
    for i in range(len(b)):
        Ai = A.copy()
        Ai[:, i] = b
        x.append(np.linalg.det(Ai)/det_A)
    return x

def lu_decomposition(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x.tolist()

def jacobi(A, b, tol=1e-10, max_iter=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.zeros_like(b)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(len(A)):
            s = np.dot(A[i, :], x) - A[i, i]*x[i]
            x_new[i] = (b[i] - s) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        x = x_new
    return x.tolist()

def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.zeros_like(b)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(len(A)):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        x = x_new
    return x.tolist()
