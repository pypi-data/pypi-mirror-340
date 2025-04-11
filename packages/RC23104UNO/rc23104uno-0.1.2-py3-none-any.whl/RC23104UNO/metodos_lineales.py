import numpy as np
from .utils import es_diagonal_dominante, verificar_sistema

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando eliminación de Gauss.
    
    Args:
        A: Matriz de coeficientes (n x n)
        b: Vector de términos independientes (n)
        
    Returns:
        Vector solución x
    """
    verificar_sistema(A, b)
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Eliminación
        for j in range(i+1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.
    """
    verificar_sistema(A, b)
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Normalizar fila pivote
        M[i] = M[i] / M[i, i]
        
        # Eliminación en todas las filas
        for j in range(n):
            if j != i:
                factor = M[j, i]
                M[j] -= factor * M[i]
    
    return M[:, -1]

def crammer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Crammer.
    """
    verificar_sistema(A, b)
    det_A = np.linalg.det(A)
    if np.isclose(det_A, 0):
        raise ValueError("La matriz es singular (determinante cero)")
    
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
    verificar_sistema(A, b)
    n = len(b)
    L = np.eye(n)
    U = np.zeros((n, n))
    
    # Descomposición LU
    for i in range(n):
        for j in range(i, n):
            U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
        
        for j in range(i+1, n):
            L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
    
    # Sustitución hacia adelante (Ly = b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:n], x[i+1:n])) / U[i, i]
    
    return x

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    """
    verificar_sistema(A, b)
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    if not es_diagonal_dominante(A):
        print("Advertencia: La matriz no es diagonal dominante - convergencia no garantizada")
    
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
    """
    verificar_sistema(A, b)
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