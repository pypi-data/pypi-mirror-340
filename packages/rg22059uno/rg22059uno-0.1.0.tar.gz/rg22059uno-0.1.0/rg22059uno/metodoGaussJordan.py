def gaussJordan(matrix, vector):
    n = len(matrix)
    # Matriz aumentada
    aug = [row + [val] for row, val in zip(matrix, vector)]

    for i in range(n):
        # Encontrar fila con el valor absoluto más alto en la columna actual
        max_row = max(range(i, n), key=lambda r: abs(aug[r][i]))
        aug[i], aug[max_row] = aug[max_row], aug[i]

        # Verificar si el pivote es cero
        if abs(aug[i][i]) < 1e-12:
            # Verifica si la fila es completamente cero con un término independiente no cero
            if any(abs(aug[i][j]) > 1e-12 for j in range(n)):
                return "El sistema no tiene solución (incompatible)."
            else:
                return "El sistema tiene infinitas soluciones (indeterminado)."

        # Normalizar la fila pivote
        divisor = aug[i][i]
        aug[i] = [x / divisor for x in aug[i]]

        # Hacer cero el resto de la columna
        for j in range(n):
            if j != i:
                ratio = aug[j][i]
                aug[j] = [aug[j][k] - ratio * aug[i][k] for k in range(n + 1)]

    # Extraer soluciones
    solution = [aug[i][-1] for i in range(n)]
    return solution