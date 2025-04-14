import numpy as np

def gauss(coefficient, ind_terms):    
    coefficient = np.array(coefficient, dtype=float)
    ind_terms = np.array(ind_terms, dtype=float)

    n = len(ind_terms)
    equations = np.hstack([coefficient, ind_terms.reshape(-1, 1)])

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(equations[r, i]))
        equations[[i, max_row]] = equations[[max_row, i]]

        for j in range(i + 1, n):
            factor = equations[j, i] / equations[i, i]
            equations[j] -= factor * equations[i]
    
    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        x[i] = (equations[i, -1] - np.dot(equations[i, i + 1:n], x[i + 1:n])) / equations[i, i]

    return x
