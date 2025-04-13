"""
MC23152UNO - Librería de métodos numéricos

Esta librería implementa varios métodos para resolver sistemas de ecuaciones lineales y no lineales.
"""

from .metodos import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu,
    jacobi,
    gauss_seidel,
    biseccion
)

__all__ = [
    'eliminacion_gauss',
    'gauss_jordan',
    'cramer',
    'descomposicion_lu',
    'jacobi',
    'gauss_seidel',
    'biseccion'
]