import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from SB14009UNO import (
    gauss,
    gauss_jordan,
    cramer,
    lu,
    jacobi,
    gauss_seidel,
    biseccion
)

# Datos de prueba para sistemas lineales
A = [[3, 2], [1, 2]]
b = [5, 5]

def test_gauss():
    x = gauss.gauss_elimination([row[:] for row in A], b[:])
    print("Gauss:", x)

def test_gauss_jordan():
    x = gauss_jordan.gauss_jordan([row[:] for row in A], b[:])
    print("Gauss-Jordan:", x)

def test_cramer():
    x = cramer.cramer(np.array(A, dtype=float), np.array(b, dtype=float))
    print("Cramer:", x)

def test_lu():
    x = lu.lu_solve(np.array(A, dtype=float), np.array(b, dtype=float))
    print("LU:", x)

def test_jacobi():
    x = jacobi.jacobi(A, b)
    print("Jacobi:", x)

def test_gauss_seidel():
    x = gauss_seidel.gauss_seidel(A, b)
    print("Gauss-Seidel:", x)

def test_biseccion():
    f = lambda x: x**3 - x - 2
    raiz = biseccion.biseccion(f, 1, 2)
    print("Bisección:", raiz)

if __name__ == "__main__":
    test_gauss()
    test_gauss_jordan()
    test_cramer()
    test_lu()
    test_jacobi()
    test_gauss_seidel()
    test_biseccion()
