# Métodos Numéricos en Python

Este repositorio contiene implementaciones en Python de varios **métodos numéricos fundamentales** utilizados para resolver problemas matemáticos como búsqueda de raíces y resolución de sistemas de ecuaciones lineales. Estos métodos son comúnmente usados en computación científica, ingeniería y matemáticas aplicadas.

## 🔧 Métodos Implementados

# 1. Método de Bisección
**Función:** `biseccion()`  
Encuentra una raíz de una función continua en un intervalo dado `[a, b]` utilizando el **método de bisección**.  
- **Entradas:** función `f`, intervalo `[a, b]`, tolerancia, número máximo de iteraciones  
- **Salida:** raíz aproximada, número de iteraciones  
- **Extras:** Muestra el progreso por iteración si `verbose=True`.

---

# 2. Regla de Cramer
**Función:** `cramer(coefficient, ind_terms)`  
Resuelve un sistema de ecuaciones lineales usando la **Regla de Cramer**.  
- **Entradas:**  
  - `coefficient`: Matriz de coeficientes (NxN)  
  - `ind_terms`: Vector de términos independientes (Nx1)  
- **Salida:** Vector con las soluciones

---

# 3. Descomposición LU
**Función:** `descomposicion_lu(coefficient, ind_terms)`  
Resuelve un sistema usando **descomposición LU** (algoritmo de Doolittle).  
- **Entradas:** Matriz de coeficientes y vector de términos independientes  
- **Salida:** Vector solución `x`  
- **Nota:** Incluye sustitución hacia adelante y hacia atrás.

---

# 4. Eliminación de Gauss
**Función:** `gauss(coefficient, ind_terms)`  
Resuelve un sistema lineal usando **eliminación de Gauss** con pivoteo parcial.  
- **Entradas:** Matriz de coeficientes y vector de términos independientes  
- **Salida:** Vector solución `x`

---

# 5. Gauss-Jordan
**Función:** `gauss_jordan(coefficient, ind_terms)`  
Resuelve un sistema lineal usando **eliminación Gauss-Jordan**, reduciendo la matriz a su forma escalonada reducida.  
- **Entradas:** Matriz de coeficientes y vector de términos independientes  
- **Salida:** Vector solución `x`

---

# 6. Método Iterativo de Gauss-Seidel
**Función:** `gauss_seidel(A, b, tol=1e-10, max_iter=1000)`  
Resuelve un sistema lineal iterativamente usando el **método de Gauss-Seidel**.  
- **Entradas:** Matriz de coeficientes `A`, vector de términos independientes `b`  
- **Salida:** Vector solución `x`  
- **Notas:**  
  - Usa una estimación inicial `[10, 10, 10]`  
  - Muestra los valores en cada iteración  
  - Convergencia basada en la norma de la diferencia entre iteraciones.

---

# 7. Método Iterativo de Jacobi
**Función:** `jacobi(A, b, tol=1e-10, max_iter=1000)`  
Resuelve un sistema lineal usando el **método iterativo de Jacobi**.  
- **Entradas:** Matriz de coeficientes `A`, vector de términos independientes `b`  
- **Salida:** Vector solución `x`  
- **Notas:**  
  - Estimación inicial `[10, 10, 10]`  
  - Muestra el progreso de cada iteración  
  - Se detiene si la convergencia se alcanza dentro de la tolerancia.

---

Requisitos
- Python 3.x
- `numpy`

Instala las dependencias:
```bash
pip install numpy
