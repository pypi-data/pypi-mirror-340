import numpy as np

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    
    Args:
        A (np.array): Matriz de coeficientes de tamaño n x n.
        b (np.array): Vector de términos independientes de tamaño n.
        x0 (np.array): Vector inicial de tamaño n. Si es None, se usa vector cero.
        tol (float): Tolerancia para el criterio de parada.
        max_iter (int): Número máximo de iteraciones.
        
    Returns:
        np.array: Vector solución x de tamaño n.
        
    Raises:
        ValueError: Si no converge en max_iter iteraciones.
        
    Example:
        >>> A = np.array([[10, -1, 2], [-1, 11, -1], [2, -1, 10]])
        >>> b = np.array([6, 25, -11])
        >>> x = jacobi(A, b)
        >>> print(x)
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    D = np.diag(A)
    R = A - np.diagflat(D)
    
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    
    raise ValueError(f"No convergió en {max_iter} iteraciones")

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    
    Args:
        A (np.array): Matriz de coeficientes de tamaño n x n.
        b (np.array): Vector de términos independientes de tamaño n.
        x0 (np.array): Vector inicial de tamaño n. Si es None, se usa vector cero.
        tol (float): Tolerancia para el criterio de parada.
        max_iter (int): Número máximo de iteraciones.
        
    Returns:
        np.array: Vector solución x de tamaño n.
        
    Raises:
        ValueError: Si no converge en max_iter iteraciones.
        
    Example:
        >>> A = np.array([[16, 3], [7, -11]])
        >>> b = np.array([11, 13])
        >>> x = gauss_seidel(A, b)
        >>> print(x)
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    
    raise ValueError(f"No convergió en {max_iter} iteraciones")

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.
    
    Args:
        f (callable): Función a la que se le busca la raíz.
        a (float): Extremo izquierdo del intervalo.
        b (float): Extremo derecho del intervalo.
        tol (float): Tolerancia para el criterio de parada.
        max_iter (int): Número máximo de iteraciones.
        
    Returns:
        float: Aproximación de la raíz.
        
    Raises:
        ValueError: Si no hay cambio de signo en el intervalo o si no converge.
        
    Example:
        >>> f = lambda x: x**3 - x - 2
        >>> raiz = biseccion(f, 1, 2)
        >>> print(raiz)
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a)/2 < tol:
            return c
        
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    raise ValueError(f"No convergió en {max_iter} iteraciones")