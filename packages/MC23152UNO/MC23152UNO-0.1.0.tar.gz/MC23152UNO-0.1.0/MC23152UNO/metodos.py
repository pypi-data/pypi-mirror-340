"""
MC23152UNO - Librería de métodos numéricos para resolver sistemas de ecuaciones lineales y no lineales

Metodos implementados:
- Eliminación de Gauss
- Gauss-Jordan
- Crammer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección
"""

import numpy as np

def validacionParam(A, b):
    if A is None or b is None:
        raise ValueError("La matriz A o el vector b no pueden ser None.")
    if A.size == 0 or b.size == 0:
        raise ValueError("La matriz A o el vector b no pueden estar vacíos.")
    if A.shape[0] != b.shape[0]:
        raise ValueError("El número de filas de A debe ser igual al tamaño de b.")

def eliminacion_gauss(A, b):
    """
    ELIMINACION GAUSS
                    
    Resuelve un sistema de ecuaciones lineales usando Eliminación Gaussiana.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    
    n = len(b)
    
    # Matriz aumentada
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # ELIMINACION HACIA ARRIBA
    for i in range(n):
        # Pivoteo 
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        # ELIMINACION
        for j in range(i+1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
    
    # SUSTITUCION HACIA ATRAS
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:])) / M[i, i]
    
    # DEVOLVEMOS CALCULO
    return x

def gauss_jordan(A, b):
    """
    GAUSS-JORDAN
    
    Resuelve un sistema de ecuaciones lineales usando Gauss-Jordan.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    for i in range(n):
        # PRIVOTE
        max_row = np.argmax(np.abs(M[i:, i])) + i
        M[[i, max_row]] = M[[max_row, i]]
        
        M[i] = M[i] / M[i, i]
        
        # ELIMINACION
        for j in range(n):
            if j != i:
                M[j] -= M[j, i] * M[i]
    
    # DEVOLVEMOS CALCULO
    return M[:, -1]

def cramer(A, b):
    """
    CRAMER
    
    Resuelve un sistema de ecuaciones lineales usando la Regla de Cramer.
    
    Parámetros NECESARIOS:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    det_A = np.linalg.det(A)
    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / det_A
    
    # DEVOLVEMOS CALCULO
    return x

def descomposicion_lu(A, b):
    """
    DESCOMPOSICION LU
    
    Resuelve un sistema de ecuaciones lineales usando Descomposición LU.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x: Vector solución (numpy array)
    """
    
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    n = len(b)
    L = np.eye(n)
    U = A.astype(float)
    
    for i in range(n):
        for j in range(i+1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    
    # SUSTICION HACIA ADELANTE
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
    
    # SUSTITUCION HACIA ATRAS
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
    
    # DEVOLVEMOS CALCULO
    return x


def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    JACOBI
    
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    X0, tol y max_iter son opcionales
    
    x0: Vector inicial 
    tol: Tolerancia 
    max_iter: Máximo número de iteraciones
    
    Retorna:
    x: Vector solución (numpy array)
    """
    
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    
    n = len(b)
    if x0 is None:
        x0 = np.zeros(n)
    x = x0.copy()
    
    D = np.diag(np.diag(A))
    R = A - D
    D_inv = np.diag(1 / np.diag(D))
    
    for _ in range(max_iter):
        x_new = D_inv @ (b - R @ x)
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    
    # DEVOLVEMOS CALCULO
    return x

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Seidel.
    
    Parámetros:
    A: Matriz de coeficientes (numpy array)*
    b: Vector de términos independientes (numpy array)*
    
    VALORES OPCIONALES
    
    x0: Vector inicial
    tol: Tolerancia
    max_iter: Máximo número de iteraciones
    
    Retorna:
    x: Vector solución (numpy array)
    """
    
    # validacion de que no entre datos vacios
    validacionParam(A, b)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
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
            return x_new
        x = x_new
    
    # DEVOLVEMOS CALCULO
    return x

def validar_parametros_biseccion(f, a, b, max_iter):
    if not callable(f):
        raise ValueError("El parámetro f debe ser una función.")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Los límites a y b deben ser números reales.")
    if a >= b:
        raise ValueError("El límite inferior 'a' debe ser menor que el superior 'b'.")
    if not isinstance(max_iter, int) or max_iter <= 0:
        raise ValueError("El número máximo de iteraciones debe ser un entero positivo.")
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe cambiar de signo en el intervalo [a, b]")
    
def biseccion(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raíz de una ecuación no lineal usando el método de bisección.
    
    Parámetros:
    f: Función a evaluar (callable)
    a: Límite inferior del intervalo (float)
    b: Límite superior del intervalo (float)
    tol: Tolerancia (opcional)
    max_iter: Máximo número de iteraciones (opcional)
    
    Retorna:
    c: Aproximación de la raíz (float)
    """
    
    # VALIDAMOS INFORMACION DE ENTRADA
    validar_parametros_biseccion(f, a, b, max_iter)
    
    # SI TODO VA BIEN, PROCEDEMOS A HACER EL CALCULO
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    
    # DEVOLVEMOS CALCULO
    return (a + b) / 2