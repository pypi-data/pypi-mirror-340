import copy

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for c in range(n):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1)**c) * matrix[0][c] * determinant(minor)
    return det

def cramer(A, b):
    n = len(b)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("La matriz no tiene solución única.")
    results = []
    for i in range(n):
        Ai = copy.deepcopy(A)
        for j in range(n):
            Ai[j][i] = b[j]
        results.append(determinant(Ai) / det_A)
    return results