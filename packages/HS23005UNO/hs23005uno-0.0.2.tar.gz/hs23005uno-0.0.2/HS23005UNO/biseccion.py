def metodo_biseccion(funcion, a, b, tolerancia=1e-7, max_iter=100):
    if funcion(a) * funcion(b) >= 0:
        raise ValueError("La funcion debe tener signos opuestos en los extremos [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(funcion(c)) < tolerancia or (b - a) / 2 < tolerancia:
            return c
        if funcion(a) * funcion(c) < 0:
            b = c
        else:

            a = c

    return (a + b / 2) 