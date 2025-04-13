import numpy as np

def cramer_solver(A, b):
    det_A = np.linalg.det(A) # Determinante de A
    n = len(b) # Longuitud del vector
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x


# A = np.array([[1, 1, 1], [2, 3, -2], [3, -2, 1]])
# b = np.array([4, 4, -1])
# sol =cramer_solver(A, b)
# for i in sol:
#     print(round(i, 2))

# referencia de la imagen "cramer-example.png"
# A = np.array([[2, -1, 1], [0, 2, -1], [1, -1, 0]])
# b = np.array([3, 1, 1])
# sol =cramer_solver(A, b)
# for i in sol:
#     print(round(i, 2))