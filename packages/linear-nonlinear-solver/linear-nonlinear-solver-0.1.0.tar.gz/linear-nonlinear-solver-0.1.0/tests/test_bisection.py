import unittest
from linear_nonlinear_solver.bisection import biseccion

class TestBisectionMethod(unittest.TestCase):

    def test_bisection_root(self):
        # Test function: f(x) = x^2 - 4, root at x = 2
        def f(x):
            return x**2 - 4
        
        root = biseccion(f, 1, 3, tol=1e-5)
        self.assertAlmostEqual(root, 2, places=5)

    def test_bisection_no_root(self):
        # Test function: f(x) = x^2 + 1, no root in the interval [0, 1]
        def f(x):
            return x**2 + 1
        
        with self.assertRaises(ValueError):
            biseccion(f, 0, 1, tol=1e-5)

    def test_bisection_multiple_roots(self):
        # Test function: f(x) = cos(x) - x, root near x = 0.739
        import math
        def f(x):
            return math.cos(x) - x
        
        root = biseccion(f, 0, 1, tol=1e-5)
        self.assertAlmostEqual(root, 0.739085, places=5)

if __name__ == '__main__':
    unittest.main()