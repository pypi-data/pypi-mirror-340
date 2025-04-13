import numpy as np

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Jacobi.
    
    Parámetros:
        A (numpy.ndarray): Matriz de coeficientes de nxn
        b (numpy.ndarray): Vector de términos independientes de tamaño n
        x0 (numpy.ndarray): Vector inicial (opcional)
        tol (float): Tolerancia para el criterio de parada
        max_iter (int): Número máximo de iteraciones
        
    Retorna:
        numpy.ndarray: Vector solución x
        int: Número de iteraciones realizadas
        
    Ejemplo:
        >>> A = np.array([[10, -1, 2], [1, 10, -1], [2, 3, 20]])
        >>> b = np.array([6, 7, 25])
        >>> x, iter = jacobi(A, b)
        >>> print(x)
        [0.9999986  0.99999951 1.00000016]
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    D = np.diag(A)
    R = A - np.diagflat(D)
    
    for k in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            return x_new, k+1
        x = x_new
    
    return x, max_iter

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Gauss-Seidel.
    
    Parámetros:
        A (numpy.ndarray): Matriz de coeficientes de nxn
        b (numpy.ndarray): Vector de términos independientes de tamaño n
        x0 (numpy.ndarray): Vector inicial (opcional)
        tol (float): Tolerancia para el criterio de parada
        max_iter (int): Número máximo de iteraciones
        
    Retorna:
        numpy.ndarray: Vector solución x
        int: Número de iteraciones realizadas
        
    Ejemplo:
        >>> A = np.array([[10, -1, 2], [1, 10, -1], [2, 3, 20]])
        >>> b = np.array([6, 7, 25])
        >>> x, iter = gauss_seidel(A, b)
        >>> print(x)
        [1. 1. 1.]
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    for k in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            x_new[i] = (b[i] - np.dot(A[i, :i], x_new[:i]) - 
                        np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            return x_new, k+1
        x = x_new
    
    return x, max_iter

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.
    
    Parámetros:
        f (function): Función a evaluar
        a (float): Extremo izquierdo del intervalo
        b (float): Extremo derecho del intervalo
        tol (float): Tolerancia para el criterio de parada
        max_iter (int): Número máximo de iteraciones
        
    Retorna:
        float: Aproximación de la raíz
        int: Número de iteraciones realizadas
        
    Ejemplo:
        >>> f = lambda x: x**3 - x - 2
        >>> raiz, iter = biseccion(f, 1, 2)
        >>> print(raiz)
        1.5213851928710938
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for k in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol or (b - a)/2 < tol:
            return c, k+1
        
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2, max_iter      