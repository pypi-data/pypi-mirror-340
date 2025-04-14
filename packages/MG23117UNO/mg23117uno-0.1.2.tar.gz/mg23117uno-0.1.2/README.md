# MG23117UNO

Es una libreria para Python que se encarga de resolver sistemas de ecuaciones lineales y encontrar las en 
funciones las cuales son no lineales. Entonces, los métodos que vamos a encontrar en esta libreria son:

- Eliminación de Gauss (exacta con fracciones)
- Gauss-Jordan (exacta con fracciones)
- Jacobi
- Gauss-Seidel
- Bisección
- Descomposición por Lu
- Crammer

## Ejemplos de uso para cada método

### Eliminación de Gauss:
```python
from MG23117UNO import gauss_elimination  # Corrección de mayúsculas

c = [[2, 6, 1], [1, 2, -1], [5, 7, -4]]
d = [7, -1, 9]

solucion = gauss_elimination(c, d)
if solucion is not None:
    print("Solución por Gauss:", solucion)
else:
    print("El sistema no tiene solución única.")
```

## Gauss-Jordan
```python
from MG23117UNO import gauss_jordan

coefficients = [[4, 2], [-2, 1]]
ind_terms = [8, -3]

solution = gauss_jordan(coefficients, ind_terms)
print("Solución con Gauss-Jordan:")
print(solution)
```

## Jacobi:
```python
from mg23117uno import jacobi
import numpy as np

A = np.array([[3, -0.1, -0.2],
              [0.1, 7, -0.3],
              [0.3, -0.2, 10]], dtype=float)

b = np.array([7.85, -19.3, 71.4], dtype=float)

solucion = jacobi(A, b)
print(f"Solución por Jacobi: {solucion}")
```
## Gauss-Seidel
```python
from metodosnumericospy import gauss_seidel
import numpy as np

A = np.array([[4, 1, 2],
              [3, 5, 1],
              [1, 1, 3]], dtype=float)

b = np.array([4, 7, 3], dtype=float)

solucion = gauss_seidel(A, b)
print(f"Solución por Gauss-Seidel: {solucion}")
```

## Bisección
```python
from metodosnumericospy import biseccion

funcion = lambda x: x**4 + 3*x**3 - 2
raiz, iteraciones = biseccion(funcion, 0, 1)
print(f"Raíz de la función por bisección: {raiz:.6f}, encontrada en {iteraciones} iteraciones.")
```

## Descomposición LU
```python
from MG23117UNO import resolver_lu

A = [[2, 3, 1],
     [4, 7, 3],
     [6, 18, 5]]
b = [1, 2, 3]

solucion = resolver_lu(A, b)
print("Solución con descomposición LU:", solucion)
```
## Crammer
```python

from MG23117UNO import cramer

A = [[2, -1, 3],
    [1, 0, 2],
    [3, 1, 4]]

b = [5, 3, 10]

solucion = cramer(A, b)
print("Solución por Cramer:", solucion)
```
## Requisitos previos a usar la libreria

- contar con `numpy` previamente instalado.

## ¿Cómo instalar la libreria?

la librería se instala desde PyPI usando el siguiente comando:

```bash
pip install MG23117UNO
```
