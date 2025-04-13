import numpy as np
import math as mt

def biseccion(func, a, b, tolerance=1e-7, max_iterations=100):
    """
    Encuentra una raíz de la función 'func' en el intervalo [a, b] usando el método de bisección.

    Parametros:       
        tolerance (float, opcional): La tolerancia para la raíz encontrada. Defaults to 1e-7.
        max_iterations (int, opcional): El número máximo de iteraciones. Defaults to 100.

    Retorna:
        Una aproximación de la raíz si se encuentra dentro de la tolerancia
        y el número máximo de iteraciones, de lo contrario devuelve None.
    """
    if np.sign(func(a)) == np.sign(func(b)):
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo.")
    
    itr = 0
    for i in range(max_iterations):
        c = (a + b) / 2
        itr = i + 1
        if np.abs(func(c)) < tolerance:
            return c, itr
        elif np.sign(func(c)) == np.sign(func(a)):
            a = c
        else:
            b = c        

    print(f"Advertencia: Número máximo de iteraciones alcanzado sin la tolerancia deseada. Última aproximación: {c}")
    return c, itr