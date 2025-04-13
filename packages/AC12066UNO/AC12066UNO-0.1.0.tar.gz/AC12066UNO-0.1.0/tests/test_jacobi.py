from ac12066uno.jacobi import jacobi_solver

def test_jacobi_soluciona_sistema_3x3():
    sistema = [
        [10, -1, 2, 6],
        [-1, 11, -1, 25],
        [2, -1, 10, -11]
    ]
    resultado = jacobi_solver(sistema)
    esperado = [1.0432692307598361, 2.269230769237108, -1.0817307692400526]
    assert all(abs(r - e) < 1e-6 for r, e in zip(resultado, esperado))
