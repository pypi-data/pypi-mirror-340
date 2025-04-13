import numpy as np
def gauss_elimination(coefficients, ind_terms):

    """
        Resuelve un sistema de ecuaciones lineales por el metodo de eliminacion de guass

        Parametros:
            coefficients: Matriz de coeficientes (lista de listas o array).
            ind_terms: Vector de términos independientes (lista o array).

        Retorna:
            El vector solución (array) o None si no hay solución única.
    """

    coefficients = np.array(coefficients, dtype=float)
    ind_terms = np.array(ind_terms, dtype=float)
    n = len(ind_terms)
    equations = np.hstack([coefficients, ind_terms.reshape(-1,1)])
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(equations[r,i]))
        if equations[max_row, i] == 0:
            return None
        equations[[i, max_row]] = equations[[max_row, i]]

        for j in range(i + 1, n):
            factor = equations[j, i] / equations[i, i]
            equations[j,i:] -= factor * equations[i, i:]

    x = np.zeros(n)

    for i in range(n - 1, -1, -1):
        x[i] = (equations[i, -1] - np.dot(equations[i, i + 1:n], x[i + 1:n])) / equations[i,i]
    
    return x

