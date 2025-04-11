import numpy as np
import pytest
from RC23104UNO import (
    eliminacion_gauss,
    gauss_jordan,
    crammer,
    descomposicion_lu,
    jacobi,
    gauss_seidel
)

# Sistemas de prueba
A1 = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
b1 = np.array([1, -2, 0])
sol1 = np.array([1, -2, -2])  # Solución correcta para A1

A2 = np.array([[4, -2, 1], [1, 1, 1], [9, 3, 1]])
b2 = np.array([1, 2, 3])
sol2 = np.array([0.03333333, 0.36666667, 1.6])  # Solución corregida para A2

class TestMetodosLineales:
    def test_eliminacion_gauss(self):
        x = eliminacion_gauss(A1, b1)
        assert np.allclose(x, sol1, atol=1e-6)
        
        x = eliminacion_gauss(A2, b2)
        assert np.allclose(x, sol2, atol=1e-6)

    def test_gauss_jordan(self):
        x = gauss_jordan(A1, b1)
        assert np.allclose(x, sol1, atol=1e-6)
        
        x = gauss_jordan(A2, b2)
        assert np.allclose(x, sol2, atol=1e-6)

    def test_crammer(self):
        x = crammer(A1, b1)
        assert np.allclose(x, sol1, atol=1e-6)
        
        x = crammer(A2, b2)
        assert np.allclose(x, sol2, atol=1e-6)

    def test_descomposicion_lu(self):
        x = descomposicion_lu(A1, b1)
        assert np.allclose(x, sol1, atol=1e-6)
        
        x = descomposicion_lu(A2, b2)
        assert np.allclose(x, sol2, atol=1e-6)

    def test_jacobi(self):
        A_jacobi = np.array([[10, -1, 2], [-1, 11, -1], [2, -1, 10]])
        b_jacobi = np.array([6, 25, -11])
        
        x = jacobi(A_jacobi, b_jacobi, max_iter=10000, tol=1e-10)
        # Validación con la ecuación original
        assert np.allclose(np.dot(A_jacobi, x), b_jacobi, atol=1e-6)

    def test_gauss_seidel(self):
        A_seidel = np.array([[16, 3], [7, -11]])
        b_seidel = np.array([11, 13])
        
        x = gauss_seidel(A_seidel, b_seidel, max_iter=10000, tol=1e-10)
        # Validación con la ecuación original
        assert np.allclose(np.dot(A_seidel, x), b_seidel, atol=1e-6)
