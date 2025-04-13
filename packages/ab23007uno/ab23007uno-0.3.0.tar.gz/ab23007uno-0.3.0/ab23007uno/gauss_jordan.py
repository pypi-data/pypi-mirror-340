import numpy as np

def gauss_jordan(matriz, tol=1e-6):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    
    Args:
        matriz: Matriz aumentada del sistema (n x n+1)
        tol: Tolerancia para considerar un valor como cero
        
    Returns:
        Vector solución de tamaño n
        
    Raises:
        ValueError: Si la matriz es singular o el sistema no tiene solución única
    """
    n = len(matriz)
    
    for i in range(n):
        # Pivotaje parcial
        max_row = i + np.argmax(np.abs(matriz[i:n, i]))
        if abs(matriz[max_row, i]) < tol:
            raise ValueError("La matriz es singular o el sistema no tiene solución única")
            
        matriz[[i, max_row]] = matriz[[max_row, i]]
        
        # Normalización
        pivote = matriz[i, i]
        matriz[i] = matriz[i] / pivote
        
        # Eliminación
        for j in range(n):
            if i != j:
                factor = matriz[j, i]
                matriz[j] = matriz[j] - factor * matriz[i]
    
    return matriz[:, -1]