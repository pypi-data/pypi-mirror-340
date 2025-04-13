import numpy as np

def gauss_seidel(A, b, x0, tol=1e-6, max_iter=1000, verbose=True):
    """
    Método de Gauss-Seidel para resolver Ax = b
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes
        x0: Aproximación inicial
        tol: Tolerancia para convergencia
        max_iter: Máximo de iteraciones
        verbose: Mostrar progreso (True/False)
        
    Returns:
        x: Solución aproximada
        iter_count: Número de iteraciones usadas
        err: Error final
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    x = np.asarray(x0, dtype=float).copy()
    
    # Validaciones
    n = len(b)
    if A.shape != (n, n):
        raise ValueError("A debe ser cuadrada")
    if len(x) != n:
        raise ValueError("x0 debe tener misma dimensión que b")
    
    if np.any(np.diag(A) == 0):
        raise ValueError("Diagonal con ceros")
    
    if not np.all(np.abs(A.diagonal()) >= np.sum(np.abs(A), axis=1) - np.abs(A.diagonal())):
        if verbose:
            print("Advertencia: La matriz no es diagonalmente dominante")
    
    # Precomputar la matriz triangular inferior
    L = np.tril(A)
    U = A - L
    
    iter_count = 0
    err = tol + 1
    
    if verbose:
        print(f"Iteración {iter_count}: x = {x}")
    
    while err > tol and iter_count < max_iter:
        x_old = x.copy()
        x = np.linalg.solve(L, b - U @ x)  # Vectorizado
        
        err = np.linalg.norm(x - x_old) / np.linalg.norm(x)
        iter_count += 1
        
        if verbose:
            print(f"Iteración {iter_count}: x = {x}, Error = {err:.6f}")
    
    if verbose and iter_count == max_iter and err > tol:
        print("Advertencia: No convergió en el máximo de iteraciones")
    
    return x, iter_count, err