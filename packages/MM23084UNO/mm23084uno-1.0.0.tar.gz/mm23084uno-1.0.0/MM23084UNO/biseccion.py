def biseccion(funcion, a, b, tolerancia=1e-10, max_iteraciones=100):
    """
    Encuentra la raíz de una función en un intervalo [a, b] usando el método de bisección.
    """
    if funcion(a) * funcion(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    for _ in range(max_iteraciones):
        c = (a + b) / 2
        if abs(funcion(c)) < tolerancia or (b - a) / 2 < tolerancia:
            return c
        if funcion(c) * funcion(a) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2