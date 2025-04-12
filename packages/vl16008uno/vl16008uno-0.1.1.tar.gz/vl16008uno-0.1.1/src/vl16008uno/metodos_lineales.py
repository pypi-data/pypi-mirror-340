import numpy as np

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando eliminación de Gauss.
    
    Args:
        A (numpy.ndarray): Matriz de coeficientes de tamaño n x n
        b (numpy.ndarray): Vector de términos independientes de tamaño n
        
    Returns:
        numpy.ndarray: Vector solución x
        
    Example:
        >>> A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
        >>> b = np.array([1, -2, 0])
        >>> x = eliminacion_gauss(A, b)
        >>> print(x)
    """
    n = len(b)
    
    # Eliminación hacia adelante
    for k in range(n-1):
        for i in range(k+1, n):
            factor = A[i,k] / A[k,k]
            A[i,k:] -= factor * A[k,k:]
            b[i] -= factor * b[k]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for k in range(n-1, -1, -1):
        x[k] = (b[k] - np.dot(A[k,k+1:], x[k+1:])) / A[k,k]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.
    """
    n = len(b)
    M = np.hstack([A, b.reshape(-1, 1)])
    
    for k in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(M[k:, k])) + k
        M[[k, max_row]] = M[[max_row, k]]
        
        # Normalizar fila pivote
        M[k] = M[k] / M[k,k]
        
        # Eliminación
        for i in range(n):
            if i != k:
                M[i] = M[i] - M[i,k] * M[k]
    
    return M[:, -1]

def crammer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Crammer.
    """
    det_A = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x

def descomposicion_lu(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando descomposición LU.
    """
    n = len(b)
    L = np.eye(n)
    U = A.copy()
    
    # Descomposición LU
    for k in range(n-1):
        for i in range(k+1, n):
            L[i,k] = U[i,k] / U[k,k]
            U[i,k:] -= L[i,k] * U[k,k:]
    
    # Sustitución hacia adelante (Ly = b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i,:i], y[:i])
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i,i]
    
    return x

def jacobi(A, b, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    """
    n = len(b)
    x = np.zeros(n)
    x_new = np.zeros(n)
    
    for _ in range(max_iter):
        for i in range(n):
            s = np.dot(A[i,:], x) - A[i,i] * x[i]
            x_new[i] = (b[i] - s) / A[i,i]
        
        if np.linalg.norm(x_new - x) < tol:
            break
            
        x = x_new.copy()
    
    return x

def gauss_seidel(A, b, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    """
    n = len(b)
    x = np.zeros(n)
    
    for _ in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i,:i], x[:i])
            s2 = np.dot(A[i,i+1:], x_old[i+1:])
            x[i] = (b[i] - s1 - s2) / A[i,i]
        
        if np.linalg.norm(x - x_old) < tol:
            break
    
    return x