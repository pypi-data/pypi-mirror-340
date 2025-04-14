import numpy as np

def gauss_jordan(coefficient, ind_terms, decimals=1):
    coefficient = np.array(coefficient, dtype=float)
    ind_terms = np.array(ind_terms, dtype=float)
    
    n = len(ind_terms)
    equations = np.hstack([coefficient, ind_terms.reshape(-1, 1)])
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(equations[r, i]))
        equations[[i, max_row]] = equations[[max_row, i]]
        equations[i] = equations[i] / equations[i, i]
        for j in range(n):
            if j != i:
                factor = equations[j, i]
                equations[j] -= factor * equations[i]
    
    return np.round(equations[:, -1], decimals=decimals)


#Ejemplo 
A = [[1, 2, 1],
     [-1, 3, -2],
     [3, 4, -7]]

b = [8, 1, 10]

solucion = gauss_jordan(A, b)

print("Usando metodo de Gauss-Jordan")
print(f"valor de x = {solucion[0]}")
print(f"valor de y = {solucion[1]}")
print(f"valor de z = {solucion[2]}")
