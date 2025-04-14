import numpy as np

def cramer(augmented_matrix, decimals=1):
    # Separate coefficient matrix and independent terms
    coefficient = augmented_matrix[:, :-1]
    ind_terms = augmented_matrix[:, -1]

    n = len(ind_terms)
    det_main = np.linalg.det(coefficient)
    if det_main == 0:
        raise ValueError("El sistema no tiene una única solución (el determinante es cero).")

    solutions = np.zeros(n)
    for i in range(n):
        temp_matrix = np.copy(coefficient)
        temp_matrix[:, i] = ind_terms
        solutions[i] = np.linalg.det(temp_matrix) / det_main

    return np.round(solutions, decimals=decimals)




