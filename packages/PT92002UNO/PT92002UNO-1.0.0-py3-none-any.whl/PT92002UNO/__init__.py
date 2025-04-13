"""
PT92002UNO - Librería de métodos numéricos para sistemas de ecuaciones

Esta librería proporciona implementaciones de varios métodos numéricos para resolver:
- Sistemas de ecuaciones lineales: Eliminación de Gauss, Gauss-Jordan, Cramer, LU
- Sistemas no lineales: Jacobi, Gauss-Seidel
- Ecuaciones no lineales: Bisección

Autor: [Frany Esmeralda Peña Tobar]
Carnet: PT92002
Versión: 1.0.0
"""

from .metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu
)

from .metodos_no_lineales import (
    jacobi,
    gauss_seidel,
    biseccion
)

__version__ = "1.0.0"
__author__ = "[Tu Nombre] <tu@email.com>"
__all__ = [
    'eliminacion_gauss',
    'gauss_jordan',
    'cramer',
    'descomposicion_lu',
    'jacobi',
    'gauss_seidel',
    'biseccion'
]                        