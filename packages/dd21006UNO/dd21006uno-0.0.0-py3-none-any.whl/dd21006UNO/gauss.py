def gauss_elimination(A, b):
    n = len(A)
    for i in range(n):
        for k in range(i+1, n):
            if A[i][i] == 0:
                raise ValueError("División por cero")
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= A[i][j]*x[j]
        x[i] = x[i]/A[i][i]
    return x
