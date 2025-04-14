import numpy as np

def jacobi_solver(A, b, tol=1e-6, max_iter=1000):
    """
    Resuelve Ax = b usando el método iterativo de Jacobi.
    
    Args:
        A: Matriz de coeficientes (numpy array 2D cuadrada y diagonalmente dominante).
        b: Vector de términos independientes (numpy array 1D).
        tol: Tolerancia para la convergencia (por defecto 1e-6).
        max_iter: Máximo número de iteraciones (por defecto 1000).
        
    Returns:
        x: Solución aproximada (numpy array 1D).
        iterations: Número de iteraciones realizadas.
    
    Excepciones:
    --------
        ValueError: Si la matriz no es cuadrada o diagonalmente dominante.
    
    Ejemplo de uso:
    --------
    >>> A = np.array([
    >>>     [10, 3, 1],
    >>>     [5, -10, 3],
    >>>     [1, 3, 10]
    >>> ])
    >>> b = np.array([14, -5, 14])
    >>> jacobi_solver(A, b)
    """
    n = len(b)
    if A.shape != (n, n):
        raise ValueError("La matriz A debe ser cuadrada")

    # Verificar dominancia diagonal (opcional pero recomendado)
    if not np.all(2 * np.abs(np.diag(A)) >= np.sum(np.abs(A), axis=1)):
        print("Advertencia: La matriz puede no ser diagonalmente dominante")

    x = np.zeros(n)
    x_new = np.zeros(n)
    
    for iteration in range(max_iter):
        for i in range(n):
            sigma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - sigma) / A[i, i]

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            break

        x = x_new.copy()
    
    return x_new, iteration + 1
