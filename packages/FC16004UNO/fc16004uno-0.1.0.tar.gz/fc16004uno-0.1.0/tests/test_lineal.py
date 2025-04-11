from fc16004uno.lineal import eliminacion_gauss, gauss_jordan, cramer
from fc16004uno.lineal import descomposicion_lu, jacobi, gauss_seidel

def test_eliminacion_gauss():
    A = [[2, -1, 1], [3, 3, 9], [3, 3, 5]]
    b = [8, 0, -6]
    x = eliminacion_gauss.gauss_elimination([row[:] for row in A], b[:])
    print("Gauss:", x)

def test_gauss_jordan():
    A = [[2, 1], [5, 7]]
    b = [11, 13]
    x = gauss_jordan.gauss_jordan([row[:] for row in A], b[:])
    print("Gauss-Jordan:", x)

def test_cramer():
    A = [[1, 2], [3, 4]]
    b = [5, 6]
    x = cramer.cramer([row[:] for row in A], b[:])
    print("Cramer:", x)

def test_lu():
    A = [[2, 3], [5, 4]]
    b = [8, 2]
    x = descomposicion_lu.lu_decomposition([row[:] for row in A], b[:])
    print("LU:", x)

def test_jacobi():
    A = [[4, -1, 0], [-1, 4, -1], [0, -1, 3]]
    b = [15, 10, 10]
    x = jacobi.jacobi([row[:] for row in A], b[:])
    print("Jacobi:", x)

def test_gauss_seidel():
    A = [[4, -1, 0], [-1, 4, -1], [0, -1, 3]]
    b = [15, 10, 10]
    x = gauss_seidel.gauss_seidel([row[:] for row in A], b[:])
    print("Gauss-Seidel:", x)

if __name__ == "__main__":
    test_eliminacion_gauss()
    test_gauss_jordan()
    test_cramer()
    test_lu()
    test_jacobi()
    test_gauss_seidel()