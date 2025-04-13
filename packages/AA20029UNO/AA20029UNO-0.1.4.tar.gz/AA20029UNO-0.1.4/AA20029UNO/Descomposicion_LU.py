import numpy as np
from .fraccion import Fraccion


def lu_decomposition(coefficients, ind_terms):
    """Descompone una matriz en LU y resuelve Ax = b.

    Parametros:
        coefficients: Matriz de coeficientes (lista de listas).
        ind_terms: Vector de términos independientes (lista).

    Retorna:
        El vector solución (lista de objetos Fraccion).

    Raises:
        ValueError: Si no se puede realizar la descomposición LU.
    """
    n = len(coefficients)
    L = [[Fraccion(0)] * n for _ in range(n)]
    U = [[Fraccion(coefficients[i][j]) for j in range(n)] for i in range(n)]
    b = [Fraccion(val) for val in ind_terms]

    for i in range(n):
        L[i][i] = Fraccion(1)
        for j in range(i + 1, n):
            if U[i][i] == Fraccion(0):
                raise ValueError("No se puede realizar la descomposicion LU debido a un pivote cero.")
            factor = U[j][i] / U[i][i]
            L[j][i] = factor
            for k in range(i, n):
                U[j][k] = U[j][k] - factor * U[i][k]

    # Resolver Ly = b usando sustitucion hacia adelante
    y = [Fraccion(0)] * n
    for i in range(n):
        sum_ly = Fraccion(0)
        for j in range(i):
            sum_ly += L[i][j] * y[j]
        y[i] = (b[i] - sum_ly) / L[i][i]

    # Resolver Ux = y usando sustitucion hacia atras
    x = [Fraccion(0)] * n
    for i in range(n - 1, -1, -1):
        sum_ux = Fraccion(0)
        for j in range(i + 1, n):
            sum_ux += U[i][j] * x[j]
        x[i] = (y[i] - sum_ux) / U[i][i]

    return x

