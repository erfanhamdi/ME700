import pytest
import numpy as np
import sympy as sp  
from newton_raphson_script import newton_raphson, J_inv, is_square, NewtonResult
from dataclasses import fields

def test_result_storage():
    """Test if the result object stores iterations and errors"""
    output_instance = NewtonResult(1.0, [1.0, 0.5], [0.5], True, 2)
    assert output_instance.root == 1.0
    assert output_instance.iterations == [1.0, 0.5]
    assert output_instance.errors == [0.5]

def test_polynomial():
    """Test Newton-Raphson with polynomial function"""
    f = lambda x: x**3 - 2*x - 5
    J = lambda x: 3*x**2 - 2
    result = newton_raphson(f, J, init_guess=2.0)
    assert abs(f(result.root)) < 1e-6
    assert result.converged
    assert len(result.iterations) > 0
    assert len(result.errors) == len(result.iterations) - 1

def test_sympy():
    """Test Newton-Raphson with sympy function"""
    x = sp.symbols('x')
    f = 3 * x**2 - 2
    J = sp.diff(f, x)
    f = sp.lambdify(x, f)
    J = sp.lambdify(x, J)
    result = newton_raphson(f, J, init_guess=2.0)
    assert abs(f(result.root)) < 1e-6
    assert result.converged

def test_inverse():
    """Test inverse calculation"""
    A = np.array([[1, 2], [3, 4]])
    A_inv = J_inv(A)
    assert np.allclose(A @ A_inv, np.eye(2))

def test_pseudo_inverse_scalar():
    """Testing the inverse calculation for a scalar jacobian"""
    A = np.array([2])
    A_inv = J_inv(A)
    assert np.allclose(A_inv, 1/A)

def test_is_square():
    """Test square matrix check"""
    A = np.array([[1, 2], [3, 4]])
    assert is_square(A)
    A = np.array([[1, 2], [3, 4], [5, 6]])
    assert not is_square(A)

def test_max_iterations():
    """Test maximum iterations limit"""
    f = lambda x: np.tan(x)  # Function with multiple roots
    J = lambda x: 1/np.cos(x)**2
    result = newton_raphson(f, J, init_guess=1.0, max_iter=5)
    assert len(result.iterations) <= 5

def test_linear_equation():
    """Test linear equation, which should converge in one iteration"""
    f = lambda x: 2*x - 3
    J = lambda x: 2
    result = newton_raphson(f, J, init_guess=1.0)
    assert abs(f(result.root)) < 1e-6
    assert result.converged
    assert result.iterations_count == 1

def test_tolerance():
    """Test custom tolerance"""
    f = lambda x: x**2 - 2
    J = lambda x: 2*x
    result = newton_raphson(f, J, init_guess=1.5, tol=1e-3)
    assert abs(f(result.root)) < 1e-3

def test_non_convergence():
    """Test case where method doesn't converge"""
    f = lambda x: np.exp(x)  # Function with no real roots
    J = lambda x: np.exp(x)
    result = newton_raphson(f, J, init_guess=0.0, max_iter=10)
    assert not result.converged

def test_result_attributes():
    """Test if result object has all required attributes"""
    f = lambda x: x**2 - 4
    J = lambda x: 2*x
    result = newton_raphson(f, J, init_guess=1.0)
    expected_attrs = {'root', 'iterations', 'errors', 'converged', 'iterations_count'}
    result_attrs = {field.name for field in fields(result)}
    assert expected_attrs.issubset(result_attrs)

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=main', '--cov-report=term-missing']) 