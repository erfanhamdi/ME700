# Bisection Method

## Overview
Bisection root finding method is implemented in this script.

## Dependencies
- Python 3.8 or higher
- `numpy 2.2.* `
- `matplotlib 3.10.*`

## Setup and Usage
1. Clone or download the code.
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. you can define your function using either a lambda function or regular python function.
* Example: To find roots of:
$$y = x^2 - 4$$ 
* Using lambda functions:
```python
f = lambda x: x**2 - 4
```
* Using python functions:
```python
def f(x):
    return x**2 - 4
```
4. Define the interval (`2D list`), maximum number of iterations (`int`), and the stopping tolerance (`float`) and Give the function as well as all theser parameters as the input to the `bisection()` function in  `bisection_method.py`:
```python
from bisection_method import bisect
interval = [0, 2]
max_iter = 100
TOL = 1e-6
root, func_val_at_root, root_history = bisect(f, interval, max_iter, TOL)
```