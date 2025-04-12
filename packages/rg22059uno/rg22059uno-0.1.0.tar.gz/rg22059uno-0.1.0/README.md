# Corto #1 -- Publicación de librería en PyPI

## Descripción:

Proyecto: Crear una librería en Python y publicarla de manera que se pueda instalar en otros equipos a través del comando pip install.

Función: La librería es capaz de resolver sistemas de ecuaciones lineales y no lineales a través de los siguientes métodos:

- **Eliminación de Gauss**
- **Gauss-Jordan**
- **Cramer**
- **Descomposición LU**
- **Jacobi**
- **Gauss-Seidel**
- **Bisección**

## Requisitos

Python 3.x

No se requieren librerías externas

## Instalación desde PyPI

```bash
pip install rg22069uno
```

## Método de Gauss

**Pasos para utilizar el método de Gauss:**

1. Importar la función desde el módulo

```python
from rg22069uno import gauss
```

2. Definir la ecuación a resolver

```python
A = [
    [2, 1, -1],
    [-3, -1, 2],
    [-2, 1, 2]
]

b = [8, -11, -3]
```

3. Llamar a la función gauss

```python
resultado = gauss(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Gauss-Jordan

**Pasos para utilizar el método de Gauss-Jordan:**

1. Importar la función desde el módulo

```python
from rg22069uno import gaussJordan
```

2. Definir la ecuación a resolver

```python
A = [
    [2, -1, 1],
    [1, 2, -1],
    [3, -1, 4]
]

b = [5, 3, 10]
```

3. Llamar a la función gaussJordan

```python
resultado = gaussJordan(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Cramer

**Pasos para utilizar el método de Cramer:**

1. Importar la función desde el módulo

```python
from rg22069uno import cramer
```

2. Definir la ecuación a resolver

```python
A = [
    [1, 1, 1],
    [2, -1, 2],
    [3, 2, 3]
]

b = [6, 7, 12]
```

3. Llamar a la función cramer

```python
resultado = cramer(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Descomposición LU

**Pasos para utilizar el método de Descomposición LU:**

1. Importar la función desde el módulo

```python
from rg22069uno import descomposicionLU
```

2. Definir la ecuación a resolver

```python
A = [
    [4, -2, 1],
    [1, 3, -2],
    [2, -1, 4]
]

b = [7, 5, 10]
```

3. Llamar a la función descomposicionLU

```python
resultado = descomposicionLU(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Jacobi

**Pasos para utilizar el método de Jacobi:**

1. Importar la función desde el módulo

```python
from rg22069uno import jacobi
```

2. Definir la ecuación a resolver

```python
A = [
    [4, -2, 1],
    [2, 3, 2],
    [1, -1, 4]
]

b = [10, 12, 5]
```

3. Llamar a la función jacobi

```python
resultado = jacobi(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Gauss-Seidel

**Pasos para utilizar el método de Gauss-Seidel:**

1. Importar la función desde el módulo

```python
from rg22069uno import gaussSeidel
```

2. Definir la ecuación a resolver

```python
A = [
    [3, -1, 1],
    [1, 2, 2],
    [2, -3, 4]
]

b = [10, 11, 5]
```

3. Llamar a la función gaussSeidel

```python
resultado = gaussSeidel(A, b)
```

4. Imprimir resultado

```python
#Imprimir solo el resultado
print(resultado)

#Imprimir el resultado con nombre de variables
if isinstance(resultado, list):
    for i, val in enumerate(resultado):
        print(f"x{i + 1}: {val}")
else:
    print(resultado)
```

## Método de Bisección

**Pasos para utilizar el método de Bisección:**

1. Importar la función desde el módulo

```python
from rg22069uno import biseccion
```

2. Definir la función a resolver

```python
f = lambda x: x**3 - 4*x**2 + 5*x - 2
```

3. Llamar a la función biseccion

```python
raiz, iteraciones = biseccion(f, 1, 2, tol=1e-6, max_iter=1000, verbose=True)
```

4. Imprimir resultado

```python
print(f"Raíz aproximada: {raiz:.6f}, Iteraciones: {iteraciones}")
```

## Licencia

Este proyecto está bajo la Licencia MIT.
