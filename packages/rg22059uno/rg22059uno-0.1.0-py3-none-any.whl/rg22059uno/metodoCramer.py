# Función recursiva para calcular el determinante de una matriz cuadrada
def determinante(matriz):
    n = len(matriz)

    # Caso base: matriz 1x1
    if n == 1:
        return matriz[0][0]

    # Caso base: matriz 2x2 (fórmula directa)
    if n == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]

    # Caso general: expansión por cofactores de la primera fila
    det = 0
    for c in range(n):
        # Crear submatriz eliminando la primera fila y columna c
        menor = [fila[:c] + fila[c+1:] for fila in matriz[1:]]
        # Sumar cofactor correspondiente
        det += ((-1)**c) * matriz[0][c] * determinante(menor)
    return det

# Función para reemplazar una columna en una matriz
def reemplazar_columna(matriz, columna, nueva_columna):
    nueva_matriz = []
    for i in range(len(matriz)):
        fila = list(matriz[i])             # Copia la fila original
        fila[columna] = nueva_columna[i]   # Reemplaza el valor en la columna deseada
        nueva_matriz.append(fila)
    return nueva_matriz

# Función principal que aplica el método de Cramer
def cramer(A, b):
    n = len(A)

    # Verifica que A sea una matriz cuadrada
    if any(len(fila) != n for fila in A):
        return "La matriz A no es cuadrada. Cramer no aplica."

    # Calcula el determinante de A
    det_A = determinante(A)

    # Si el determinante es 0, no se puede aplicar Cramer
    if abs(det_A) < 1e-12:
        return "El sistema no se puede resolver con Cramer (det(A) = 0)."

    # Lista para almacenar las soluciones xi
    soluciones = []

    # Iterar por cada incógnita
    for i in range(n):
        # Crear una nueva matriz Ai reemplazando la columna i por el vector b
        Ai = reemplazar_columna(A, i, b)
        # Calcular el determinante de Ai
        det_Ai = determinante(Ai)
        # xi = det(Ai) / det(A)
        soluciones.append(det_Ai / det_A)

    return soluciones