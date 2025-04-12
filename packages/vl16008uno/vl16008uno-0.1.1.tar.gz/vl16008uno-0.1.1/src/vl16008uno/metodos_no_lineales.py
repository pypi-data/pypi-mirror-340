def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.
    
    Args:
        f (function): Función a la que se le busca la raíz
        a (float): Extremo izquierdo del intervalo
        b (float): Extremo derecho del intervalo
        tol (float): Tolerancia para el error
        max_iter (int): Número máximo de iteraciones
        
    Returns:
        float: Aproximación de la raíz
        
    Example:
        >>> f = lambda x: x**2 - 2
        >>> raiz = biseccion(f, 0, 2)
        >>> print(raiz)
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2