import unittest
from linear_nonlinear_solver.gauss_jordan import gauss_jordan

class TestGaussJordan(unittest.TestCase):

    def test_simple_system(self):
        A = [[2, 1, -1],
             [-3, -1, 2],
             [-2, 1, 2]]
        b = [8, -11, -3]
        expected_solution = [2, 3, -1]
        self.assertEqual(gauss_jordan(A, b), expected_solution)

    def test_no_solution(self):
        A = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        b = [1, 2, 3]
        with self.assertRaises(ValueError):
            gauss_jordan(A, b)

    def test_infinite_solutions(self):
        A = [[1, 2, 3],
             [2, 4, 6],
             [0, 0, 0]]
        b = [1, 2, 0]
        with self.assertRaises(ValueError):
            gauss_jordan(A, b)

if __name__ == '__main__':
    unittest.main()