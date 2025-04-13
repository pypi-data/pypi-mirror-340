import numpy as np

def gauss_elimination(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de eliminación gaussiana.
    
    Args:
        A: Matriz de coeficientes de tamaño n x n
        b: Vector de términos independientes de tamaño n
    
    Returns:
        x: Vector solución de tamaño n
    """
    # Convertir a arrays de numpy si no lo son ya
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    
    # Validar que la matriz A sea cuadrada
    if A.shape != (n, n):
        raise ValueError("La matriz A debe ser cuadrada")
    
    # Crear la matriz aumentada [A|b]
    Ab = np.column_stack((A, b))
    
    # Eliminación hacia adelante
    for i in range(n):
        # Buscar el pivote máximo en la columna actual
        max_row = i + np.argmax(abs(Ab[i:n, i]))
        
        # Intercambiar filas si es necesario
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Verificar si la matriz es singular
        if abs(Ab[i, i]) < 1e-10:
            raise ValueError("La matriz es singular o casi singular")
        
        # Eliminación de variables
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:n+1] -= factor * Ab[i, i:n+1]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (Ab[i, n] - np.sum(Ab[i, i+1:n] * x[i+1:n])) / Ab[i, i]
    
    return x
