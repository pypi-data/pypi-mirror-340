from .fraccion import Fraccion
import numpy as np

def gauss_jordan(coefficients, ind_terms):
    """
    Resuelve un sistema de ecuaciones lineales Ax = ind_terms usando el método de Gauss-Jordan
    con la clase personalizada Fraccion.

    Parámetros:
        coefficients (list[list[float|int]]): Matriz de coeficientes A.
        ind_terms (list[float|int]): Términos independientes b.

    Retorna:
        list[Fraccion]: solucin del sistema como lista de objetos Fraccion
                        o None si el sistema no tiene una solución única.
    """
    n = len(ind_terms)
    equations = [[Fraccion(coefficients[i][j]) for j in range(n)] + [Fraccion(ind_terms[i])] for i in range(n)]
    
    for i in range(n):
        if equations[i][i].n == 0:
            for k in range(i + 1, n):
                if equations[k][i].n != 0:
                    equations[i], equations[k] = equations[k], equations[i]
                    break
            else:
                return None  # No se puede resolver

        divisor = equations[i][i]
        equations[i] = [x / divisor for x in equations[i]]
        
        for j in range(n):
            if i != j:
                factor = equations[j][i]
                equations[j] = [equations[j][k] - factor * equations[i][k] for k in range(n + 1)]
    
    return [row[-1] for row in equations]


# Ejemplo de uso:
if __name__ == "__main__":
    # Resolver el sistema:
    # 4x - 2y = 8
    # -2x + y = -3
    coefficients = [[4, 2], [-2, 1]]
    ind_terms = [8, -3]

    solution = gauss_jordan(coefficients, ind_terms)
    print("Solución con Gauss-Jordan:")
    print(solution)

    #MÉTODO PARA RESOLVER POR JACOBI

def jacobi(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Jacobi.

    Parámetros:
    - A (numpy.ndarray): Matriz de coeficientes (debe ser cuadrada y diagonalmente dominante).
    - b (numpy.ndarray): Vector de términos independientes.
    - tol (float): Tolerancia para determinar la convergencia (default: 1e-10).
    - max_iter (int): Número máximo de iteraciones permitidas (default: 1000).

    Retorna:
    - numpy.ndarray: Vector solución aproximado del sistema.

    Imprime:
    - El número de iteraciones necesarias para converger, o un mensaje indicando que no se logró

    Ejemplo:
        A = np.array([[3, -0.1, -0.2],
                        [0.1, 7, -0.3],
                        [0.3, -0.2, 10]], dtype=float)

        b = np.array([7.85, -19.3, 71.4], dtype=float)

        solucion = jacobi(A, b)
        print(solucion)
    """
    n = len(b)
    x = np.zeros(n)
    x_new = np.zeros(n)

    for k in range(max_iter):
        for i in range(n):
            x_new[i] = (b[i] - sum(A[i, j] * x[j] for j in range(n) if j != i)) / A[i, i]

        if np.linalg.norm(x_new - x) < tol:
            print(f"Total de iteraciones necesitadas: {k}")
            return x_new

        x = x_new.copy()

    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x


# Ejemplo de uso:
if __name__ == "__main__":
    A = np.array([[3, -0.1, -0.2],
                    [0.1, 7, -0.3],
                    [0.3, -0.2, 10]], dtype=float)
    b = np.array([7.85, -19.3, 71.4], dtype=float)

    solucion = jacobi(A, b)
    print(f"Solución por Jacobi: {solucion}")

    #RESOLVER POR GAUSS SEIDEL:

def gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método iterativo de Gauss-Seidel.

    Parámetros:
    - A (numpy.ndarray): Matriz de coeficientes (debe ser cuadrada y preferiblemente diagonalmente dominante).
    - b (numpy.ndarray): Vector de términos independientes.
    - tol (float): Tolerancia para determinar la convergencia (default: 1e-10).
    - max_iter (int): Número máximo de iteraciones permitidas (default: 1000).

    Retorna:
    - numpy.ndarray: Vector solución aproximado del sistema.

    Imprime:
    - El número de iteraciones necesarias para converger, o un mensaje indicando que no se logró.

    Ejemplo:
        A = np.array([[4, 1, 2],
                        [3, 5, 1],
                        [1, 1, 3]], dtype=float)

        b = np.array([4,7,3], dtype=float)

        solucion = gauss_seidel(A, b)
        print(solucion)
    """
    n = len(b)
    x = np.zeros(n)

    for k in range(max_iter):
        x_old = np.copy(x)

        for i in range(n):
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i, i]

        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            print(f"Total de iteraciones necesitadas: {k+1}")
            return x

    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x


# Ejemplo de uso:
if __name__ == "__main__":
    A = np.array([[4, 1, 2],
                    [3, 5, 1],
                    [1, 1, 3]], dtype=float)
    b = np.array([4, 7, 3], dtype=float)

    solucion = gauss_seidel(A, b)
    print(f"Solución por Gauss-Seidel: {solucion}")

    #gauss normal:

def gauss_elimination(coefficients, ind_terms):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b utilizando el método de eliminación de Gauss
    con aritmética exacta mediante la clase personalizada Fraccion.

    Parámetros:
    - coefficients (list[list[float]]): Matriz de coeficientes A.
    - ind_terms (list[float]): Vector de términos independientes b.

    Retorna:
    - list[Fraccion]: Solución del sistema como una lista de fracciones, o None si no tiene solución única.

    Ejemplo:
        c = [[2, 6, 1], [1, 2, -1], [5, 7, -4]]
        d = [7, -1, 9]
        solucion = gauss_elimination(c, d)
        print(solucion)
    """
    n = len(ind_terms)
    m = [[Fraccion(coefficients[i][j]) for j in range(n)] + [Fraccion(ind_terms[i])] for i in range(n)]
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m[r][i].n / m[r][i].d))
        if m[max_row][i].n == 0:
            return None  # No hay solución única
        m[i], m[max_row] = m[max_row], m[i]
        for j in range(i + 1, n):
            factor = m[j][i] / m[i][i]
            for k in range(i, n + 1):
                m[j][k] -= factor * m[i][k]
    
    x = [Fraccion(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        suma = Fraccion(0)
        for j in range(i + 1, n):
            suma += m[i][j] * x[j]
        x[i] = (m[i][-1] - suma) / m[i][i]

    return x

# Ejemplo de uso:
if __name__ == "__main__":
    c = [[2, 6, 1], [1, 2, -1], [5, 7, -4]]
    d = [7, -1, 9]
    solucion = gauss_elimination(c, d)
    if solucion is not None:
        print("Solución por Gauss:", solucion)
    else:
        print("El sistema no tiene solución única.")

    #RESOLVER POR BISECCION:

import math

def biseccion(f, a, b, tol=0.01, max_iter=1000):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.

    Parámetros:
        f (function): Función continua f(x) tal que f(a)*f(b) < 0.
        a (float): Límite inferior del intervalo.
        b (float): Límite superior del intervalo.
        tol (float, opcional): Tolerancia del error (default=0.01).
        max_iter (int, opcional): Número máximo de iteraciones (default=1000).

    Retorna:
        tuple:
            - float: Raíz aproximada de la función.
            - int: Número de iteraciones realizadas.

    Ejemplo:
        funcion = lambda x: x**4 + 3*x**3 - 2
        raiz, iteraciones = biseccion(funcion, 0, 1)
        print(f"Raíz encontrada: {raiz}, en {iteraciones} iteraciones.")
    """
    if f(a) * f(b) >= 0:
        raise ValueError("Error, la función no cambia de signo en el intervalo [a, b]")

    iteraciones = 0
    while (b - a) / 2 > tol and iteraciones < max_iter:
        c = (a + b) / 2
        if f(c) == 0:
            return c, iteraciones
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteraciones += 1

    return (a + b) / 2, iteraciones

# Ejemplo de uso
if __name__ == "__main__":
    funcion = lambda x: x**4 + 3*x**3 - 2
    raiz, iteraciones = biseccion(funcion, 0, 1)
    print(f"Raíz de la función por bisección: {raiz:.6f}, encontrada en {iteraciones} iteraciones.")


# LU

def lu_decomposition(A):
    """
    Descomposición LU con pivoteo parcial.
    
    Args:
        A: Matriz cuadrada del sistema (n x n)
    
    Returns:
        P: Matriz de permutación
        L: Matriz triangular inferior
        U: Matriz triangular superior
    
    Raises:
        ValueError: Si la matriz no es cuadrada o el sistema es singular
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada")
        
    L = np.eye(n)
    U = A.copy()
    P = np.eye(n)
    
    for i in range(n-1):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(U[i:, i])) + i
        if max_row != i:
            U[[i, max_row], :] = U[[max_row, i], :]
            P[[i, max_row], :] = P[[max_row, i], :]
            if i > 0:
                L[[i, max_row], :i] = L[[max_row, i], :i]
                
        if np.isclose(U[i, i], 0):
            raise ValueError("Matriz singular, no se puede factorizar")
            
        # Eliminación gaussiana
        for j in range(i+1, n):
            L[j, i] = U[j, i] / U[i, i]
            U[j, i:] -= L[j, i] * U[i, i:]
    
    return P, L, U

def resolver_lu(A, b):
    """
    Resuelve un sistema Ax = b usando descomposición LU con pivoteo.
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
    
    Returns:
        x: Vector solución
    """
    P, L, U = lu_decomposition(A)
    b = np.array(b, dtype=float)
    Pb = P @ b
    
    # Sustitución hacia adelante (Ly = Pb)
    y = np.zeros_like(b)
    for i in range(len(b)):
        y[i] = Pb[i] - L[i, :i] @ y[:i]
    
    # Sustitución hacia atrás (Ux = y)
    x = np.zeros_like(b)
    for i in reversed(range(len(b))):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]
    
    return x

if __name__ == "__main__":
    A = [[2, 3, 1], [4, 7, 3], [6, 18, 5]]  # <-- Definir A y b aquí
    b = [1, 2, 3]
    solucion = resolver_lu(A, b)
    print("Solución con descomposición LU:", solucion)

# RESOLVER POR CRAMMER
def cramer(A, b, tol=1e-10):
    """
    Resuelve un sistema Ax = b usando la regla de Cramer.
    
    Args:
        A: Matriz de coeficientes cuadrada
        b: Vector de términos independientes
        tol: Tolerancia para detectar singularidad
    
    Returns:
        x: Lista con las soluciones
    
    Raises:
        ValueError: Si la matriz es singular o las dimensiones no coinciden
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada")
    if A.shape[0] != b.shape[0]:
        raise ValueError("Dimensiones incompatibles entre A y b")
        
    det_A = np.linalg.det(A)
    
    if abs(det_A) < tol:
        raise ValueError("El sistema no tiene solución única (det(A) ≈ 0)")
    
    n = len(b)
    x = []
    
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        det_Ai = np.linalg.det(Ai)
        x.append(det_Ai / det_A)
    
    return x

A = [[2, -1, 3],
    [1, 0, 2],
    [3, 1, 4]]

b = [5, 3, 10]

if __name__ == "__main__":
    A = [[2, -1, 3], [1, 0, 2], [3, 1, 4]]
    b = [5, 3, 10]
    solucion = cramer(A, b)
    print("Solución por Cramer:", solucion)

