# Método de Bisección para ecuaciones no lineales
def biseccion(f, a, b, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando bisección.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo.")

    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c
