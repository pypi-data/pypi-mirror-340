import unittest
from linear_nonlinear_solver.jacobi import metodo_jacobi

class TestJacobiMethod(unittest.TestCase):

    def test_jacobi_convergence(self):
        A = [[4, -1, 0, 0],
             [-1, 4, -1, 0],
             [0, -1, 4, -1],
             [0, 0, -1, 3]]
        b = [15, 10, 10, 10]
        x0 = [0, 0, 0, 0]
        tol = 1e-10
        max_iterations = 25
        
        solution = metodo_jacobi(A, b, x0, tol, max_iterations)
        expected_solution = [3, 2, 2, 1]  # Expected solution for the given A and b
        
        for s, e in zip(solution, expected_solution):
            self.assertAlmostEqual(s, e, places=5)

    def test_jacobi_non_convergence(self):
        A = [[1, 2],
             [2, 4]]
        b = [1, 2]
        x0 = [0, 0]
        tol = 1e-10
        max_iterations = 10
        
        with self.assertRaises(ValueError):
            metodo_jacobi(A, b, x0, tol, max_iterations)

if __name__ == '__main__':
    unittest.main()