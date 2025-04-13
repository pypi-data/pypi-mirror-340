import numpy as np

def cramer(coefficient, ind_terms):
    n = len(ind_terms)
    det_main = np.linalg.det(coefficient)
    if det_main == 0:
        raise ValueError("El sistema no tiene una unica solucion (el determinante es cero).")
    
    solutions = np.zeros(n)
    for i in range(n):
        temp_matrix = np.copy(coefficient)
        temp_matrix[:, i] = ind_terms
        solutions[i] = np.linalg.det(temp_matrix) / det_main
        
    return solutions

