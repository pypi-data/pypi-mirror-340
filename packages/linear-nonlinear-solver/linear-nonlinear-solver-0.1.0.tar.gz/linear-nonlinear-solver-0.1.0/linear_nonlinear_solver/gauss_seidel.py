def metodo_gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b utilizando el método de Gauss-Seidel.

    Parámetros:
    A : array_like
        Matriz de coeficientes del sistema.
    b : array_like
        Vector de términos independientes.
    x0 : array_like, opcional
        Aproximación inicial (por defecto es un vector de ceros).
    tol : float, opcional
        Tolerancia para la convergencia (por defecto es 1e-10).
    max_iter : int, opcional
        Número máximo de iteraciones (por defecto es 1000).

    Retorna:
    x : array_like
        Solución del sistema de ecuaciones.
    """
    n = len(b)
    x = x0 if x0 is not None else np.zeros(n)

    for k in range(max_iter):
        x_old = np.copy(x)
        for i in range(n):
            suma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
            x[i] = (b[i] - suma) / A[i, i]

        # Verificar la convergencia
        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x

    raise ValueError("El método de Gauss-Seidel no convergió en el número máximo de iteraciones.")