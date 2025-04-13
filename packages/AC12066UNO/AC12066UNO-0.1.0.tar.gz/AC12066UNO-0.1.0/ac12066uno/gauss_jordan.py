# src/AC12066UNO/gauss_jordan.py

import copy

def gauss_jordan_elimination(matrix):
    """
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.

    Parámetro:
        matrix (list[list[float]]): matriz aumentada del sistema (n x n+1)

    Retorna:
        list[float]: solución del sistema

    Lanza:
        ValueError: si el sistema no tiene solución única
    """
    matrix = copy.deepcopy(matrix)  # Evita modificar la original
    n = len(matrix)

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
        if matrix[max_row][i] == 0:
            raise ValueError("Sistema sin solución única (pivote cero)")
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        pivote = matrix[i][i]
        matrix[i] = [x / pivote for x in matrix[i]]

        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                matrix[j] = [a - factor * b for a, b in zip(matrix[j], matrix[i])]

    return [fila[-1] for fila in matrix]

# Prueba de la función
"""
if __name__ == "__main__":
    sistema = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]

    resultado = gauss_jordan_elimination(sistema)
    print("Solución:", resultado)
"""