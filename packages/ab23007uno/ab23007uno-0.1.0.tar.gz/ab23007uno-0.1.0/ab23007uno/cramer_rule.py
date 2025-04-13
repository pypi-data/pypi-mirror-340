import numpy as np

def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando la regla de Cramer.
    
    Args:
        A: Matriz de coeficientes de tamaño n x n
        b: Vector de términos independientes de tamaño n
    
    Returns:
        x: Vector solución de tamaño n
        
    Note:
        Este método es computacionalmente costoso para n > 4.
        Para sistemas grandes, considere usar eliminación gaussiana.
    """
    # Convertir a arrays de numpy si no lo son ya
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    
    # Validar que la matriz A sea cuadrada
    if A.shape != (n, n):
        raise ValueError("La matriz A debe ser cuadrada")
    
    # Calcular el determinante de la matriz A
    det_A = np.linalg.det(A)
    
    # Verificar si el determinante es cero (sistema sin solución única)
    if abs(det_A) < 1e-10:
        raise ValueError("El determinante de la matriz es cero. El sistema no tiene solución única.")
    
    # Inicializar el vector solución
    x = np.zeros(n)
    
    # Aplicar la regla de Cramer para cada incógnita
    for i in range(n):
        # Crear una copia de la matriz A
        A_i = A.copy()
        
        # Reemplazar la columna i por el vector b
        A_i[:, i] = b
        
        # Calcular el determinante de A_i
        det_A_i = np.linalg.det(A_i)
        
        # Calcular x_i según la regla de Cramer
        x[i] = det_A_i / det_A
    
    return x
