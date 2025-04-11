def gauss_eliminacion(A, b):
    n = len(A)
    for i in range(n):
        for j in range(i+1, n):
            if A[i][i] == 0:
                raise ValueError("Division por cero en Gauss")
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - suma) / A[i][i]
    return x

def gauss_jordan(A, b):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError("Division por cero en Gauss-Jordan")
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        b[i] /= factor
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
    return b

def cramer(A, b):
    from numpy.linalg import det
    import numpy as np
    D = det(A)
    if D == 0:
        raise ValueError("Sistema sin solucion unica")
    n = len(A)
    x = []
    for i in range(n):
        Ai = [row[:] for row in A]
        for j in range(n):
            Ai[j][i] = b[j]
        x.append(det(Ai)/D)
    return x

def lu_decomposicion(A, b):
    import numpy as np
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i, n):
            if U[i][i] == 0:
                raise ValueError("Division por cero en LU")
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][k] * y[k] for k in range(i))
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i+1, n))) / U[i][i]
    return x.tolist()

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    import numpy as np
    n = len(A)
    x = x0 if x0 is not None else [0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        if np.linalg.norm(np.array(x_new) - np.array(x), ord=np.inf) < tol:
            return x_new
        x = x_new
    return x

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    import numpy as np
    n = len(A)
    x = x0 if x0 is not None else [0 for _ in range(n)]
    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i+1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
        if np.linalg.norm(np.array(x_new) - np.array(x), ord=np.inf) < tol:
            return x_new
        x = x_new
    return x
