def multiply_matrices(F, M):
    # Multiplies two 2x2 matrices F and M, stores result back in F
    x = F[0][0] * M[0][0] + F[0][1] * M[1][0]
    y = F[0][0] * M[0][1] + F[0][1] * M[1][1]
    z = F[1][0] * M[0][0] + F[1][1] * M[1][0]
    w = F[1][0] * M[0][1] + F[1][1] * M[1][1]

    F[0][0], F[0][1], F[1][0], F[1][1] = x, y, z, w

def power(F, n):
    # Raises matrix F to the power n using exponentiation by squaring
    if n == 0 or n == 1:
        return
    M = [[1, 1], [1, 0]]
    power(F, n // 2)
    multiply_matrices(F, F)
    if n % 2 != 0:
        multiply_matrices(F, M)

def fibonacci_mod(n, mod):
    # Computes the nth Fibonacci number modulo `mod` using matrix exponentiation
    if n == 0:
        return 0
    F = [[1, 1], [1, 0]]
    power(F, n - 1)
    return F[0][0] % mod