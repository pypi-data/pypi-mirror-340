def bisection(f, a, b, tol=1e-10, max_iter=100):
    if f(a) * f(b) > 0:
        raise ValueError("La función no cambia de signo en el intervalo dado.")
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            print(f"NOMBRE DEL MÉTODO USADO: Bisección | X = {c}  Y = {c}")
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    resultado = (a + b) / 2
    print(f"NOMBRE DEL MÉTODO USADO: Bisección | X = {resultado}  Y = {resultado}")
    return resultado
