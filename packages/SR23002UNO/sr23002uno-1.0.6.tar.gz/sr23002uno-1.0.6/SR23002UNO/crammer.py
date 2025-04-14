import numpy as np

def cramer_solver(A, b):
    """
    Encuentra los coeficientes de la solución de las ecuaciones lineales A*x = b.
    
    Args:
        A: Matriz de coeficientes de las ecuaciones lineales.
        b: Vector de constantes de las ecuaciones lineales.
    
    Returns:
        np.array: Vector de coeficientes de la solución de las ecuaciones lineales.
    
    Ejemplo de uso:
    --------
    >>> A = np.array([[2, -1, 1], [0, 2, -1], [1, -1, 0]])
    >>> b = np.array([3, 1, 1])
    >>> cramer_solver(A, b)
    """
    det_A = np.linalg.det(A) # Determinante de A
    n = len(b) # Longuitud del vector
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x
