import os
import pytest
from src.bisection_method import not_the_same_sign, take_average, is_root, bisect, plotter_function

def test_positive_and_negative():
    assert not_the_same_sign(3, -2) == True

def test_negative_and_positive():
    assert not_the_same_sign(-1, 4) == True

def test_positive_and_positive():
    assert not_the_same_sign(2, 5) == False

def test_negative_and_negative():
    assert not_the_same_sign(-3, -6) == False

def test_take_average():
    assert take_average(1, 3) == 2

f = lambda x: x**2 - 4

def test_bisect_root():
    root, value, _ = bisect(f, (-2, 2), 100)
    assert pytest.approx(value, abs=1e-6) == 0
    
def test_is_root_bigger_than_tol():
    assert is_root(f, 2 + 1e-7, TOL=1e-12) == False

def tet_is_root_smaller_than_tol():
    assert is_root(f, 2 + 1e-13, TOL=1e-12) == True

def test_bisect_root():
    root, value, _ = bisect(f, (-2, 2), 100)
    assert pytest.approx(value, abs=1e-6) == 0

def test_bisect_tolerance():
    root, value, _ = bisect(f, (-2, 2), 100, TOL=1e-8)
    assert pytest.approx(value, abs=1e-8) == 0

def test_bisect_max_iterations():
    with pytest.raises(ValueError, match = "Max iter reached, No roots found"):
        root, value, _ = bisect(f, (-2, 2), 1)

def test_plotter_function():
    root, value, c_history = bisect(f, (-2, 2), 100, TOL=1e-8)
    plotter_function(f, c_history, "eqtest", [-2, 2])
    # Check if the file is created
    assert os.path.exists("/Users/erfan/Documents/Courses/ME700-push/figs/eqtest.png") == True
