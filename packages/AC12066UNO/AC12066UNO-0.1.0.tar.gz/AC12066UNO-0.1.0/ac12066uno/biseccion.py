# src/AC12066UNO/biseccion.py

def biseccion(f, a, b, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando bisección.

    Parámetros:
        f (function): función f(x)
        a (float): límite inferior
        b (float): límite superior
        tol (float): tolerancia para detener iteraciones
        max_iter (int): número máximo de iteraciones

    Retorna:
        float: valor aproximado de la raíz

    Lanza:
        ValueError: si no se cumple f(a)*f(b) < 0
    """
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol or abs(b - a) / 2 < tol:
            return c

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    raise ValueError("No se encontró una raíz dentro del número máximo de iteraciones.")

# Prueba de la función
"""
if __name__ == "__main__":
    import math

    def f(x):
        return x**3 - x - 2  # raíz real entre [1, 2]

    raiz = biseccion(f, 1, 2)
    print("Raíz aproximada:", raiz)

    #Solución: Raíz aproximada: 1.521...
"""