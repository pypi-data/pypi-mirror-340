import math

def bisection(f, a, b, tol=1e-6, max_iter=1000, verbose=False):
    '''
    Método de bisección para encontrar raíces de f(x) = 0 en [a, b]
    
    Args:
        f: Función continua (debe cambiar de signo en [a,b])
        a: Extremo izquierdo del intervalo
        b: Extremo derecho del intervalo
        tol: Tolerancia (criterio de parada)
        max_iter: Máximo número de iteraciones
        verbose: Mostrar progreso (opcional)
        
    Returns:
        tuple: (aproximación de la raíz, número de iteraciones)
        
    Raises:
        ValueError: Si no se cumple el teorema de Bolzano
    '''
    # Verificación inicial 
    fa, fb = f(a), f(b)
    
    if abs(fa) < tol:
        return a, 0
    if abs(fb) < tol:
        return b, 0
        
    if fa * fb >= 0:
        raise ValueError("No se cumple el teorema de Bolzano: f(a) y f(b) deben tener signos opuestos")
    
    iter_count = 0
    m_prev = a  # Para calcular el error relativo
    
    while iter_count < max_iter:
        m = a + (b - a)/2  
        fm = f(m)
        
        if verbose:
            print(f"Iter {iter_count}: a={a:.6f}, b={b:.6f}, m={m:.6f}, f(m)={fm:.6e}")
        
        # Criterio de parada (error absoluto o relativo)
        if abs(fm) < tol or (b - a)/2 < tol:
            break
            
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
            
        iter_count += 1
    
    if verbose and iter_count == max_iter:
        print("Advertencia: Alcanzado el máximo de iteraciones")
    
    return m, iter_count
