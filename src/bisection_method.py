import numpy as np
import matplotlib.pyplot as plt

def not_the_same_sign(f_a, f_b):
    return f_a * f_b < 0

def take_average(a, b):
    return (a + b) / 2

def is_root(f, x, TOL=1e-6):
    return np.abs(f(x)) < TOL

def bisect(f, interval, max_iter, TOL=1e-6):
    c_history = []
    # Adding an epsilon to the brackets to cover the case that one of the interval ends might be the root
    epsilon = 1e-3
    a = interval[0] - epsilon
    b = interval[1] + epsilon
    for i in range(max_iter):
        c = 0.1
        if not_the_same_sign(f(a), f(b)):
            c = take_average(a, b)
            c_history.append(c)
        if not_the_same_sign(f(c), f(a)) and np.abs(f(c)) > TOL :
            b = c
        elif np.abs(f(c)) < TOL:
            return c, f(c), c_history
        else:
            a = c
        error = np.abs(f(c))
        print(f"iteration: {i} - error = {error}")
    if i == max_iter-1:
        raise ValueError("Max iter reached, No roots found")