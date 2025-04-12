import unittest
from equation_solver import bisection

class TestNonlinearMethods(unittest.TestCase):

    def test_bisection(self):
        def f(x): return x**3 - x - 2 
        root = bisection(f, 1, 2)
        self.assertAlmostEqual(root, 1.52138, places=4)

if __name__ == "__main__":
    unittest.main()
