import numpy as np

def eliminacion_gauss_solver(A, b):
    """
    Resuelve Ax = b usando eliminación de Gauss.
    
    Args:
        A: Matriz de coeficientes (numpy array 2D).
        b: Vector de términos independientes (numpy array 1D).
    
    Returns:
        x: Solución del sistema (numpy array 1D).
    
    --------
    Ejemplo de uso:
    >>> A = np.array([
    >>>     [1, 1, 1],
    >>>     [2, 3, -4],
    >>>     [1, -1, 1]
    >>> ], dtype=float)
    >>> b = np.array([1,9,-1], dtype=float)
    >>> eliminacion_gauss_solver(A, b)
    """
    n = len(b)
    Ab = np.column_stack((A, b)).astype(float)
    
    # Eliminación hacia adelante
    for i in range(n):
        Ab[i] = Ab[i] / Ab[i, i]
        for j in range(i + 1, n):
            Ab[j] -= Ab[j, i] * Ab[i]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])
    
    return x
