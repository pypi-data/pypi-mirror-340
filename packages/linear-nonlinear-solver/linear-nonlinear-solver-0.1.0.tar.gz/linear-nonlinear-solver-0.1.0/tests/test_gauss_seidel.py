import unittest
from linear_nonlinear_solver.gauss_seidel import metodo_gauss_seidel

class TestGaussSeidel(unittest.TestCase):

    def test_convergence(self):
        A = [[4, -1, 0, 0],
             [-1, 4, -1, 0],
             [0, -1, 4, -1],
             [0, 0, -1, 3]]
        b = [15, 10, 10, 10]
        expected_solution = [5, 5, 5, 5]
        solution = metodo_gauss_seidel(A, b)
        self.assertAlmostEqual(solution[0], expected_solution[0], places=2)
        self.assertAlmostEqual(solution[1], expected_solution[1], places=2)
        self.assertAlmostEqual(solution[2], expected_solution[2], places=2)
        self.assertAlmostEqual(solution[3], expected_solution[3], places=2)

    def test_inconsistent_system(self):
        A = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]]
        b = [1, 2, 3]
        with self.assertRaises(ValueError):
            metodo_gauss_seidel(A, b)

    def test_singular_matrix(self):
        A = [[1, 2],
             [2, 4]]
        b = [5, 10]
        with self.assertRaises(ValueError):
            metodo_gauss_seidel(A, b)

if __name__ == '__main__':
    unittest.main()