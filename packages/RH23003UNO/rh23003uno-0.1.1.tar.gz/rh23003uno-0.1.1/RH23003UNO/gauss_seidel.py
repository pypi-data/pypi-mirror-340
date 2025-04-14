import numpy as np

def gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    A = np.array(A, dtype=float)  
    b = np.array(b, dtype=float)  
    n = len(b)
    x = np.array([10.0] * n)     

    for k in range(max_iter):
        x_prev = x.copy()
        for i in range(n):
            if A[i, i] != 0:
                x[i] = (b[i] - sum(A[i, j] * x[j] for j in range(n) if j != i)) / A[i, i]
                print(f"Iter {k}, x = {x}")
            else:
                print(f"No se puede dividir entre cero en linea {i}")
                return x
        if np.linalg.norm(x - x_prev) < tol:
            print("Convergio!")
            return x

    print(f"No convergio en {max_iter} iteraciones")
    return x