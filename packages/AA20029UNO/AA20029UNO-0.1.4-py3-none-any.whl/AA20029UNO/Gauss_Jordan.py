import numpy as np
from .fraccion import Fraccion
def gauss_jordan(coefficients, ind_terms, imprimir_it=False):
    """ Resuelve un sistema lineal Ax = ind_terms por Gauss-Jordan.

        Parametros:
            coefficients: Matriz de coeficientes (lista de listas).
            ind_terms: Vector de términos independientes (lista).
            imprimir_it: valor boolean que determina si se imprimen las interaciones.
        Retorna:
            El vector solución (array) o None si no hay solución única.
    """
    n = len(ind_terms)
    
    equations_ls = [[Fraccion(coefficients[i][j]) for j in range(n)] + [Fraccion(ind_terms[i])] for i in range(n)]
    equations = np.array(equations_ls)
    for i in range(n):
        if i == 0 and imprimir_it : print("matriz inicial", *equations, sep= "\n")   
        if equations[i, i] == 0:
            for k in range(i + 1, n):
                if equations[k, i] != 0:
                    equations[[i, k]] = equations[[k, i]]
                    break
            else:
                return None       
                  
        pivote = equations[i, i]
        equations[i] = np.array([equations[i, l] / pivote for l in range(n + 1)])
        
        for j in range(n):
            if i != j:                
                factor = equations[j, i]
                equations[j] = np.array([equations[j, l] - factor * equations[i, l] for l in range(n + 1)])
        
        if imprimir_it : print('Iteracion: ' + str(i+1), *equations, sep= "\n")                       
    return equations[:, -1]



