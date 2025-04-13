from ac12066uno.gauss_jordan import gauss_jordan_elimination

def test_gauss_jordan_resuelve_sistema_3x3():
    sistema = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]
    resultado = gauss_jordan_elimination(sistema)
    esperado = [2.0, 3.0, -1.0]
    assert all(abs(r - e) < 1e-6 for r, e in zip(resultado, esperado))
