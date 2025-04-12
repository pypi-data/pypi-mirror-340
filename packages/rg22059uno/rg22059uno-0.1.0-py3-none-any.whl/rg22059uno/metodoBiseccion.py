def biseccion(f, a, b, tol=1e-6, max_iter=1000, verbose=False):
    """
    Método de Bisección para encontrar una raíz de f(x) = 0 en el intervalo [a, b].

    Parámetros:
        f (function): Función a evaluar.
        a (float): Límite inferior del intervalo.
        b (float): Límite superior del intervalo.
        tol (float): Tolerancia para la aproximación de la raíz.
        max_iter (int): Número máximo de iteraciones.
        verbose (bool): Si True, imprime las iteraciones.

    Retorna:
        (raíz aproximada, número de iteraciones)
    """
    if f(a)*f(b) >= 0:
        raise ValueError("Error: La función no cambia de signo en el intervalo dado.")

    iteraciones = 0
    while (b - a)/2 > tol and iteraciones < max_iter:
        xr = (a + b) / 2
        if verbose:
            print(f"Iteración #{iteraciones}, xr = {xr:.6f}, f(xr) = {f(xr):.6f}")
        if f(xr) == 0:
            return xr, iteraciones
        elif f(a)*f(xr) < 0:
            b = xr
        else:
            a = xr
        iteraciones += 1

    return (a + b)/2, iteraciones