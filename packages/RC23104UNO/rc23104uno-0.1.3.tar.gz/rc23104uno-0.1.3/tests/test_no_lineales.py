def biseccion(f, a, b, tol=1e-6, max_iter=1000):
    if f(a) * f(b) >= 0:
        raise ValueError("El teorema de Bolzano no se cumple: f(a) y f(b) deben tener signos opuestos")

    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or abs(b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    raise ValueError("No se encontró una raíz dentro del número máximo de iteraciones")
