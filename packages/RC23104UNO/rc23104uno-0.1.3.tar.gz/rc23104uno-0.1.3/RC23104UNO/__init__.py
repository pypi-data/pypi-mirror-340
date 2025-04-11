from .metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    crammer,
    descomposicion_lu,
    jacobi,          # solo poner los metdos aqui
    gauss_seidel
)

from .metodos_no_lineales import biseccion

__all__ = [
    'eliminacion_gauss',
    # y los otros métodos ...
    'jacobi',        # Y aquí
    'biseccion'
]