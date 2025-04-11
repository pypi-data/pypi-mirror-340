def descomponer_lu(matriz):
    n = len(matriz)
    L = [[0] * n for _ in range(n)]
    U = [[0] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1  # Diagonal de L es 1

        for j in range(i, n):
            U[i][j] = matriz[i][j]
            for k in range(i):
                U[i][j] -= L[i][k] * U[k][j]

        for j in range(i + 1, n):
            L[j][i] = matriz[j][i]
            for k in range(i):
                L[j][i] -= L[j][k] * U[k][i]
            L[j][i] /= U[i][i]

    return L, U


def resolver_lu(matriz, vector):
    L, U = descomponer_lu(matriz)
    n = len(vector)

    # Sustitución hacia adelante
    y = [0] * n
    for i in range(n):
        y[i] = vector[i]
        for j in range(i):
            y[i] -= L[i][j] * y[j]

    # Sustitución hacia atrás
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i]
        for j in range(i + 1, n):
            x[i] -= U[i][j] * x[j]
        x[i] /= U[i][i]

    return x