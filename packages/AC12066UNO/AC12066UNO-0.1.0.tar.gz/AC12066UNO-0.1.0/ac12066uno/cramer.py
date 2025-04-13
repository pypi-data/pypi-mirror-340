# src/AC12066UNO/cramer.py

import copy

def determinante(matrix):
    """
    Calcula el determinante de una matriz cuadrada mediante recursión (expansión de cofactores).
    """
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        # Fórmula directa 2x2
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1)**c) * matrix[0][c] * determinante(minor)
    return det


def cramer_solver(matrix):
    """
    Resuelve un sistema lineal usando la regla de Cramer.

    Parámetro:
        matrix (list[list[float]]): matriz aumentada del sistema (n x n+1)

    Retorna:
        list[float]: solución del sistema

    Lanza:
        ValueError: si el sistema no tiene solución única
    """
    matrix = copy.deepcopy(matrix)
    n = len(matrix)
    A = [row[:-1] for row in matrix]
    B = [row[-1] for row in matrix]

    det_A = determinante(A)
    if det_A == 0:
        raise ValueError("El sistema no tiene solución única (determinante cero)")

    soluciones = []
    for i in range(n):
        matriz_modificada = copy.deepcopy(A)
        for j in range(n):
            matriz_modificada[j][i] = B[j]
        det_i = determinante(matriz_modificada)
        soluciones.append(det_i / det_A)

    return soluciones

# Prueba de la función
"""
if __name__ == "__main__":
    sistema = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]
    resultado = cramer_solver(sistema)
    print("Solución:", resultado)

    #Solución: [2.0, 3.0, -1.0]
"""