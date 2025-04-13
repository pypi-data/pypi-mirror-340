def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de Bisección para encontrar la raíz de una función f(x) = 0.

    Parámetros:
    f -- función a evaluar
    a -- límite inferior del intervalo
    b -- límite superior del intervalo
    tol -- tolerancia aceptada para la raíz
    max_iter -- número máximo de iteraciones

    Retorna:
    Aproximación de la raíz si se encuentra dentro del intervalo.
    """
    if f(a) * f(b) > 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b].")

    for i in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    raise RuntimeError("El método no convergió en el número máximo de iteraciones.")