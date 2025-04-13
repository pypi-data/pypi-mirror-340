from CG19057UNO.EcuacionesNoLineales import biseccion

def test_biseccion():
    # Función: f(x) = x^3 - 6x^2 + 11x - 6, raíz esperada: 1.0
    f = lambda x: x**3 - 6*x**2 + 11*x - 6
    A = 0
    b = 2
    raiz = biseccion(f, A, b)
    assert abs(f(raiz)) < 1e-6, f"La funcion evaluada en la raiz no es cercana a cero: {f(raiz)}"
    assert A <= raiz <= b, f"La raiz no esta dentro del intervalo [{A}, {b}]"