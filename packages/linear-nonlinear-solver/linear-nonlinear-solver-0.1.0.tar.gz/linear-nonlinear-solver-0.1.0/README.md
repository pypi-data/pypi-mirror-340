# Proyecto de Resolución de Sistemas de Ecuaciones Lineales y No Lineales

Este proyecto proporciona una librería en Python para resolver sistemas de ecuaciones lineales y no lineales utilizando varios métodos numéricos. La librería incluye implementaciones de los métodos de eliminación de Gauss, Gauss-Jordan, Cramer, descomposición LU, Jacobi, Gauss-Seidel y bisección.

## Métodos Implementados

- **Eliminación de Gauss**: Resuelve sistemas de ecuaciones lineales mediante la eliminación de variables.
- **Gauss-Jordan**: Extensión del método de Gauss que transforma la matriz en su forma reducida.
- **Cramer**: Utiliza determinantes para resolver sistemas de ecuaciones lineales.
- **Descomposición LU**: Descompone una matriz en el producto de una matriz triangular inferior y una matriz triangular superior.
- **Método de Jacobi**: Un método iterativo para encontrar soluciones de sistemas de ecuaciones lineales.
- **Método de Gauss-Seidel**: Otro método iterativo que mejora la convergencia respecto al método de Jacobi.
- **Bisección**: Encuentra raíces de funciones no lineales en un intervalo dado.

## Instalación

Para instalar la librería, usar `pip`:

```
pip install linear-nonlinear-solver
```

## Uso

A continuación se presentan ejemplos de cómo utilizar algunos de los métodos disponibles en la librería:

### Ejemplo de Eliminación de Gauss

```python
from linear_nonlinear_solver.gauss import eliminar_gauss

# Definir la matriz de coeficientes y el vector de términos independientes
A = [[3, 2, -4], [2, 3, 3], [5, -3, 1]]
b = [3, 15, 14]

# Resolver el sistema
solucion = eliminar_gauss(A, b)
print(solucion)
```

### Ejemplo de Bisección

```python
from linear_nonlinear_solver.bisection import biseccion

# Definir la función y el intervalo
def f(x):
    return x**3 - x - 2

# Encontrar la raíz
raiz = biseccion(f, 1, 2)
print(raiz)
```

## Pruebas

El proyecto incluye pruebas unitarias para cada uno de los métodos implementados. Puedes ejecutar las pruebas utilizando `pytest`:

```
pytest tests/
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.