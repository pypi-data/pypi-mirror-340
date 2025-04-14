import numpy as np

def metodo_gauss_sediel(A, b, tolerancia=1e-10, max_iter=100):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)
    x = np.zeros(n)

    for iteracion in range(max_iter):
        x_nuevo = np.copy(x)

        for i in range(n):
            suma1 = sum(A[i][j] * x_nuevo[j] for j in range(i))
            suma2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_nuevo[i] = (b[i] - suma1 - suma2) / A[i][i]

        if np.linalg.norm(x_nuevo - x, ord=np.inf) < tolerancia:
            return x_nuevo
        
        x = x_nuevo.copy()

    
    return x
    