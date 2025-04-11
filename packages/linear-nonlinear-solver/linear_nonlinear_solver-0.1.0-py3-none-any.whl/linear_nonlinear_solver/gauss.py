def eliminar_gauss(matriz, terminos_independientes):
    n = len(matriz)

    # Aplicar eliminación de Gauss
    for i in range(n):
        # Buscar el máximo en la columna actual
        max_fila = i + max(range(n - i), key=lambda k: abs(matriz[i + k][i]))
        matriz[i], matriz[max_fila] = matriz[max_fila], matriz[i]
        terminos_independientes[i], terminos_independientes[max_fila] = terminos_independientes[max_fila], terminos_independientes[i]

        # Hacer ceros debajo del pivote
        for j in range(i + 1, n):
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            terminos_independientes[j] -= factor * terminos_independientes[i]

    # Sustitución hacia atrás
    solucion = [0] * n
    for i in range(n - 1, -1, -1):
        solucion[i] = (terminos_independientes[i] - sum(matriz[i][j] * solucion[j] for j in range(i + 1, n))) / matriz[i][i]

    return solucion