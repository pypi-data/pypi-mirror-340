# MR23013UNO

Librería para resolver sistemas de ecuaciones lineales y no lineales.

## Instalación

```bash
pip install mr23013uno
```

## Métodos incluidos

- Eliminación de Gauss
- Bisección
- Regla de Cramer
- Descomposición LU
- Método de Jacobi
- Método de Gauss-Seidel
- Método de Bisección

## Ejemplo de uso

```python
from mr23013uno.lineales import gauss_elimination
A = [[3, 2], [1, 2]]
b = [5, 5]
print(gauss_elimination(A, b))
```
