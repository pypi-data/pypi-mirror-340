# MS23056UNO

Librería hecha en Python para resolver sistemas de ecuaciones lineales y no lineales.

## Métodos incluidos

- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección

## Instalación

```bash
pip install MS23056UNO
```

## Ejemplo de uso

```python
from MS23056UNO.gauss import gauss_elimination

a = [[2, -1, 1],
     [3, 3, 9],
     [3, 3, 5]]
b = [2, -1, 4]

sol = gauss_elimination(a, b)
print("Solución:", sol)
```

## Autor

Tu Nombre MS23056