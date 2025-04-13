from AA20029UNO import crammer

# Ejemplo de uso
coefficients = [[3, -1, 4], [1, 2, -1], [2, -1, 1]]
ind_terms = [10, 3, 5]

solucion = crammer(coefficients, ind_terms)
print("Solución del sistema de ecuaciones por la regla de Cramer:")
for variable, valor in solucion.items():
    print(f"{variable} = {valor}")