import math
from ac12066uno.biseccion import biseccion

def test_biseccion_raiz_funcion():
    def f(x):
        return x**3 - x - 2  # raíz real entre [1, 2]

    raiz = biseccion(f, 1, 2)
    # Solución aproximada esperada
    raiz_esperada = 1.5213797067990527

    # Se compara la raíz encontrada con un margen de error
    assert abs(raiz - raiz_esperada) < 1e-6
