def resolver_jacobi(matriz, vector, iteraciones=100, tolerancia=1e-10):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    """
    n = len(matriz)
    x = [0] * n
    for _ in range(iteraciones):
        x_nuevo = x.copy()
        for i in range(n):
            suma = sum(matriz[i][j] * x[j] for j in range(n) if j != i)
            x_nuevo[i] = (vector[i] - suma) / matriz[i][i]
        if all(abs(x_nuevo[i] - x[i]) < tolerancia for i in range(n)):
            break
        x = x_nuevo
    return x