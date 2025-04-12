def resolver_lu(matriz, vector):
    """
    Resuelve un sistema de ecuaciones lineales usando descomposición LU.
    """
    import numpy as np
    from scipy.linalg import lu
    P, L, U = lu(matriz)
    y = np.linalg.solve(L, np.dot(P, vector))
    x = np.linalg.solve(U, y)
    return x.tolist()