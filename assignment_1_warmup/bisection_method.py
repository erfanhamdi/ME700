import numpy as np
import matplotlib.pyplot as plt

def plotter_function(f, c_history, title = None, plotting_interval = [-5, 5]):
    a_, b_ = plotting_interval
    x = np.linspace(a_, b_, 300)
    plt.figure(figsize=(8, 6))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$f(x)$')
    plt.axhline(y = 0, color = 'lightgray', zorder = 1)
    plt.axvline(x = 0, color = 'lightgray', zorder = 1)
    plt.plot(x, f(x), zorder = 1)
    # plotting the steps to the root and changing the transparency at each step
    alpha_step = 1 / len(c_history)
    for idx, c_ in enumerate(c_history):
        plt.scatter(c_, f(c_), color = 'b', s = 42, alpha = (idx + 1) * alpha_step)
    plt.scatter(c_history[-1], f(c_), color = 'r', s = 42)
    if title is not None:
        plt.tight_layout()
        plt.savefig(f"./figs/{title}.png", dpi = 150, transparent=True)
    plt.show()

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
        if error < TOL:
            return c, f(c)
    if i == max_iter-1:
        raise ValueError("Max iter reached, No roots found")

if __name__=="__main__":
    # Example usage
    ## a: lower bound of the interval
    a = 0
    ## b: upper bound of the interval
    b = 2
    max_iter = 100
    # f: function to find the root
    K = 1
    l = 1
    F = 1.5
    a_ = 1
    b_ = 10
    f = lambda x: (x-0.5)**3 
    # f = lambda w: 2*K*(np.sqrt(l**2 + w**2) - l) * (w)/(np.sqrt(l**2 + w**2)) - F
    # f = lambda phi: (phi*np.pi/180)/np.sin(phi*np.pi/180) - F*l/K
    # f = lambda x: np.sin(5 * x) + x**3 - x
    f = lambda x: (a_ - x)**2 + b_*(1-x**2)**2 - 15
    x = np.linspace(-1, 2, 300)
    plt.plot(x, f(x))
    plt.grid()
    plt.show()
    c, f_c, c_history = bisect(f, [a, b], max_iter, TOL = 1e-3)
    print(f"root = {c}")
    # Plotting the results and steps to the root
    # plotter_function(f, c_history,  "eq3", [-1, 2])