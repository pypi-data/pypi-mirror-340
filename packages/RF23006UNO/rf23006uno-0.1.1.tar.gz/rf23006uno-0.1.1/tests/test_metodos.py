import numpy as np
import pytest
from RF23006UNO import MetodosNumericos

TOL = 1e-6

class TestEliminacionGauss:
    def test_sistema_3x3(self):
        A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]], dtype=float)
        b = np.array([1, -2, 0], dtype=float)
        x = MetodosNumericos.eliminacion_gauss(A, b)
        expected = np.array([1., -2., -2.])
        assert np.allclose(x, expected, atol=TOL)

class TestGaussJordan:
    def test_sistema_3x3(self):
        A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
        b = np.array([8, -11, -3], dtype=float)
        x = MetodosNumericos.gauss_jordan(A, b)
        expected = np.array([2., 3., -1.])
        assert np.allclose(x, expected, atol=TOL)

class TestCramer:
    def test_sistema_2x2(self):
        A = np.array([[3, -2], [5, 1]], dtype=float)
        b = np.array([4, 3], dtype=float)
        x = MetodosNumericos.cramer(A, b)
        expected = np.array([10/13, -11/13])
        assert np.allclose(x, expected, atol=TOL)

class TestDescomposicionLU:
    def test_sistema_3x3(self):
        A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]], dtype=float)
        b = np.array([1, -2, 0], dtype=float)
        x = MetodosNumericos.descomposicion_lu(A, b)
        expected = np.array([1., -2., -2.])
        assert np.allclose(x, expected, atol=TOL)

class TestJacobi:
    def test_sistema_convergente(self):
        A = np.array([[15, -1, 2], [1, 18, -1], [2, 3, 25]], dtype=float)
        b = np.array([6, 7, 9], dtype=float)
        x0 = np.zeros(3)
        x = MetodosNumericos.jacobi(A, b, x0, tol=TOL)
        expected = np.linalg.solve(A, b)
        assert np.allclose(x, expected, atol=TOL)

class TestGaussSeidel:
    def test_sistema_convergente(self):
        A = np.array([[15, -1, 2], [1, 18, -1], [2, 3, 25]], dtype=float)
        b = np.array([6, 7, 9], dtype=float)
        x0 = np.zeros(3)
        x = MetodosNumericos.gauss_seidel(A, b, x0, tol=TOL)
        expected = np.linalg.solve(A, b)
        assert np.allclose(x, expected, atol=TOL)

class TestBiseccion:
    def test_raiz_polinomio(self):
        f = lambda x: x**3 - x - 2
        raiz = MetodosNumericos.biseccion(f, 1, 2, tol=TOL)
        assert abs(f(raiz)) < TOL

    def test_intervalo_invalido(self):
        f = lambda x: x**2 - 2
        with pytest.raises(ValueError):
            MetodosNumericos.biseccion(f, 0, 1, tol=TOL)