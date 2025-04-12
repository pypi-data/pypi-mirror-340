"""
Librería para resolver sistemas de ecuaciones lineales y no lineales

Esta librería implementa los siguientes métodos:
- Eliminación de Gauss
- Gauss-Jordan
- Crammer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección
"""

from .metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    crammer,
    descomposicion_lu,
    jacobi,
    gauss_seidel
)
from .metodos_no_lineales import biseccion

__all__ = [
    'eliminacion_gauss',
    'gauss_jordan',
    'crammer',
    'descomposicion_lu',
    'jacobi',
    'gauss_seidel',
    'biseccion'
]