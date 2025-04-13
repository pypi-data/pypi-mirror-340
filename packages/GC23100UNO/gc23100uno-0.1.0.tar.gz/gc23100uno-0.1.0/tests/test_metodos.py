import unittest
import numpy as np
from GC23100UNO.metodos_numericos import MetodosNumericos

class TestMetodosNumericos(unittest.TestCase):
    
    def setUp(self):
        # Sistema lineal de prueba 3x3
        self.A3 = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]], dtype=float)
        self.b3 = np.array([1, -2, 0], dtype=float)
        self.sol3 = np.array([1, -2, -2])
        
        # Sistema lineal de prueba 2x2
        self.A2 = np.array([[2, -1], [-1, 2]], dtype=float)
        self.b2 = np.array([1, 0], dtype=float)
        self.sol2 = np.array([2/3, 1/3])
        
        # Función para bisección
        self.f = lambda x: x**2 - 2
        self.raiz = np.sqrt(2)
    
    def test_gauss(self):
        x = MetodosNumericos.EliminacionGauss(self.A3, self.b3)
        np.testing.assert_array_almost_equal(x, self.sol3, decimal=6)
        
    def test_gauss_jordan(self):
        x = MetodosNumericos.GaussJordan(self.A3, self.b3)
        np.testing.assert_array_almost_equal(x, self.sol3, decimal=6)
        
    def test_crammer(self):
        x = MetodosNumericos.Crammer(self.A3, self.b3)
        np.testing.assert_array_almost_equal(x, self.sol3, decimal=6)
        
    def test_lu(self):
        x = MetodosNumericos.DescomposicionLU(self.A3, self.b3)
        np.testing.assert_array_almost_equal(x, self.sol3, decimal=6)
        
    def test_jacobi(self):
        x = MetodosNumericos.Jacobi(self.A2, self.b2)
        np.testing.assert_array_almost_equal(x, self.sol2, decimal=6)
        
    def test_gauss_seidel(self):
        x = MetodosNumericos.GaussSeidel(self.A2, self.b2)
        np.testing.assert_array_almost_equal(x, self.sol2, decimal=6)
        
    def test_biseccion(self):
        raiz = MetodosNumericos.Biseccion(self.f, 1, 2)
        self.assertAlmostEqual(raiz, self.raiz, places=6)

if __name__ == '__main__':
    unittest.main()