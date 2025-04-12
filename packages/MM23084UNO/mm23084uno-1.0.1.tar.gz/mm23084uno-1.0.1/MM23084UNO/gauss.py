def resolver_gauss(matriz, vector):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de eliminación de Gauss.
    Parámetros:
        matriz: lista de listas con los coeficientes del sistema
        vector: lista con los términos independientes
    Retorna:
        Una lista con las soluciones del sistema
    """
    n = len(matriz)
    for i in range(n):
        # Pivoteo
        max_fila = max(range(i, n), key=lambda k: abs(matriz[k][i]))
        matriz[i], matriz[max_fila] = matriz[max_fila], matriz[i]
        vector[i], vector[max_fila] = vector[max_fila], vector[i]

        # Eliminación
        for j in range(i+1, n):
            if matriz[i][i] == 0:
                raise ValueError("División por cero durante la eliminación")
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            vector[j] -= factor * vector[i]

    # Sustitución hacia atrás
    x = [0] * n
    for i in range(n-1, -1, -1):
        suma = sum(matriz[i][j] * x[j] for j in range(i+1, n))
        x[i] = (vector[i] - suma) / matriz[i][i]
    return x