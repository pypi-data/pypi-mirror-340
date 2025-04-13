def biseccion_solver(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de f(x) = 0 en [a, b].
    
    Args:
        f: Función a evaluar. Ejemplo f(x) = x**4 + 7*x**3 -7
        a: Extremo izquierdo(Inferior) del intervalo.
        b: Extremo derecho(Superior) del intervalo.
        tol: Tolerancia para la raiz. Por defecto es 1e-6 (0.000001).
        max_iter: Máximo de iteraciones. Por defecto es 100.
    
    Returns:
        float: Aproximación de la raíz
    """
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a)/2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2



# x**3 + 2*x**2 + 10*x -20
#print(biseccion_solver(lambda x: x**3 + 2*x**2 + 10*x - 20, -7, 16))

# x**5 - 3*x**2 + 1
# print(biseccion_solver(lambda x: x**5 -3*x**2+1, 1, -1))