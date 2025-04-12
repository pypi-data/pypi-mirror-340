def resolver_cramer(matriz, vector):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.
    """
    import copy
    import numpy as np
    n = len(matriz)
    det_principal = np.linalg.det(matriz)
    if det_principal == 0:
        raise ValueError("El sistema no tiene solución única")
    soluciones = []
    for i in range(n):
        matriz_modificada = copy.deepcopy(matriz)
        for j in range(n):
            matriz_modificada[j][i] = vector[j]
        soluciones.append(np.linalg.det(matriz_modificada) / det_principal)
    return soluciones