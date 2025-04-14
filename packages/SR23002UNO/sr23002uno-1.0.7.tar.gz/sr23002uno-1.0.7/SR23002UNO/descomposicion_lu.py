import numpy as np

def dcp_lu_solver(A, b):
    """
    Resuelve ecuaciones lineales A*x = b usando el método LU.
    
    Args:
        A: Matriz de coeficientes (numpy.ndarray).
        b: Vector de términos independientes (numpy.ndarray).
        
    Returns:
        x: Solución del sistema (numpy array 1D).
    
    Raises:
        ValueError: Si la matriz es singular o no cuadrada.

    
    Ejemplo de uso:
    --------
    >>> A = np.array([
    >>>     [25, 5, 1],
    >>>     [64, 8, 1],
    >>>     [144, 12, 1]
    >>> ], dtype=float)
    >>> b = np.array([106.8, 177.2, 279.2], dtype=float)
    >>> dcp_lu_solver(A, b)
    """
    n = len(b)
    L = np.eye(n)
    U = A.copy().astype(float)
    P = np.eye(n)  # Matriz de permutación

    for k in range(n - 1):
        # Pivoteo parcial
        pivot_row = np.argmax(np.abs(U[k:, k])) + k
        if pivot_row != k:
            U[[k, pivot_row]] = U[[pivot_row, k]]
            P[[k, pivot_row]] = P[[pivot_row, k]]
            if k > 0:
                L[[k, pivot_row], :k] = L[[pivot_row, k], :k]

        if U[k, k] == 0:
            raise ValueError("Matriz singular: no se puede factorizar")

        # Eliminación
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]

    # Sustitución Ly = Pb
    y = np.zeros(n)
    Pb = np.dot(P, b)
    for i in range(n):
        y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

    # Sustitución Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    return x
