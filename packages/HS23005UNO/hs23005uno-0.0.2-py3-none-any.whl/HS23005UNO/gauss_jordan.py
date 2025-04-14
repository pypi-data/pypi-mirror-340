import numpy as np

def gauss_jordan(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    # Formamos la matriz aumentada
    aug = np.hstack((A, b.reshape(-1, 1)))

    # Proceso de Gauss-Jordan
    for i in range(n):
        # Pivote
        if aug[i][i] == 0:
            raise ValueError("División por cero detectada.")
        aug[i] = aug[i] / aug[i][i]  # Hacer el pivote 1
        for j in range(n):
            if i != j:
                aug[j] = aug[j] - aug[j][i] * aug[i]

    # El resultado está en la última columna
    return aug[:, -1]
