import numpy as np

def descomposicion_lu(coefficient, ind_terms, decimals=1):
    coefficient = np.array(coefficient, dtype=float)
    ind_terms = np.array(ind_terms, dtype=float)
    n = len(ind_terms)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        for k in range(i, n):
            U[i, k] = coefficient[i, k] - sum(L[i, j] * U[j, k] for j in range(i))
        for k in range(i, n):
            if i == k:
                L[i, i] = 1
            else:
                L[k, i] = (coefficient[k, i] - sum(L[k, j] * U[j, i] for j in range(i))) / U[i, i]

    y = np.zeros(n)
    for i in range(n):
        y[i] = ind_terms[i] - sum(L[i, j] * y[j] for j in range(i))

    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]

    return np.round(x, decimals=decimals)  