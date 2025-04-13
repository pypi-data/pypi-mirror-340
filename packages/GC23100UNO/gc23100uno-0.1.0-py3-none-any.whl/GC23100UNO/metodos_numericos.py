import numpy as np

class MetodosNumericos:
    @staticmethod
    def EliminacionGauss(A, b):
        n = len(b)
        Ab = np.hstack([A, b.reshape(-1, 1)])
        for k in range(n):
            for i in range(k + 1, n):
                factor = Ab[i, k] / Ab[k, k]
                Ab[i, k:] = Ab[i, k:] - factor * Ab[k, k:]
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:n])) / Ab[i, i]
        return x

    @staticmethod
    def GaussJordan(A, b):
        n = len(b)
        Ab = np.hstack([A, b.reshape(-1, 1)])
        for k in range(n):
            Ab[k] = Ab[k] / Ab[k, k]
            for i in range(n):
                if i != k:
                    Ab[i] = Ab[i] - Ab[i, k] * Ab[k]
        return Ab[:, -1]

    @staticmethod
    def Crammer(A, b):
        detA = np.linalg.det(A)
        if abs(detA) < 1e-10:
            raise ValueError("La matriz es singular")
        n = len(b)
        x = np.zeros(n)
        for i in range(n):
            Ai = A.copy()
            Ai[:, i] = b
            x[i] = np.linalg.det(Ai) / detA
        return x

    @staticmethod
    def DescomposicionLU(A, b):
        n = len(b)
        L = np.zeros((n, n))
        U = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
            L[i, i] = 1
            for j in range(i + 1, n):
                L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]
        return x

    @staticmethod
    def Jacobi(A, b, x0=None, tol=1e-10, maxIter=100):
        n = len(b)
        if x0 is None:
            x0 = np.zeros(n)
        x = x0.copy()
        for _ in range(maxIter):
            xNew = np.zeros(n)
            for i in range(n):
                s = sum(A[i][j] * x[j] for j in range(n) if j != i)
                xNew[i] = (b[i] - s) / A[i][i]
            if np.linalg.norm(xNew - x, ord=np.inf) < tol:
                return xNew
            x = xNew
        return x

    @staticmethod
    def GaussSeidel(A, b, x0=None, tol=1e-10, maxIter=100):
        n = len(b)
        if x0 is None:
            x0 = np.zeros(n)
        x = x0.copy()
        for _ in range(maxIter):
            xOld = x.copy()
            for i in range(n):
                s1 = sum(A[i][j] * x[j] for j in range(i))
                s2 = sum(A[i][j] * xOld[j] for j in range(i + 1, n))
                x[i] = (b[i] - s1 - s2) / A[i][i]
            if np.linalg.norm(x - xOld, ord=np.inf) < tol:
                return x
        return x

    @staticmethod
    def Biseccion(f, a, b, tol=1e-10, maxIter=100):
        if f(a) * f(b) >= 0:
            raise ValueError("La funcion no cambia de signo en el intervalo")
        for _ in range(maxIter):
            c = (a + b) / 2
            if f(c) == 0 or (b - a) / 2 < tol:
                return c
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2
