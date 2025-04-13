import numpy as np

def gauss_jordan(coefficient, ind_terms):    
    n = len(ind_terms)
    equations = np.hstack([coefficient, ind_terms.reshape(-1,1)])
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(equations[r, i]))
        equations[[i, max_row]] = equations[[max_row, i]]
        equations[i] = equations[i] / equations[i, i]
        for j in range(n):
            if j != i:
                factor = equations[j, i]
                equations[j] -= factor * equations[i]
    return equations[:, -1]