# src/AC12066UNO/gauss.py

import copy

def gauss_elimination(matrix):
    """
    Resuelve un sistema de ecuaciones lineales usando Eliminación de Gauss.

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

        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n + 1):
                matrix[j][k] -= factor * matrix[i][k]

    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        suma = sum(matrix[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (matrix[i][n] - suma) / matrix[i][i]

    return x

# Prueba de la función
#"""
if __name__ == "__main__":
    sistema = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]

    resultado = gauss_elimination(sistema)
    print("Solución:", resultado)
#"""