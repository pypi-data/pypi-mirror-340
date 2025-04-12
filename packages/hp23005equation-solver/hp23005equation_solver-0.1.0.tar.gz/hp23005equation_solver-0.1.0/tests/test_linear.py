import unittest
import numpy as np
from equation_solver import (
    gauss_elimination,
    gauss_jordan,
    cramer,
    lu_decomposition,
    jacobi,
    gauss_seidel,
)

class TestLinearMethods(unittest.TestCase):

    def setUp(self):
        self.A = np.array([[10, 1], [2, 10]])
        self.b = np.array([11, 12])
        self.expected = np.array([1, 1])

    def assertArrayAlmostEqual(self, result, expected, places=5):
        for r, e in zip(result, expected):
            self.assertAlmostEqual(r, e, places=places)

    def test_gauss_elimination(self):
        result = gauss_elimination(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

    def test_gauss_jordan(self):
        result = gauss_jordan(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

    def test_cramer(self):
        result = cramer(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

    def test_lu_decomposition(self):
        result = lu_decomposition(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

    def test_jacobi(self):
        result = jacobi(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

    def test_gauss_seidel(self):
        result = gauss_seidel(self.A, self.b)
        self.assertArrayAlmostEqual(result, self.expected)

if __name__ == "__main__":
    unittest.main()
