from .lineales import ( #esto permite importar modularmente: from rp23005uno.lineales import crammer 
    crammer,                                                 #from rp23005uno.no_lineales import bisection
    gauss_elimination,
    gauss_jordan,
    lu_solver,
    jacobi,
    gauss_seidel
)

from .no_lineales import (
    bisection
)

__all__ = [  #esto permite importar: from rp23005uno import cramer, bisection
    "crammer",
    "gauss_elimination",
    "gauss_jordan",
    "lu_solver",
    "jacobi",
    "gauss_seidel",
    "bisection"
]
