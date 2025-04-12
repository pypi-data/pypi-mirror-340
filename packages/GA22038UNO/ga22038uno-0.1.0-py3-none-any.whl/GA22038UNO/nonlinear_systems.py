import numpy as np

def bisection(f, a, b, tol=1e-10, max_iter=100):
    """
    Encuentra una raíz de una función no lineal usando el método de bisección.
    
    Parameters:
    ----------
    f : function
        Función para la cual se busca la raíz
    a : float
        Límite inferior del intervalo inicial
    b : float
        Límite superior del intervalo inicial
    tol : float, optional
        Tolerancia para el criterio de convergencia
    max_iter : int, optional
        Número máximo de iteraciones
        
    Returns:
    -------
    float
        Aproximación de la raíz
    int
        Número de iteraciones realizadas
    """
    # Verificar que f(a) y f(b) tengan signos opuestos
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    # Iteraciones del método
    for i in range(max_iter):
        # Punto medio
        c = (a + b) / 2
        fc = f(c)
        
        # Verificar convergencia
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, i+1
            
        # Actualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    print(f"Advertencia: Alcanzado el número máximo de iteraciones ({max_iter}) sin convergencia.")
    return (a + b) / 2, max_iter