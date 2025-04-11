def resolver_cramer(matriz_coeficientes, vector_terminos):
    import numpy as np

    # Verificar que la matriz de coeficientes sea cuadrada
    n = len(matriz_coeficientes)
    if n != len(vector_terminos):
        raise ValueError("La matriz de coeficientes y el vector de términos deben tener dimensiones compatibles.")

    # Calcular el determinante de la matriz de coeficientes
    det_matriz = np.linalg.det(matriz_coeficientes)
    if det_matriz == 0:
        raise ValueError("El sistema no tiene solución única (determinante cero).")

    # Inicializar la lista de soluciones
    soluciones = []

    # Aplicar la regla de Cramer
    for i in range(n):
        # Crear una copia de la matriz de coeficientes
        matriz_temp = np.copy(matriz_coeficientes)
        # Reemplazar la columna i con el vector de términos
        matriz_temp[:, i] = vector_terminos
        # Calcular el determinante de la nueva matriz
        det_temp = np.linalg.det(matriz_temp)
        # Calcular la solución para la variable i
        soluciones.append(det_temp / det_matriz)

    return soluciones