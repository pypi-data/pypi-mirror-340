"""
HA23039UNO - Librería para resolver sistemas de ecuaciones lineales y no lineales.

Métodos implementados:
- Sistemas lineales:
  * Eliminación de Gauss
  * Gauss-Jordan
  * Cramer
  * Descomposición LU
  * Jacobi
  * Gauss-Seidel
- Sistemas no lineales:
  * Bisección
"""

from .linear_methods import (
    gauss_elimination,
    gauss_jordan,
    cramer,
    lu_decomposition,
    jacobi,
    gauss_seidel
)

from .nonlinear_methods import bisection

__version__ = '0.1.0'
__all__ = [
    'gauss_elimination',
    'gauss_jordan',
    'cramer',
    'lu_decomposition',
    'jacobi',
    'gauss_seidel',
    'bisection'
]