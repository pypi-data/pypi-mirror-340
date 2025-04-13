def biseccion(f, a, b, tol=1e-6, max_iter=1000, verbose=True):
    if f(a) == 0:
        if verbose:
            print(f"La raíz exacta se encontró en a = {a}")
        return a, 0
    if f(b) == 0:
        if verbose:
            print(f"La raíz exacta se encontró en b = {b}")
        return b, 0
    if f(a)*f(b) >= 0:
        raise ValueError("Error, la función no cambia de signo en el rango proporcionado")
    
    iteraciones = 0
    while (b - a)/2 > tol and iteraciones < max_iter:
        xr = (a + b)/2
        fxr = f(xr)

        if verbose:
            print(f"Iteración #{iteraciones}, xr = {xr:.6f}, f(xr) = {fxr:.6e}")

        if abs(fxr) < tol:
            return xr, iteraciones
        elif f(a)*fxr < 0:
            b = xr  
        else:
            a = xr 
        iteraciones += 1

    return (a + b)/2, iteraciones

