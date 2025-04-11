import numpy as np

def es_matriz_cuadrada(A):
    """Verifica si una matriz es cuadrada"""
    return A.shape[0] == A.shape[1]

def es_diagonal_dominante(A):
    """Verifica diagonal dominante para Jacobi/Gauss-Seidel"""
    diagonal = np.abs(np.diag(A))
    suma_filas = np.sum(np.abs(A), axis=1) - diagonal
    return np.all(diagonal >= suma_filas)

def verificar_sistema(A, b):
    """Validaciones comunes para sistemas lineales"""
    if not es_matriz_cuadrada(A):
        raise ValueError("La matriz debe ser cuadrada")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Dimensiones incompatibles entre A y b")