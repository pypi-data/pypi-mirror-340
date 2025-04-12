from fractions import Fraction

'''Metodo Eliminacion de Gauss'''

def gauss_elimination(A, b):
    
    # Conversion de elementos a fracciones
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]

    n = len(b)

    # Eliminacion hacia adelante
    for i in range(n):
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [aj - factor * ai for aj, ai in zip(A[j], A[i])]
            b[j] = b[j] - factor * b[i]

    # Sustitucion hacia atras
    x = [Fraction(0) for _ in range(n)]
    for i in range(n-1, -1, -1):
        suma = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - suma) / A[i][i]

    return x

'''Metodo de Gauss-Jordan'''

def gauss_jordan(A, b):
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]
    n = len(b)

    # Matriz aumentada
    aug = [row + [val] for row, val in zip(A, b)]

    for i in range(n):
        
        # Normalizar la fila actual
        factor = aug[i][i]
        aug[i] = [elem / factor for elem in aug[i]]

        for j in range(n):
            if i != j:
                factor = aug[j][i]
                aug[j] = [a - factor * b for a, b in zip(aug[j], aug[i])]

    # Retornar ultima columna
    return [row[-1] for row in aug]


'''Metodo de Cramer'''

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = Fraction(0)
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1)**c) * matrix[0][c] * determinant(minor)
    return det

def cramer(A, b):
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Sistema sin solucion única")
    
    x = []
    for i in range(len(b)):
        Ai = [row[:] for row in A]
        for j in range(len(b)):
            Ai[j][i] = b[j]
        det_Ai = determinant(Ai)
        x.append(det_Ai / det_A)
    return x


'''Metodo de Descomposicion de LU'''

def lu_decomposition(A, b):
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]
    n = len(A)

    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    U = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    for i in range(n):
        
        # U
        for k in range(i, n):
            U[i][k] = A[i][k] - sum(L[i][j]*U[j][k] for j in range(i))
            
        # L
        for k in range(i, n):
            if i == k:
                L[i][i] = Fraction(1)
            else:
                L[k][i] = (A[k][i] - sum(L[k][j]*U[j][i] for j in range(i))) / U[i][i]

    # Ly = b sustitucion hacia adelante
    y = [Fraction(0) for _ in range(n)]
    for i in range(n):
        y[i] = b[i] - sum(L[i][j]*y[j] for j in range(i))

    # Ux = y sustitucion hacia atras)
    x = [Fraction(0) for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i][j]*x[j] for j in range(i+1, n))) / U[i][i]

    return x

'''Metodo De Jacobi'''

def jacobi(A, b, tol=1e-10, max_iter=100):
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]
    x = [Fraction(0) for _ in range(len(b))]

    for _ in range(max_iter):
        x_new = x[:]
        for i in range(len(A)):
            s = sum(A[i][j] * x[j] for j in range(len(A)) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        
        # Verificacion de convergencia 
        if all(abs(float(x_new[i] - x[i])) < tol for i in range(len(x))):
            return x_new
        x = x_new

    return x

'''Metodo de Gauss-Seidel'''

def gauss_seidel(A, b, tol=1e-10, max_iter=100):
    
    # Conversion de elementos a fracciones
    A = [[Fraction(val) for val in row] for row in A]
    b = [Fraction(val) for val in b]
    n = len(A)
    x = [Fraction(0) for _ in range(n)]

    for _ in range(max_iter):
        x_new = x[:]
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i+1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        # Verificacion de convergencia usando floats para comparar
        if all(abs(float(x_new[i] - x[i])) < tol for i in range(n)):
            return x_new

        x = x_new

    return x

