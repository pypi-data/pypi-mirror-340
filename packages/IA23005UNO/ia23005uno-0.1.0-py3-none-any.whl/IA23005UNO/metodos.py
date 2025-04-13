"""
IA23005UNO - Librería para resolver sistemas de ecuaciones lineales y no lineales

Esta librería implementa los siguientes métodos:
- Eliminación de Gauss
- Gauss-Jordan
- Crammer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección
"""

import numpy as np

def eliminacion_gauss(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Eliminación Gaussiana.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    n = len(b)
    # Matriz aumentada
    M = np.hstack([A, b.reshape(-1, 1)])
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Eliminación
        for j in range(i+1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    n = len(b)
    M = np.hstack([A, b.reshape(-1, 1)])
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # Normalizar la fila del pivote
        M[i] = M[i] / M[i, i]
        
        # Eliminación en todas las demás filas
        for j in range(n):
            if j != i:
                M[j] -= M[j, i] * M[i]
    
    x = M[:, -1]
    return x

def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la Regla de Cramer.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    detA = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / detA
    
    return x

def descomposicion_lu(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando Descomposición LU.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    n = len(b)
    L = np.eye(n)
    U = A.copy()
    
    # Descomposición LU
    for i in range(n):
        for j in range(i+1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    
    # Sustitución hacia adelante (Ly = b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    return x

def jacobi(A, b, x0=None, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (opcional)
    tol: Tolerancia para la convergencia (opcional)
    max_iter: Número máximo de iteraciones (opcional)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    D = np.diag(A)
    R = A - np.diagflat(D)
    
    for _ in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    
    return x

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (opcional)
    tol: Tolerancia para la convergencia (opcional)
    max_iter: Número máximo de iteraciones (opcional)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    for _ in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    
    return x

def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de una ecuación no lineal usando el método de Bisección.
    
    Parámetros:
    f: Función a la que se le busca la raíz (callable)
    a: Extremo izquierdo del intervalo (float)
    b: Extremo derecho del intervalo (float)
    tol: Tolerancia para la convergencia (opcional)
    max_iter: Número máximo de iteraciones (opcional)
    
    Retorna:
    c: Aproximación de la raíz (float)
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2