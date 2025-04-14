import numpy as np

def metodo_lu(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(A)

    L = np.zeros((n, n))
    U = np.zeros((n, n))

    # Inicializamos U y L
    for i in range(n):
        L[i][i] = 1  # Diagonal de L es 1

        for j in range(i, n):
            suma = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - suma

        for j in range(i + 1, n):
            suma = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - suma) / U[i][i]

    # Sustitución hacia adelante: L * y = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

    # Sustitución hacia atrás: U * x = y
    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]

    return x
