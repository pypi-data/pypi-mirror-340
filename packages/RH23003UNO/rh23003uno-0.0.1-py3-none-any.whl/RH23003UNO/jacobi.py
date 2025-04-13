import numpy as np

def jacobi(A, b, tol=1e-10, max_iter=1000):
    n = len(b)
    x = [10, 10, 10]
    for k in range(max_iter):
        x_prev = x.copy()
        for i in range(n):
            if A[i, i] != 0:
                x[i] = (b[i] - sum(A[i, j] * x_prev[j] for j in range(n) if j != i)) / A[i, i]
                print(x)
            else:
                print(f"No se puede continuar aproximacion ya que en linea {i} se encuentra un 0 y no se pueden realizar divisiones entre 0")
                return x
        if np.linalg.norm(np.array(x) - np.array(x_prev)) < tol:
            return x
    print(f"No se logro la convergencia en {max_iter} iteraciones")
    return x