import numpy as np

def jacobi(A, b, x0, tol=1e-6, max_iter=1000, verbose=True):
    '''
    Método de Jacobi mejorado para resolver Ax = b
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes
        x0: Aproximación inicial
        tol: Tolerancia para convergencia
        max_iter: Máximo de iteraciones
        verbose: Mostrar progreso (True/False)
        
    Returns:
        x: Solución aproximada
        k: Número de iteraciones usadas
    '''
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    x = np.asarray(x0, dtype=float).copy()
    
    # Validaciones
    n = len(A)
    if A.shape != (n, n):
        raise ValueError("A debe ser cuadrada")
    if len(b) != n or len(x) != n:
        raise ValueError("Dimensiones incompatibles")
        
    if not np.all(np.abs(A.diagonal()) >= np.sum(np.abs(A), axis=1) - np.abs(A.diagonal())):
        if verbose:
            print("Advertencia: La matriz no es diagonalmente dominante")
    
    # Precomputar componentes
    D = np.diag(A)
    if np.any(D == 0):
        raise ValueError("Diagonal con ceros")
    R = A - np.diagflat(D)
    
    # Algoritmo de Jacobi
    for k in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x, np.inf) < tol:
            if verbose:
                print(f"Convergencia alcanzada en {k+1} iteraciones")
            return x_new, k+1
        if verbose:
            print(f"Iteración {k+1}: x = {x_new}")
        x = x_new
    
    if verbose:
        print("No convergió en el máximo de iteraciones")
    return x, max_iter


