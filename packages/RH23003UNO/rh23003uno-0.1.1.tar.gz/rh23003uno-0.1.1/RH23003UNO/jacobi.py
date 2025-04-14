import numpy as np

def jacobi(A, b, tol=1e-10, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    x = np.full(n, 10.0)
    
    for k in range(max_iter):
        x_prev = x.copy()
        for i in range(n):
            if A[i, i] != 0:
                sum_ = np.dot(A[i, :i], x_prev[:i]) + np.dot(A[i, i+1:], x_prev[i+1:])
                x[i] = (b[i] - sum_) / A[i, i]
                print(x)
            else:
                print(f"No se puede continuar: división entre 0 en la fila {i}")
                return x
        if np.linalg.norm(x - x_prev) < tol:
            return x
    print(f"No se logró la convergencia en {max_iter} iteraciones")
    return x

