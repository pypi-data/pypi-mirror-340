import numpy as np

def lu_decomposition(A, tol=1e-6):
    """
    Descomposición LU con pivotaje parcial.
    Devuelve L, U, P para que PA = LU.
    """
    n = len(A)
    L = np.eye(n)
    U = np.array(A, dtype=float)
    P = np.eye(n)
    
    for i in range(n):
        # Pivotaje
        max_row = i + np.argmax(np.abs(U[i:, i]))
        if abs(U[max_row, i]) < tol:
            raise ValueError("Matriz singular")
            
        if max_row != i:
            U[[i, max_row]] = U[[max_row, i]]
            P[[i, max_row]] = P[[max_row, i]]
            L[[i, max_row], :i] = L[[max_row, i], :i]
        
        # Eliminación
        L[i+1:, i] = U[i+1:, i] / U[i, i]
        U[i+1:, i:] -= np.outer(L[i+1:, i], U[i, i:])
    
    return L, U, P


def resolver_LU(A, b):
    """
    Resuelve Ax = b usando descomposición LU.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    L, U, P = lu_decomposition(A)
    pb = P @ b  # Vector permutado
    
    # Sustitución hacia adelante (Ly = Pb)
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = pb[i] - np.dot(L[i, :i], y[:i])  # Importante usar :i no i:
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    return x