from .linear_systems import gauss_elimination, gauss_jordan, cramer, lu_decomposition, jacobi, gauss_seidel
from .nonlinear_systems import bisection

__version__ = '0.1.0'
__all__ = ['gauss_elimination', 'gauss_jordan', 'cramer', 'lu_decomposition', 
           'jacobi', 'gauss_seidel', 'bisection']