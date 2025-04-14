import numpy as np

def gauss_elimination(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    # Triangular superior
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError("División por cero detectada.")
        for j in range(i+1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] = A[j][k] - ratio * A[i][k]
            b[j] = b[j] - ratio * b[i]

    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - suma) / A[i][i]
    
    return x
