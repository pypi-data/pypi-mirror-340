import numpy as np
from CG19057UNO.EcuacionesLineales import elimina_Gauss, gauss_Jordan, crammer, descomposicion_LU, jacobi, gauss_Seidel

def test_elimina_Gauss():
    # Sistema de ecuaciones: 3x + 2y = 18, -x + 2y = 2
    A = [[3, 2], [-1, 2]]
    b = [18, 2]
    solucion = elimina_Gauss(A, b)
    assert np.allclose(solucion, [4.0, 3.0]), "Solucion incorrecta"

def test_Gauss_Jordan():
    # Sistema de ecuaciones: 3x + 2y = 18, -x + 2y = 2
    A = [[3, 2], [-1, 2]]
    b = [18, 2]
    solucion = gauss_Jordan(A, b)
    assert np.allclose(solucion, [4.0, 3.0]), "Solucion incorrecta"

def test_crammer():
    # Sistema de ecuaciones: 3x + 2y = 18, -x + 2y = 2
    A = [[3, 2], [-1, 2]]
    b = [18, 2]
    solucion = crammer(A, b)
    assert np.allclose(solucion, [4.0, 3.0]), "Solucion incorrecta"

def test_descomposicion_LU():
    # Sistema de ecuaciones: 3x + 2y = 18, -x + 2y = 2
    A = [[3, 2], [-1, 2]]
    b = [18, 2]
    solucion = descomposicion_LU(A, b)
    assert np.allclose(solucion, [4.0, 3.0]), "Solucion incorrecta"

def test_jacobi():
    # Sistema de ecuaciones: 4x + y = 5, x + 5y = 14
    A = [[4, 1], [1, 5]]
    b = [5, 14]
    solucion_exacta = np.linalg.solve(np.array(A), np.array(b))
    solucion = jacobi(A, b, max_Iteraciones=100)
    assert np.allclose(solucion, solucion_exacta, atol=1e-6), f"Solución incorrecta: {solucion}"

def test_gauss_seidel():
    # Sistema de ecuaciones: 4x + y = 5, x + 5y = 14
    A = [[4, 1], [1, 5]]
    b = [5, 14]
    solucion_exacta = np.linalg.solve(np.array(A), np.array(b))
    solucion = gauss_Seidel(A, b, max_iteraciones=100)
    assert np.allclose(solucion, solucion_exacta, atol=1e-6), f"Solución incorrecta: {solucion}"