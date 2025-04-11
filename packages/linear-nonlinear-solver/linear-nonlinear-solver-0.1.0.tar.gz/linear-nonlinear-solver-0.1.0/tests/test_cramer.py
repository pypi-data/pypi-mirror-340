import unittest
from linear_nonlinear_solver.cramer import resolver_cramer

class TestCramerMethod(unittest.TestCase):

    def test_resolver_cramer(self):
        # Test case 1: Simple 2x2 system
        A = [[2, 1], [1, 3]]
        B = [8, 13]
        expected = [3, 2]
        result = resolver_cramer(A, B)
        self.assertEqual(result, expected)

        # Test case 2: Simple 3x3 system
        A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        B = [14, 13, 12]
        expected = [1, 2, 3]
        result = resolver_cramer(A, B)
        self.assertEqual(result, expected)

        # Test case 3: No solution
        A = [[1, 2], [2, 4]]
        B = [5, 10]
        with self.assertRaises(ValueError):
            resolver_cramer(A, B)

        # Test case 4: Infinite solutions
        A = [[1, 2], [2, 4]]
        B = [5, 10]
        with self.assertRaises(ValueError):
            resolver_cramer(A, B)

if __name__ == '__main__':
    unittest.main()