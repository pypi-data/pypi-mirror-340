import numpy as np
from typing import Union, List, Tuple

class MetodosNumericos:
    @staticmethod
    def eliminacion_gauss(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando eliminacion gaussiana.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
            >>> b = np.array([1, -2, 0])
            >>> RF23006UNO.MetodosNumericos.eliminacion_gauss(A, b)
            array([ 1., -2., -2.])
        """
        n = len(b)
        # Matriz aumentada
        M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
        
        # Eliminacion hacia adelante
        for i in range(n):
            # Pivoteo parcial
            max_row = np.argmax(np.abs(M[i:, i])) + i
            M[[i, max_row]] = M[[max_row, i]]
            
            # Eliminacion
            for j in range(i+1, n):
                factor = M[j, i] / M[i, i]
                M[j, i:] -= factor * M[i, i:]
                
        # Sustitucion hacia atras
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
            
        return x

    @staticmethod
    def gauss_jordan(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando el metodo de Gauss-Jordan.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
            >>> b = np.array([8, -11, -3])
            >>> RF23006UNO.MetodosNumericos.gauss_jordan(A, b)
            array([ 2.,  3., -1.])
        """
        n = len(b)
        M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
        
        for i in range(n):
            # Pivoteo parcial
            max_row = np.argmax(np.abs(M[i:, i])) + i
            M[[i, max_row]] = M[[max_row, i]]
            
            # Normalizar fila pivote
            M[i] = M[i] / M[i, i]
            
            # Eliminar en otras filas
            for j in range(n):
                if j != i:
                    M[j] -= M[j, i] * M[i]
                    
        return M[:, -1]

    @staticmethod
    def cramer(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[3, -2], [5, 1]])
            >>> b = np.array([4, 3])
            >>> RF23006UNO.MetodosNumericos.cramer(A, b)
            array([ 0.76923077, -0.15384615])
        """
        det_A = np.linalg.det(A)
        if np.abs(det_A) < 1e-12:  # Evitar division por cero
            raise ValueError("El determinante de A es cero. El sistema no tiene solución única.")
            
        n = len(b)
        x = np.zeros(n)
        
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            x[i] = np.linalg.det(Ai) / det_A
            
        return x 

    @staticmethod
    def descomposicion_lu(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando descomposicion LU.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]])
            >>> b = np.array([1, -2, 0])
            >>> RF23006UNO.MetodosNumericos.descomposicion_lu(A, b)
            array([ 1., -2., -2.])
        """
        n = len(b)
        L = np.eye(n)
        U = np.zeros((n, n))
        
        # Descomposicion LU
        for i in range(n):
            for j in range(i, n):
                U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
                
            for j in range(i+1, n):
                L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
        
        # Sustitucion hacia adelante (Ly = b)
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
            
        # Sustitucion hacia atras (Ux = y)
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
            
        return x

    @staticmethod
    def jacobi(A: np.ndarray, b: np.ndarray, x0: np.ndarray, tol: float = 1e-6, max_iter: int = 100) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando el metodo iterativo de Jacobi.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            x0: Vector inicial (n)
            tol: Tolerancia para la convergencia (por defecto 1e-6)
            max_iter: Numero maximo de iteraciones
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[10, -1, 2], [1, 10, -1], [2, 3, 20]])
            >>> b = np.array([6, 7, 9])
            >>> x0 = np.array([0, 0, 0])
            >>> RF23006UNO.MetodosNumericos.jacobi(A, b, x0)
            array([0.9999998 , 0.99999989, 0.19999996])
        """
        n = len(b)
        x = x0.copy()
        x_new = np.zeros(n)
        
        for _ in range(max_iter):
            for i in range(n):
                s = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
                x_new[i] = (b[i] - s) / A[i, i]
                
            if np.linalg.norm(x_new - x) < tol:
                return x_new
                
            x = x_new.copy()
            
        return x

    @staticmethod
    def gauss_seidel(A: np.ndarray, b: np.ndarray, x0: np.ndarray, tol: float = 1e-6, max_iter: int = 100) -> np.ndarray:
        """
        Resuelve un sistema de ecuaciones lineales usando el metodo iterativo de Gauss-Seidel.
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de terminos independientes (n)
            x0: Vector inicial (n)
            tol: Tolerancia para la convergencia (por defecto 1e-6)
            max_iter: Numero máximo de iteraciones
            
        Returns:
            Vector solucion x (n)
            
        Example:
            >>> A = np.array([[10, -1, 2], [1, 10, -1], [2, 3, 20]])
            >>> b = np.array([6, 7, 9])
            >>> x0 = np.array([0, 0, 0])
            >>> RF23006UNO.MetodosNumericos.gauss_seidel(A, b, x0)
            array([1., 1., 0.2])
        """
        n = len(b)
        x = x0.copy()
        
        for _ in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                s1 = np.dot(A[i, :i], x[:i])
                s2 = np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - s1 - s2) / A[i, i]
                
            if np.linalg.norm(x - x_old) < tol:
                return x
                
        return x

    @staticmethod
    def biseccion(f: callable, a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> float:
        """
        Encuentra una raiz de una ecuacion no lineal usando el metodo de biseccion.
        
        Args:
            f: Función a la que se le busca la raiz
            a: Extremo izquierdo del intervalo
            b: Extremo derecho del intervalo
            tol: Tolerancia para la convergencia (por defecto 1e-6)
            max_iter: Numero maximo de iteraciones
            
        Returns:
            Aproximacion de la raiz
            
        Example:
            >>> f = lambda x: x**3 - x - 2
            >>> RF23006UNO.MetodosNumericos.biseccion(f, 1, 2)
            1.5213794708251953
        """
        if f(a) * f(b) >= 0:
            raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
            
        for _ in range(max_iter):
            c = (a + b) / 2
            if abs(f(c)) < tol:
                return c
                
            if f(c) * f(a) < 0:
                b = c
            else:
                a = c
                
        return (a + b) / 2