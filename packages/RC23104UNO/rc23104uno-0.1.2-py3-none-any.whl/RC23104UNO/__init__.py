from .metodos_lineales import (
    eliminacion_gauss,
    gauss_jordan,
    crammer,
    descomposicion_lu,
    jacobi,          # Asegúrate de que esté aquí
    gauss_seidel
)

from .metodos_no_lineales import biseccion

__all__ = [
    'eliminacion_gauss',
    # ... otros métodos ...
    'jacobi',        # Y aquí
    'biseccion'
]