from ac12066uno.gauss import gauss_elimination

def test_gauss_resuelve_sistema_3x3():
    matrix = [
        [2, 1, -1, 8],
        [-3, -1, 2, -11],
        [-2, 1, 2, -3]
    ]
    resultado = gauss_elimination(matrix)
    esperado = [2.0, 3.0, -1.0]
    assert all(abs(r - e) < 1e-6 for r, e in zip(resultado, esperado))
