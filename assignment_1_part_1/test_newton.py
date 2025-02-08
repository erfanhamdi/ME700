import pytest
import numpy as np
from main import newton_raphson
from dataclasses import fields

def test_polynomial():
    """Test Newton-Raphson with polynomial function"""
    f = lambda x: x**3 - 2*x - 5
    result = newton_raphson(f, x0=2.0)
    assert abs(f(result.root)) < 1e-6
    assert result.converged
    assert len(result.iterations) > 0
    assert len(result.errors) == len(result.iterations) - 1

def test_transcendental():
    """Test with transcendental equation"""
    f = lambda x: np.cos(x) - x
    result = newton_raphson(f, x0=1.0)
    assert abs(f(result.root)) < 1e-6
    assert result.converged

def test_beam_deflection():
    """Test beam deflection calculation"""
    E = 2e6
    P = 1000
    L = 2
    def beam_deflection(x):
        return P*x**3/(6*E) - P*L**3/(3*E)
    f = lambda x: beam_deflection(x) + 0.002
    result = newton_raphson(f, x0=1.0)
    assert abs(f(result.root)) < 1e-6

def test_colebrook():
    """Test Colebrook equation"""
    Re = 1e5
    eps = 0.0002
    D = 0.1
    def colebrook(f):
        return 1/np.sqrt(f) + 2*np.log10(eps/(3.7*D) + 2.51/(Re*np.sqrt(f)))
    result = newton_raphson(colebrook, x0=0.02)
    assert abs(colebrook(result.root)) < 1e-6

def test_complex_function():
    """Test complex function"""
    f = lambda x: x*np.exp(x) - 2
    result = newton_raphson(f, x0=1.0)
    assert abs(f(result.root)) < 1e-6

def test_max_iterations():
    """Test maximum iterations limit"""
    f = lambda x: np.tan(x)  # Function with multiple roots
    result = newton_raphson(f, x0=1.0, max_iterations=5)
    assert len(result.iterations) <= 5

def test_tolerance():
    """Test custom tolerance"""
    f = lambda x: x**2 - 2
    result = newton_raphson(f, x0=1.5, tolerance=1e-3)
    assert abs(f(result.root)) < 1e-3

def test_non_convergence():
    """Test case where method doesn't converge"""
    f = lambda x: np.exp(x)  # Function with no real roots
    result = newton_raphson(f, x0=0.0, max_iterations=10)
    assert not result.converged

def test_result_attributes():
    """Test if result object has all required attributes"""
    f = lambda x: x**2 - 4
    result = newton_raphson(f, x0=1.0)
    expected_attrs = {'root', 'iterations', 'errors', 'converged', 'iterations_count'}
    result_attrs = {field.name for field in fields(result)}
    assert expected_attrs.issubset(result_attrs)

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=main', '--cov-report=term-missing']) 