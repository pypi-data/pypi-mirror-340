def resolver_gauss_jordan(matriz, vector):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    """
    n = len(matriz)
    for i in range(n):
        divisor = matriz[i][i]
        if divisor == 0:
            raise ValueError("División por cero durante la eliminación")
        for j in range(n):
            matriz[i][j] /= divisor
        vector[i] /= divisor
        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(n):
                    matriz[k][j] -= factor * matriz[i][j]
                vector[k] -= factor * vector[i]
    return vector