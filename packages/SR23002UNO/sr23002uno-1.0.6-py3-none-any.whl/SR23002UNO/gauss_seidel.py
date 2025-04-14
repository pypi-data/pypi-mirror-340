import numpy as np

def gauss_seidel_solver(A, b, initial_guess=None, tol=1e-6, max_iter=1000):
    """
    Resuelve el sistema Ax = b usando el método de Gauss-Seidel.
    
    Parámetros:
        A: Matriz de coeficientes (numpy array 2D).
        b: Vector de términos independientes (numpy array 1D).
        initial_guess: Valores iniciales para las variables (opcional).
        tol: Tolerancia para la convergencia (por defecto 1e-6).
        max_iter: Máximo número de iteraciones (por defecto 1000).
    
    Retorna:
        x: Solución del sistema (numpy array 1D).
        iterations: Número de iteraciones realizadas.
    
    Ejemplo de uso:
    --------
    >>> A = np.array([
    >>>     [10, 3, 1],
    >>>     [5, -10, 3],
    >>>     [1, 3, 10]
    >>> ])
    >>> b = np.array([14, -5, 14])
    >>> gauss_seidel_solver(A, b)
    """
    n = len(b)
    x = initial_guess.copy() if initial_guess is not None else np.zeros(n)
    
    for iterations in range(1, max_iter + 1):
        x_old = x.copy()
        
        for i in range(n):
            sum_ax = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x_old[i + 1:])
            x[i] = (b[i] - sum_ax) / A[i, i]
        
        # Criterio de convergencia
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            break
    
    return x, iterations