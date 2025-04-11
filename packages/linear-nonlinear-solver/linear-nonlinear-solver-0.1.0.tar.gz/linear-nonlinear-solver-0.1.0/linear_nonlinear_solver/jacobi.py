def metodo_jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    """
    Resuelve el sistema de ecuaciones lineales Ax = b utilizando el método de Jacobi.

    Parámetros:
    A : array_like
        Matriz de coeficientes.
    b : array_like
        Vector de términos independientes.
    x0 : array_like, opcional
        Aproximación inicial (por defecto es un vector de ceros).
    tol : float, opcional
        Tolerancia para la convergencia (por defecto es 1e-10).
    max_iter : int, opcional
        Número máximo de iteraciones (por defecto es 100).

    Retorna:
    x : array_like
        Solución del sistema de ecuaciones.
    """
    import numpy as np

    n = len(b)
    x = np.zeros_like(b) if x0 is None else x0
    for it_count in range(max_iter):
        x_new = np.zeros_like(x)
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise ValueError("El método de Jacobi no convergió en el número máximo de iteraciones.")