import unittest
from linear_nonlinear_solver.lu_decomposition import descomponer_lu, resolver_lu

class TestLUDecomposition(unittest.TestCase):

    def test_descomponer_lu(self):
        A = [[4, 3], [6, 3]]
        L, U = descomponer_lu(A)
        
        # Verificar que L y U son matrices de la misma dimensión que A
        self.assertEqual(len(L), len(A))
        self.assertEqual(len(U), len(A))
        
        # Verificar que A = L * U
        LU = [[sum(a * b for a, b in zip(L_row, U_col)) for U_col in zip(*U)] for L_row in L]
        for i in range(len(A)):
            for j in range(len(A)):
                self.assertAlmostEqual(A[i][j], LU[i][j])

    def test_resolver_lu(self):
        A = [[4, 3], [6, 3]]
        b = [10, 12]
        x = resolver_lu(A, b)
        
        # Verificar que la solución es correcta
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(x[1], 2.0)

if __name__ == '__main__':
    unittest.main()