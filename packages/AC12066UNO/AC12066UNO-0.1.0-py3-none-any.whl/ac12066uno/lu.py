# src/AC12066UNO/lu.py

import copy

def forward_substitution(L, b):
    n = len(L)
    y = [0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    return y

def backward_substitution(U, y):
    n = len(U)
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x

def lu_decomposition(matrix):
    """
    Realiza la descomposición LU de una matriz cuadrada A.
    Retorna las matrices L y U tal que A = LU.
    """
    n = len(matrix)
    A = copy.deepcopy(matrix)
    L = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    U = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        for j in range(i+1, n):
            if U[i][i] == 0:
                raise ValueError("Cero en el pivote. No se puede descomponer.")
            L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    return L, U

def lu_solver(matrix):
    """
    Resuelve un sistema lineal usando descomposición LU.

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
    b = [row[-1] for row in matrix]

    L, U = lu_decomposition(A)
    y = forward_substitution(L, b)
    x = backward_substitution(U, y)
    return x

# Prueba de la función
"""
if __name__ == "__main__":
    sistema = [
        [2, 1, 1, 5],
        [4, 1, 2, 9],
        [-2, 1, 2, -1]
    ]
    resultado = lu_solver(sistema)
    print("Solución:", resultado)

    #Solución: [1.666, 1.0, 0.666]
"""