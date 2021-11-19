import numpy as np
import mpmath as mp
# Integration solver
from scipy.integrate import solve_ivp

# Calcul of the bi-logistic function
def simple_logistic(T, l, k, t0):
    """Definition of a logistic function."""
    res = l / (1. + np.exp(-k * (T - t0)))
    return T, res

# Use for minimization
def simple_logistic_weight(params, x, y, incert):
    """Definition of the logistic function to be minimized."""
    _, y_vals = simple_logistic(x, params['l'],
                                   params['k'],
                                   params['t0'])
    return (y_vals - y) / incert
