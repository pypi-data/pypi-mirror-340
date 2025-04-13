# src/AC12066UNO/jacobi.py

import copy

def jacobi_solver(matrix, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema lineal utilizando el método iterativo de Jacobi.

    Parámetros:
        matrix (list[list[float]]): matriz aumentada del sistema (n x n+1)
        tol (float): tolerancia para la convergencia
        max_iter (int): número máximo de iteraciones

    Retorna:
        list[float]: solución aproximada del sistema

    Lanza:
        ValueError: si la matriz no es cuadrada o hay división por cero
    """
    matrix = copy.deepcopy(matrix)
    n = len(matrix)
    A = [row[:-1] for row in matrix]
    b = [row[-1] for row in matrix]

    x = [0.0 for _ in range(n)]  # vector inicial (puede personalizarse)
    for iteracion in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            if A[i][i] == 0:
                raise ValueError(f"Cero en la diagonal en fila {i}.")
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]

        # Verificar convergencia
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new

        x = x_new

    raise ValueError("No converge dentro del número máximo de iteraciones")

# Prueba de la función
"""
if __name__ == "__main__":
    sistema = [
        [10, -1, 2, 6],
        [-1, 11, -1, 25],
        [2, -1, 10, -11]
    ]
    resultado = jacobi_solver(sistema)
    print("Solución:", resultado)

    #Solución: [1.0432692307598361, 2.269230769237108, -1.0817307692400526]
"""