def resolver_gauss_seidel(matriz, vector, iteraciones=100, tolerancia=1e-10):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    """
    n = len(matriz)
    x = [0] * n
    for _ in range(iteraciones):
        x_nuevo = x.copy()
        for i in range(n):
            suma1 = sum(matriz[i][j] * x_nuevo[j] for j in range(i))
            suma2 = sum(matriz[i][j] * x[j] for j in range(i+1, n))
            x_nuevo[i] = (vector[i] - suma1 - suma2) / matriz[i][i]
        if all(abs(x_nuevo[i] - x[i]) < tolerancia for i in range(n)):
            break
        x = x_nuevo
    return x