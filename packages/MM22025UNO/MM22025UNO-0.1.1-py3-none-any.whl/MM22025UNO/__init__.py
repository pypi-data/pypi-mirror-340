__version__ = "1.0.0"

from .lineales import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu,
    jacobi,
    gauss_seidel
)

from .no_lineales import resolver_biseccion

__all__ = [
    "eliminacion_gauss",
    "gauss_jordan",
    "cramer",
    "descomposicion_lu",
    "jacobi",
    "gauss_seidel",
    "resolver_biseccion"
]