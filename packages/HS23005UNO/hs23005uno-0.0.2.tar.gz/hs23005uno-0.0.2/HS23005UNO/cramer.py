import numpy as np

def metodo_cramer(A, b):
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única (determinante es cero)")

    soluciones = []
    for i in range(n):
        A_temp = A.copy()
        A_temp[:, i] = b  # reemplazamos la columna i por el vector b
        det_Ai = np.linalg.det(A_temp)
        soluciones.append(det_Ai / det_A)

    return np.array(soluciones)
