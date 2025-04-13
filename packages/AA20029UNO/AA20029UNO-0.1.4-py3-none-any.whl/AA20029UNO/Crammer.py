import numpy as np
from fractions import Fraction as StandardFraction
from .fraccion import Fraccion

def crammer(coefficients, ind_terms):
    """Resuelve un sistema 3x3 por la regla de Cramer.

        Parametros:
            coefficients: Matriz 3x3 de coeficientes (lista de listas).
            ind_terms: Vector de términos independientes (lista de 3 elementos).

        Retorna:
            Un diccionario con las soluciones {'x': valor, 'y': valor, 'z': valor}
            o un mensaje si no hay solución única.
    """

    def determinante(matriz_det):
        dimension = len(matriz_det)
        if dimension == 1:
            return matriz_det[0][0]
        elif dimension == 2:
            return (matriz_det[0][0] * matriz_det[1][1]) - (matriz_det[0][1] * matriz_det[1][0])
        else:
            determinante_val = Fraccion(0)
            for j in range(dimension):
                elemento = matriz_det[0][j]
                submatriz = [fila[:j] + fila[j+1:] for fila in matriz_det[1:]]
                determinante_submatriz = determinante(submatriz)
                signo = Fraccion(1) if j % 2 == 0 else Fraccion(-1)
                determinante_val += elemento * signo * determinante_submatriz
            return determinante_val

    # Convertir los coeficientes y términos independientes a objetos Fraccion
    matriz_coeficientes = [[Fraccion(StandardFraction(num)) for num in row] for row in coefficients]
    vector_terminos_independientes = [Fraccion(StandardFraction(num)) for num in ind_terms]

    det_A = determinante(matriz_coeficientes)

    if det_A == Fraccion(0):
        return "El sistema no tiene solución única (el determinante de la matriz de coeficientes es cero)."

    n = len(vector_terminos_independientes)
    soluciones = {}

    for i in range(n):
        matriz_modificada = [list(fila) for fila in matriz_coeficientes]
        for j in range(n):
            matriz_modificada[j][i] = vector_terminos_independientes[j]

        det_Ai = determinante(matriz_modificada)
        variable_name = ['x', 'y', 'z'][i]
        soluciones[variable_name] = det_Ai / det_A

    return soluciones

