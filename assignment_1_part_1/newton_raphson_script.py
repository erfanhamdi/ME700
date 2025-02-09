import numpy as np
import sympy as sp
from typing import Callable, List
from dataclasses import dataclass

@dataclass
class NewtonResult:
    """Class to store Newton-Raphson method results"""
    root: float
    iterations: List[float]
    errors: List[float]
    converged: bool
    iterations_count: int

def is_square(J):
    """Check if a matrix is square"""
    try:
        return J.shape[0] == J.shape[1]
    except:
        return False

def J_inv(J):
    """Calculate the inverse of the Jacobian"""
    if is_square(J) == False:
        # Psuedo inverse always exists so no need for a try/except block!
        try:
            return np.linalg.pinv(J).T
        except np.linalg.LinAlgError:
            return np.array([1/(J+1e-8)])
    else:
        try:
            return np.linalg.inv(J)
        except np.linalg.LinAlgError:
            print("Jacobian is singular. Stopping iterations.")
            return None
    
def newton_raphson(
    f: Callable,
    J: None,
    init_guess: float,
    tol: float = 1e-6,
    max_iter: int = 100,
    store_history: bool = True
) -> NewtonResult:
    """
    Implementation of Newton-Raphson method
    
    Args:
        f: Function to find root for
        J: Jacobian of the function
        init_guess: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum number of iterations
        store_history: Whether to store iteration history
    """
    flag_sym = False
    X = np.array(init_guess)
    iterations = [X] if store_history else []
    errors = []
    if f(X).shape == ():
        X = np.array([init_guess])
    if is_square(J(X)) == False:
        print("Jacobian is not square. using the psudo inverse")
    for i in range(max_iter):
        X_new = X - J_inv(J(X)) @ f(X)
        error_rel = np.linalg.norm(abs(f(X_new)))
        
        if store_history:
            iterations.append(X_new)
            errors.append(error_rel)
            
        if error_rel < tol:
            return NewtonResult(X_new, iterations, errors, True, i + 1)
            
        X = X_new

    return NewtonResult(X, iterations, errors, False, max_iter)

if __name__ == "__main__":

    x = sp.symbols('x')
    f1 = x**3 - 2*x - 5
    J1 = sp.diff(f1, x)
    f1 = sp.lambdify(x, f1)
    J1 = sp.lambdify(x, J1)
    init_guess = 2

    # result = newton_raphson(f1, J1, init_guess=init_guess, max_iter = 1000)
    
    # Print results
    # print(f"Root found: {result.root}")
    # print(f"Converged: {result.converged}")
    # print(f"Number of iterations: {result.iterations_count}")

    from sympy import symbols, sqrt, Eq

# Define variables
    
    # Display the equation
    # print(equation)