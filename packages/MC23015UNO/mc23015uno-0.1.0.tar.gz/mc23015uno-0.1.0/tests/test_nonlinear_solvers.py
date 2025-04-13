import pytest
from mc23015uno.nonlinear_solvers import bisection
import math

def test_bisection_quadratic():
    """Prueba bisección con una función cuadrática"""
    def f(x):
        return x**2 - 4
    
    root = bisection(f, 0., 3., tol=1e-8)
    assert abs(f(root)) < 1e-6
    assert abs(root - 2) < 1e-6

def test_bisection_cubic():
    """Prueba bisección con una función cúbica"""
    def f(x):
        return x**3 - 2*x - 5
    
    root = bisection(f, 2., 3., tol=1e-8)
    assert abs(f(root)) < 1e-6
    assert abs(root - 2.094551) < 1e-6

def test_bisection_trigonometric():
    """Prueba bisección con una función trigonométrica"""
    def f(x):
        return math.sin(x) - 0.5
    
    root = bisection(f, 0., math.pi/2, tol=1e-8)
    assert abs(f(root)) < 1e-6
    assert abs(root - math.pi/6) < 1e-6

def test_bisection_exponential():
    """Prueba bisección con una función exponencial"""
    def f(x):
        return math.exp(x) - 2
    
    root = bisection(f, 0., 1., tol=1e-8)
    assert abs(f(root)) < 1e-6
    assert abs(root - math.log(2)) < 1e-6

def test_bisection_invalid_interval():
    """Prueba que se lance excepción cuando el intervalo no contiene raíz"""
    def f(x):
        return x**2 + 1
    
    with pytest.raises(ValueError, match="cambiar de signo"):
        bisection(f, 0., 1.)

def test_bisection_max_iterations():
    """Prueba que se alcanza el máximo de iteraciones si la tolerancia es muy pequeña"""
    def f(x):
        return x**2 - 2
    
    root = bisection(f, 0., 2., tol=1e-20, max_iter=10)
    # Aunque no converja completamente, debería devolver una aproximación
    assert abs(root - math.sqrt(2)) < 0.1

def test_bisection_edge_cases():
    """Prueba casos extremos con raíces en los bordes"""
    def f1(x):
        return x - 1.0
    
    # Probar con intervalo que contiene la raíz
    root1 = bisection(f1, 0.5, 1.5)
    assert abs(root1 - 1.0) < 1e-6
    
    def f2(x):
        return x - 2.0
    
    # Probar con intervalo que contiene la raíz
    root2 = bisection(f2, 1.5, 2.5)
    assert abs(root2 - 2.0) < 1e-6