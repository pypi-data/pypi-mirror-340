from ac12066uno.gauss_seidel import gauss_seidel_solver

def test_gauss_seidel_soluciona_sistema_3x3():
    sistema = [
        [4, 1, 2, 4],
        [3, 5, 1, 7],
        [1, 1, 3, 3]
    ]
    resultado = gauss_seidel_solver(sistema)
    esperado = [0.500000000016384, 0.9999999999934464, 0.49999999999672323]
    assert all(abs(r - e) < 1e-6 for r, e in zip(resultado, esperado))
