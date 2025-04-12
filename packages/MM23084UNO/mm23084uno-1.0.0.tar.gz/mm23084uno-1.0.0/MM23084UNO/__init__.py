### MM23084UNO/__init__.py

from .gauss import resolver_gauss
from .gauss_jordan import resolver_gauss_jordan
from .cramer import resolver_cramer
from .lu import resolver_lu
from .jacobi import resolver_jacobi
from .gauss_seidel import resolver_gauss_seidel
from .biseccion import biseccion

__all__ = [
    "resolver_gauss",
    "resolver_gauss_jordan",
    "resolver_cramer",
    "resolver_lu",
    "resolver_jacobi",
    "resolver_gauss_seidel",
    "biseccion"
]
