def biseccion(funcion, a, b, tol=1e-7, max_iter=1000):
    if funcion(a) * funcion(b) >= 0:
        raise ValueError("La función debe tener diferentes signos en los extremos del intervalo [a, b].")

    for i in range(max_iter):
        c = (a + b) / 2  # Punto medio
        if abs(funcion(c)) < tol or (b - a) / 2 < tol:
            return c  # Raíz encontrada

        if funcion(c) * funcion(a) < 0:
            b = c  # La raíz está en el intervalo [a, c]
        else:
            a = c  # La raíz está en el intervalo [c, b]

    raise ValueError("No se encontró la raíz en el número máximo de iteraciones.")