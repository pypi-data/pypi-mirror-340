import numpy as np
import pytest
from mc23015uno.linear_solvers import (
    gauss_elimination,
    gauss_jordan,
    cramer,
    lu_decomposition,
    jacobi,
    gauss_seidel
)

# Matrices de prueba y soluciones esperadas
A1 = np.array([[3., 2., -1.], [2., -2., 4.], [-1., 0.5, -1.]])
b1 = np.array([1., -2., 0.])
expected1 = np.array([1., -2., -2.])

A2 = np.array([[2., 1., -1.], [-3., -1., 2.], [-2., 1., 2.]])
b2 = np.array([8., -11., -3.])
expected2 = np.array([2., 3., -1.])

A3 = np.array([[2., -1., 1.], 
               [1., 3., -1.], 
               [1., 0., 2.]])
b3 = np.array([4., 6., 2.])
# Solución CORRECTA del sistema:
# x1 = 2.666..., x2 = 1.0, x3 = -0.333...
expected3 = np.array([8/3, 1.0, -1/3])  # Usando fracciones para mayor precisión


A4 = np.array([[4., 3., -2.], 
               [1., 1., 0.], 
               [3., 2., 1.]])
b4 = np.array([7., 2., 5.])
expected4 = np.array([1., 1., 0.])  # Solución real del sistema

# Matriz diagonalmente dominante para métodos iterativos
A5 = np.array([[4., 1., -1.], [2., 7., 1.], [1., -3., 12.]])
b5 = np.array([3., 19., 31.])
expected5 = np.array([1., 2., 3.])

def test_gauss_elimination():
    """Prueba el método de eliminación de Gauss"""
    sol1 = gauss_elimination(A1, b1)
    assert np.allclose(sol1, expected1, atol=1e-6)
    
    sol2 = gauss_elimination(A2, b2)
    assert np.allclose(sol2, expected2, atol=1e-6)

def test_gauss_elimination_singular():
    """Prueba que se lance excepción para matriz singular"""
    A = np.array([[1., 2.], [1., 2.]])
    b = np.array([3., 6.])
    with pytest.raises(ValueError, match="La matriz es singular"):
        gauss_elimination(A, b)

def test_gauss_jordan():
    """Prueba el método de Gauss-Jordan"""
    sol1 = gauss_jordan(A1, b1)
    assert np.allclose(sol1, expected1, atol=1e-6)
    
    sol2 = gauss_jordan(A2, b2)
    assert np.allclose(sol2, expected2, atol=1e-6)

def test_gauss_jordan_singular():
    """Prueba que se lance excepción para matriz singular"""
    A = np.array([[1., 1.], [2., 2.]])
    b = np.array([3., 6.])
    with pytest.raises(ValueError, match="La matriz es singular"):
        gauss_jordan(A, b)

def test_cramer():
    """Prueba la regla de Cramer"""
    sol3 = cramer(A3, b3)
    assert np.allclose(sol3, expected3, atol=1e-6)
    
    sol4 = cramer(A4, b4)
    assert np.allclose(sol4, expected4, atol=1e-6)

def test_cramer_singular():
    """Prueba que se lance excepción para matriz singular"""
    A = np.array([[1., 2.], [2., 4.]])
    b = np.array([3., 6.])
    with pytest.raises(ValueError, match="La matriz es singular"):
        cramer(A, b)

def test_lu_decomposition():
    """Prueba la descomposición LU"""
    sol1 = lu_decomposition(A1, b1)
    assert np.allclose(sol1, expected1, atol=1e-6)
    
    sol4 = lu_decomposition(A4, b4)
    assert np.allclose(sol4, expected4, atol=1e-6)

def test_lu_decomposition_singular():
    """Prueba que se lance excepción para matriz singular"""
    A = np.array([[1., 1.], [1., 1.]])
    b = np.array([2., 2.])
    with pytest.raises(ValueError):
        lu_decomposition(A, b)

def test_jacobi():
    """Prueba el método de Jacobi"""
    sol5 = jacobi(A5, b5, tol=1e-8)
    assert np.allclose(sol5, expected5, atol=1e-6)

def test_jacobi_non_convergent():
    """Prueba que se lance excepción cuando no converge"""
    A = np.array([[1., 2.], [3., 4.]])
    b = np.array([5., 6.])
    with pytest.raises(ValueError, match="no convergió"):
        jacobi(A, b, max_iter=10)

def test_gauss_seidel():
    """Prueba el método de Gauss-Seidel"""
    sol5 = gauss_seidel(A5, b5, tol=1e-8)
    assert np.allclose(sol5, expected5, atol=1e-6)

def test_gauss_seidel_non_convergent():
    """Prueba que se lance excepción cuando no converge"""
    A = np.array([[1., 2.], [3., 4.]])
    b = np.array([5., 6.])
    with pytest.raises(ValueError, match="no convergió"):
        gauss_seidel(A, b, max_iter=10)

def test_all_methods_consistency():
    """Prueba que todos los métodos dan la misma solución para un sistema"""
    A = np.array([[4., 3., 2.], [1., 1., 0.], [3., 2., 1.]])
    b = np.array([9., 2., 6.])
    
    methods = [
        gauss_elimination,
        gauss_jordan,
        cramer,
        lu_decomposition
    ]
    
    solutions = [method(A, b) for method in methods]
    
    # Verificar que todas las soluciones son iguales
    for i in range(1, len(solutions)):
        assert np.allclose(solutions[0], solutions[i], atol=1e-6)