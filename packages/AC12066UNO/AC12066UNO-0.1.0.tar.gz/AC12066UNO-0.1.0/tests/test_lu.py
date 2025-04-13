from ac12066uno.lu import lu_solver

def test_lu_resuelve_sistema_3x3():
    sistema = [
        [2, 1, 1, 5],
        [4, 1, 2, 9],
        [-2, 1, 2, -1]
    ]
    resultado = lu_solver(sistema)
    esperado = [1.6666666666666667, 1.0, 0.6666666666666666]
    assert all(abs(r - e) < 1e-6 for r, e in zip(resultado, esperado))
