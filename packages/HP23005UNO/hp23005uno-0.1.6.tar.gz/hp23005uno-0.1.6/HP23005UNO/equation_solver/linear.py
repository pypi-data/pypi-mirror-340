import numpy as np

def gauss_elimination(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError("División por cero detectada.")
        for j in range(i+1, n):
            r = A[j][i] / A[i][i]
            A[j] = A[j] - r * A[i]
            b[j] = b[j] - r * b[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i][i+1:], x[i+1:])) / A[i][i]
    return x

def gauss_jordan(A, b):
    A = np.array(A, float)
    b = np.array(b, float).reshape(-1, 1)
    Ab = np.hstack([A, b])
    n = len(b)
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(n):
            if i != j:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]
    return Ab[:, -1]

def cramer(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única.")
    n = len(b)
    x = np.zeros(n)
    for i in range(n):
        Ai = np.copy(A)
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    return x

def lu_decomposition(A, b):
    from scipy.linalg import lu
    A = np.array(A, float)
    b = np.array(b, float)
    P, L, U = lu(A)
    y = np.linalg.solve(L, np.dot(P, b))
    x = np.linalg.solve(U, y)
    return x

def jacobi(A, b, tol=1e-10, max_iter=100):
    A = np.array(A, float)
    b = np.array(b, float)
    x = np.zeros_like(b)
    D = np.diag(A)
    R = A - np.diagflat(D)
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise RuntimeError("No se alcanzó la convergencia en Jacobi.")

def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    A = np.array(A, float)
    b = np.array(b, float)
    x = np.zeros_like(b)
    n = len(b)
    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise RuntimeError("No se alcanzó la convergencia en Gauss-Seidel.")