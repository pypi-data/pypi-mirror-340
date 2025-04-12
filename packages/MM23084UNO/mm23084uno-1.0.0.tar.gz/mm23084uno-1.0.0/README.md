## Métodos disponibles:

- Eliminación de Gauss
- Gauss-Jordan
- Regla de Cramer
- Descomposición LU
- Método de Jacobi
- Método de Gauss-Seidel
- Método de Bisección

## Instalación (una vez publicada en PyPI)
```bash
pip install sistematix-mm23084
```

## Ejemplo de uso
```python
from sistematix import resolver_gauss

A = [[2, -1, 1], [1, 3, 2], [1, -1, 2]]
b = [2, 0, 3]
solucion = resolver_gauss(A, b)
print(solucion)
```

## Autor
Ricardo Mora - mm23084@ues.edu.sv