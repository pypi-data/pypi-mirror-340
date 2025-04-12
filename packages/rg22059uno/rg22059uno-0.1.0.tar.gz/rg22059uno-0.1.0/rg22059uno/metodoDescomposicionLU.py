def LU(A):
    n = len(A)
    L = [[0.0]*n for _ in range(n)]
    U = [[0.0]*n for _ in range(n)]

    for i in range(n):
        # Calcular los elementos de la matriz U
        for k in range(i, n):
            suma = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - suma

        # Verificar división por cero
        if U[i][i] == 0:
            return None, None  # No se puede descomponer con Doolittle

        # Calcular los elementos de la matriz L
        for k in range(i, n):
            if i == k:
                L[k][i] = 1.0  # Diagonal de L es 1
            else:
                suma = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (A[k][i] - suma) / U[i][i]

    return L, U

# Sustitución hacia adelante: resuelve Ly = b
def sustitucion_adelante(L, b):
    n = len(L)
    y = [0.0]*n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j]*y[j] for j in range(i))
    return y

# Sustitución hacia atrás: resuelve Ux = y
def sustitucion_atras(U, y):
    n = len(U)
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        suma = sum(U[i][j]*x[j] for j in range(i+1, n))
        if U[i][i] == 0:
            raise ValueError("No se puede resolver: división por cero en sustitución hacia atrás")
        x[i] = (y[i] - suma) / U[i][i]
    return x

# Función principal que resuelve Ax = b usando LU
def descomposicionLU(A, b):
    L, U = LU(A)
    if L is None or U is None:
        return "El sistema no se puede resolver con descomposición LU (división por cero o matriz singular)."

    y = sustitucion_adelante(L, b)
    x = sustitucion_atras(U, y)
    return x