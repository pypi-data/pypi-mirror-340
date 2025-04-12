def gauss(matrix, vector):
    n = len(matrix)

    # Construir matriz aumentada
    aug_matrix = [matrix[i] + [vector[i]] for i in range(n)]

    for i in range(n):
        # Buscar el mayor valor en la columna actual
        max_row = max(range(i, n), key=lambda r: abs(aug_matrix[r][i]))
        aug_matrix[i], aug_matrix[max_row] = aug_matrix[max_row], aug_matrix[i]

        # Si el pivote es 0, puede haber infinitas soluciones o no solución
        if abs(aug_matrix[i][i]) < 1e-12:
            return "El sistema no se puede resolver por el método de Gauss (pivote cero)."

        # Eliminación hacia abajo
        for j in range(i + 1, n):
            ratio = aug_matrix[j][i] / aug_matrix[i][i]
            for k in range(i, n + 1):
                aug_matrix[j][k] -= ratio * aug_matrix[i][k]

    # Sustitución regresiva
    solution = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        if abs(aug_matrix[i][i]) < 1e-12:
            return "El sistema tiene infinitas soluciones o es incompatible."
        sum_ax = sum(aug_matrix[i][j] * solution[j] for j in range(i + 1, n))
        solution[i] = (aug_matrix[i][n] - sum_ax) / aug_matrix[i][i]

    return solution