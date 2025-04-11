# CG23016UNO

Una libreria en Python para resolver sistemas de ecuaciones lineales y no lineales.

## Instalación

```bash
pip install CG23016UNO
```

## Métodos incluidos

### Lineales

- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Jacobi
- Gauss-Seidel

### No Lineales

- Bisección

## Ejemplo

```python
from CG23016UNO import gauss_elimination

A = [[2, 1], [5, 7]]
b = [11, 13]

x = gauss_elimination(A, b)
print("Solución:", x)
```
