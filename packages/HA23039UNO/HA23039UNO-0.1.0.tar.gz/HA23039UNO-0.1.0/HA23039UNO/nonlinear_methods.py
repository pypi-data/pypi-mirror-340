"""
Módulo que implementa métodos para resolver ecuaciones no lineales.
"""

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Resuelve una ecuación no lineal f(x) = 0 usando el método de bisección.
    
    Args:
        f (callable): Función que representa la ecuación f(x) = 0.
        a (float): Extremo izquierdo del intervalo inicial.
        b (float): Extremo derecho del intervalo inicial.
        tol (float, optional): Tolerancia para convergencia. Por defecto 1e-6.
        max_iter (int, optional): Número máximo de iteraciones. Por defecto 100.
    
    Returns:
        tuple: (Aproximación de la raíz, Número de iteraciones realizadas)
    
    Raises:
        ValueError: Si f(a) y f(b) tienen el mismo signo.
    """
    # Verificar que la función cambia de signo en el intervalo
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    # Iterar hasta encontrar la raíz o alcanzar max_iter
    for i in range(max_iter):
        # Calcular el punto medio
        c = (a + b) / 2
        fc = f(c)
        
        # Si la función en c es suficientemente cercana a cero o el intervalo es pequeño
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, i + 1
        
        # Actualizar el intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    # Si llegamos aquí, retornar la mejor aproximación
    return (a + b) / 2, max_iter