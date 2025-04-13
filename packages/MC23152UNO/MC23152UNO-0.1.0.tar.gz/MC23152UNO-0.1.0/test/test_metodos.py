import unittest
import numpy as np
from MC23152UNO import (
    eliminacion_gauss,
    gauss_jordan,
    cramer,
    descomposicion_lu,
    jacobi,
    gauss_seidel,
    biseccion
)

class TestMetodosNumericos(unittest.TestCase):
    def setUp(self):
        self.A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
        self.b = np.array([1, -2, 0])
        self.solucion = np.array([1, -2, -2])
    
    def test_eliminacion_gauss(self):
        x = eliminacion_gauss(self.A, self.b)
        np.testing.assert_array_almost_equal(x, self.solucion)
    
    def test_gauss_jordan(self):
        x = gauss_jordan(self.A, self.b)
        np.testing.assert_array_almost_equal(x, self.solucion)

if __name__ == '__main__':
    unittest.main()