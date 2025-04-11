# FC16004UNO

Una librería en Python para resolver sistemas de ecuaciones lineales y no lineales usando métodos numéricos como:

- Eliminación de Gauss
- Gauss-Jordan
- Regla de Cramer
- Descomposición LU
- Métodos iterativos: Jacobi y Gauss-Seidel
- Método de Bisección

## Instalación

```bash
pip install FC16004UNO
```

## Uso

```python
from fc16004uno.lineal import eliminacion_gauss

A = [[2, -1, 1], [3, 3, 9], [3, 3, 5]]
b = [8, 0, -6]
sol = eliminacion_gauss.gauss_elimination(A, b)
print(sol)
```