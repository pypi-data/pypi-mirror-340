from fractions import Fraction
import numpy as np
#-----------------------------ELIMINACIÓN GAUSSANIANA/GAUSS ELIMINATION-------------------------------------------------------------------
# función auxiliar para imprimir matrices con fracciones de forma visual
def imprimir_matriz(m):
    for fila in m:
        print(" | ".join(f"{elem}" for elem in fila))
    print()

def gauss_elimination(c, it):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b 
    usando el método de eliminación de Gauss (con pivoteo parcial).

    Args:
        c (list[list]): Matriz de coeficientes.
        it (list): Vector de términos independientes.

    Returns:
        list: Soluciones del sistema como objetos Fraction.
    """
    n = len(it)
    m = [[Fraction(c[i][j]) for j in range(n)] + [Fraction(it[i])] for i in range(n)]
    
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m[r][i]))
        if m[max_row][i] == 0:
            return None
        m[i], m[max_row] = m[max_row], m[i]
        for j in range(i + 1, n):
            factor = m[j][i] / m[i][i]
            for k in range(i, n + 1):
                m[j][k] -= factor * m[i][k]
    x = [Fraction(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        suma = Fraction(0)
        for j in range(i + 1, n):
            suma += m[i][j] * x[j]
        x[i] = (m[i][-1] - suma) / m[i][i]
    return x

#-----------------------------GAUSS JORDAN-------------------------------------------------------------------
def gauss_jordan(coefficients, ind_terms):
    """
    Resuelve un sistema de ecuaciones lineales de la forma Ax = b usando el método de Gauss-Jordan.

    Este método transforma la matriz aumentada [A|b] en su forma reducida por filas (forma escalonada reducida),
    y obtiene directamente la solución del sistema.

    Args:
        coefficients (list[list]): Matriz de coeficientes A del sistema.
        ind_terms (list): Vector de términos independientes b.

    Returns:
        list: Solución del sistema como una lista de fracciones [x1, x2, ..., xn],
        o None si el sistema no tiene solución única.
    """
    # convertir a objetos Fraction si es que no lo son
    coefficients = [[Fraction(coef) for coef in row] for row in coefficients]
    ind_terms = [Fraction(term) for term in ind_terms]

    n = len(ind_terms)
    
    #Crear la matriz aumentada
    equations = [coefficients[i] + [ind_terms[i]] for i in range(n)]

    for i in range(n):
        # Si el pivote es 0, intercambiar filas
        if equations[i][i] == 0:
            for k in range(i + 1, n):
                if equations[k][i] != 0:
                    equations[i], equations[k] = equations[k], equations[i]
                    break
            else:
                return None # no se puede resolver si hay una fila llena de ceros

        #normalizar la fila dividiendo por el pivote
        pivote = equations[i][i]
        equations[i] = [elemento / pivote for elemento in equations[i]]

        #hacer ceros en la columna i para todas las demás filas
        for j in range(n):
            if i != j:
                factor = equations[j][i]
                equations[j] = [equations[j][k] - factor * equations[i][k] for k in range(n + 1)]

    #extraer la solución
    return [fila[-1] for fila in equations]

#-----------------------------GAUSS SEIDEL-------------------------------------------------------------------
def gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve un sistema lineal Ax = b usando el método iterativo de Gauss-Seidel.

    Args:
        A (ndarray): Matriz de coeficientes (tipo numpy).
        b (ndarray): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        ndarray: Aproximación de la solución.
    """
    n = len(b) #número de incognitas (o ecuaciones)
    x = np.zeros(n) # vector de soluciones inicializadas en cero

    for k in range(max_iter):
        x_prev = x.copy()

        for i in range(n): 
            #aplica la fórmula de Gauss Seidel
            x[i] = (b[i] - sum(A[i, j] * x[j] for j in range(n) if j != i)) / A[i, i]

        # Verifica si la solución ha convergido (o sea si el cambio es menor a la tolerancia)
        if np.linalg.norm(x - x_prev) < tol:
            print(f"Total de iteraciones necesitadas: {k}")
            return x
    
    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x

#-----------------------------JACOBI-------------------------------------------------------------------
def jacobi(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve un sistema lineal Ax = b usando el método iterativo de Jacobi.

    Args:
        A (ndarray): Matriz de coeficientes (tipo numpy).
        b (ndarray): Vector de términos independientes.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        ndarray: Aproximación de la solución.
    """
    n = len(b) #número de incognitas (o ecuaciones)
    x = np.zeros(n) #inicializa el vector solución con ceros
    x_new = np.zeros(n) # vector temporal para guardar la nueva estimación en cada iteración

    for k in range(max_iter):
        for i in range(n): 
            # aplica la fórmula del metodo de Jacobi
            x_new[i] = (b[i] - sum(A[i, j] * x[j] for j in range(n) if j != i)) / A[i, i]
        # Verificamos si la diferencia entre la solución actual y la anterior es menor que la tolerancia 
        if np.linalg.norm(x_new - x) < tol:
            print(f"Total de iteraciones necesitadas: {k}")
            return x_new #Devuelve la solucion aproximada
        #actualiza x para la siguiente iteración
        x = x_new.copy()

    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x

#-----------------------------CRAMMER-------------------------------------------------------------------
def determinante(matriz):
    """Calcula el determinante de una matriz cuadrada."""
    n = len(matriz)
    if n == 1:
        return matriz[0][0]
    elif n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    det = Fraction(0)
    for col in range(n):
        signo = (-1) ** col
        submatriz = []
        for fila in matriz[1:]:
            submatriz.append(fila[:col] + fila[col+1:])
        det += signo * matriz[0][col] * determinante(submatriz)
    return det

def crammer(matriz_coeficientes, constantes):
    """
    Resuelve un sistema de ecuaciones lineales usando la Regla de Crammer.

    Args:
        matriz_coeficientes (list): Matriz cuadrada de coeficientes.
        constantes (list): Vector de términos independientes.

    Returns:
        list: Soluciones en orden [x1, x2, ..., xn] o None si no hay solución única.
    """
    n = len(matriz_coeficientes)

    # Validar que la matriz sea cuadrada
    if any(len(fila) != n for fila in matriz_coeficientes):
        raise ValueError("La matriz de coeficientes debe ser cuadrada")
    # Validar que las constantes coincidan en tamaño
    if len(constantes) != n:
        raise ValueError("Debe haber el mismo número de constantes que de ecuaciones")

    # Convertir a fracciones
    A = [[Fraction(elem) for elem in fila] for fila in matriz_coeficientes]
    b = [Fraction(num) for num in constantes]

    # Calcular determinante de la matriz de coeficientes
    det_principal = determinante(A)
    if det_principal == 0:
        return None  # No hay solución única

    soluciones = []
    for i in range(n):
        # Crear matriz modificada reemplazando la columna i
        matriz_modificada = [fila.copy() for fila in A]
        for j in range(n):
            matriz_modificada[j][i] = b[j]

        # Calcular determinante de la matriz modificada
        det_modificado = determinante(matriz_modificada)
        soluciones.append(Fraction(det_modificado, det_principal))

    return soluciones


#-----------------------------DESCOMPOSICION LU/LU DECOMPOSITION-------------------------------------------------------------------
def decomposicion_lu(matriz):
    """
    Realiza la descomposición LU de una matriz cuadrada.
    
    Args:
        matriz: Lista de listas que representa una matriz cuadrada.
    
    Returns:
        (L, U): Tupla con las matrices triangular inferior (L) y superior (U).
    
    Raises:
        ValueError: Si la matriz no es cuadrada o si es singular.
    """
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada")
    
    # Inicializar matrices L y U
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        # Calcular U
        for k in range(i, n):
            suma = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matriz[i][k] - suma
        
        # Calcular L
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0  # Diagonal de L es 1
            else:
                if U[i][i] == 0:
                    raise ValueError("Matriz singular, no se puede factorizar")
                suma = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (matriz[k][i] - suma) / U[i][i]
    
    return L, U

def forward_substitution(L, b):
    """
    Resuelve Ly = b usando sustitución hacia adelante.
    
    Args:
        L: Matriz triangular inferior con diagonal 1
        b: Vector de términos independientes
    
    Returns:
        y: Vector solución
    """
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        suma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = b[i] - suma
    return y

def backward_substitution(U, y):
    """
    Resuelve Ux = y usando sustitución hacia atrás.
    
    Args:
        U: Matriz triangular superior
        y: Vector resultado de la sustitución hacia adelante
    
    Returns:
        x: Vector solución
    """
    n = len(U)
    x = [0.0] * n
    for i in reversed(range(n)):
        suma = sum(U[i][j] * x[j] for j in range(i+1, n))
        if U[i][i] == 0:
            raise ValueError("Matriz singular, sistema sin solución única")
        x[i] = (y[i] - suma) / U[i][i]
    return x

def lu_solver(A, b):
    """
    Resuelve un sistema de ecuaciones Ax = b usando descomposición LU.
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
    
    Returns:
        x: Vector solución
    """
    try:
        L, U = decomposicion_lu(A)
    except ValueError as e:
        return None  # Sistema sin solución única
    
    y = forward_substitution(L, b)
    x = backward_substitution(U, y)
    return x




