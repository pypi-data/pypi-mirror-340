import numpy as np

def metodo_jacobi(A, b, tolerancia=1e-10, max_iter=100):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    x = np.zeros(n)
    x_anterior = np.zeros(n)

    for iteracion in range(max_iter):
        for i in range(n):
            suma = sum(A[i][j] * x_anterior[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i][i]


        if np.linalg.norm(x - x_anterior, ord=np.inf) < tolerancia:
            return x
        
        x_anterior = x.copy()

    return x