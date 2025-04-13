import numpy as np

def eliminacion_gauss(A, b):
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    for i in range(n):
        if np.isclose(M[i, i], 0):
            raise np.linalg.LinAlgError("Matriz singular detectada")
            
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        for j in range(i+1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
    
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
    return x

def gauss_jordan(A, b):
    n = len(b)
    M = np.hstack([A.copy().astype(float), b.copy().reshape(-1, 1).astype(float)])
    
    for i in range(n):
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        pivot = M[i, i]
        if np.isclose(pivot, 0):
            raise np.linalg.LinAlgError("Matriz singular")
        M[i] = M[i] / pivot
        
        for j in range(n):
            if j != i:
                M[j] -= M[j, i] * M[i]
    
    return M[:, -1]

def cramer(A, b):
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz debe ser cuadrada")
        
    A = A.astype(float)
    b = b.astype(float)
    det_A = np.linalg.det(A)
    
    if np.isclose(det_A, 0):
        raise ValueError("Matriz singular")
    
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    return x

def descomposicion_lu(A, b):
    n = len(b)
    L = np.eye(n, dtype=float)
    U = np.zeros((n, n), dtype=float)
    A = A.astype(float)
    b = b.astype(float)
    
    for i in range(n):
        for j in range(i, n):
            U[i, j] = A[i, j] - np.dot(L[i, :i], U[:i, j])
        
        for j in range(i+1, n):
            L[j, i] = (A[j, i] - np.dot(L[j, :i], U[:i, i])) / U[i, i]
    
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    return x
  