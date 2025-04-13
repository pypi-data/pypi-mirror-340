# src/AC12066UNO/gauss_seidel.py

import copy

def gauss_seidel_solver(matrix, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema lineal utilizando el método de Gauss-Seidel.

    Parámetros:
        matrix (list[list[float]]): matriz aumentada del sistema (n x n+1)
        tol (float): tolerancia para la convergencia
        max_iter (int): número máximo de iteraciones

    Retorna:
        list[float]: solución aproximada del sistema

    Lanza:
        ValueError: si hay división por cero o el sistema no converge
    """
    matrix = copy.deepcopy(matrix)
    n = len(matrix)
    A = [row[:-1] for row in matrix]
    b = [row[-1] for row in matrix]

    x = [0.0 for _ in range(n)]

    for iteration in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            if A[i][i] == 0:
                raise ValueError(f"Cero en la diagonal en fila {i}.")
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i][i]

        # Verificar convergencia
        if all(abs(x[i] - x_old[i]) < tol for i in range(n)):
            return x

    raise ValueError("No converge dentro del número máximo de iteraciones")

# Prueba de la función
"""
if __name__ == "__main__":
    sistema = [
        [4, 1, 2, 4],
        [3, 5, 1, 7],
        [1, 1, 3, 3]
    ]
    resultado = gauss_seidel_solver(sistema)
    print("Solución:", resultado)

    #Solución: [0.500000000016384, 0.9999999999934464, 0.49999999999672323]
"""