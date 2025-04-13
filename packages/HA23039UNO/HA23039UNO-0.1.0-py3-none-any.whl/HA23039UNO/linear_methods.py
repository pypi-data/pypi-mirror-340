"""
Módulo que implementa métodos para resolver sistemas de ecuaciones lineales.
"""

def gauss_elimination(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de eliminación de Gauss.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
    
    Returns:
        list: Vector solución del sistema.
    
    Raises:
        ValueError: Si el sistema no tiene solución única.
    """
    n = len(b)
    # Crear copias para no modificar los originales
    matrix = [row[:] for row in A]
    vector = b[:]
    
    # Crear la matriz aumentada [A|b]
    augmented = [matrix[i] + [vector[i]] for i in range(n)]
    
    # Eliminación hacia adelante
    for i in range(n):
        # Buscar pivote no nulo
        if augmented[i][i] == 0:
            for k in range(i + 1, n):
                if augmented[k][i] != 0:
                    augmented[i], augmented[k] = augmented[k], augmented[i]
                    break
            else:
                raise ValueError("El sistema no tiene solución única")
        
        # Eliminar elementos debajo del pivote
        for j in range(i + 1, n):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(i, n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    
    # Sustitución hacia atrás
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]
    
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
    
    Returns:
        list: Vector solución del sistema.
    
    Raises:
        ValueError: Si el sistema no tiene solución única.
    """
    n = len(b)
    # Crear copias para no modificar los originales
    matrix = [row[:] for row in A]
    vector = b[:]
    
    # Crear la matriz aumentada [A|b]
    augmented = [matrix[i] + [vector[i]] for i in range(n)]
    
    # Eliminación hacia adelante
    for i in range(n):
        # Buscar pivote no nulo
        if augmented[i][i] == 0:
            for k in range(i + 1, n):
                if augmented[k][i] != 0:
                    augmented[i], augmented[k] = augmented[k], augmented[i]
                    break
            else:
                raise ValueError("El sistema no tiene solución única")
        
        # Normalizar la fila del pivote
        divisor = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= divisor
        
        # Eliminar elementos en la columna i para todas las filas
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(i, n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    
    # La solución está en la última columna
    return [row[n] for row in augmented]

def determinant(A):
    """
    Calcula el determinante de una matriz usando la expansión por cofactores.
    
    Args:
        A (list): Matriz cuadrada (lista de listas).
    
    Returns:
        float: Determinante de la matriz.
    """
    n = len(A)
    
    # Caso base: matriz 1x1
    if n == 1:
        return A[0][0]
    
    # Caso base: matriz 2x2
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    # Expansión por cofactores en la primera fila
    det = 0
    for j in range(n):
        # Crear la submatriz eliminando la primera fila y la columna j
        submatrix = []
        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(A[i][k])
            submatrix.append(row)
        
        # Sumar el cofactor
        sign = (-1) ** j
        det += sign * A[0][j] * determinant(submatrix)
    
    return det

def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
    
    Returns:
        list: Vector solución del sistema.
    
    Raises:
        ValueError: Si el determinante de A es cero.
    """
    n = len(b)
    
    # Calcular el determinante de A
    det_A = determinant(A)
    
    if abs(det_A) < 1e-10:
        raise ValueError("El determinante de la matriz A es cero, no se puede aplicar Cramer")
    
    # Calcular la solución
    x = []
    for i in range(n):
        # Crear la matriz A_i reemplazando la columna i con el vector b
        A_i = []
        for j in range(n):
            row = []
            for k in range(n):
                if k == i:
                    row.append(b[j])
                else:
                    row.append(A[j][k])
            A_i.append(row)
        
        # Calcular x_i
        det_A_i = determinant(A_i)
        x.append(det_A_i / det_A)
    
    return x

def lu_decomposition(A, b):
    """
    Resuelve un sistema de ecuaciones lineales utilizando la descomposición LU.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
    
    Returns:
        list: Vector solución del sistema.
    
    Raises:
        ValueError: Si la matriz no puede descomponerse.
    """
    n = len(A)
    
    # Inicializar matrices L y U
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    # Descomposición LU (Algoritmo de Doolittle)
    for i in range(n):
        # Diagonal de L es 1
        L[i][i] = 1.0
        
        # Elementos de U en la fila i
        for j in range(i, n):
            sum_Lu = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - sum_Lu
        
        # Elementos de L en la columna i
        for j in range(i + 1, n):
            sum_Lu = sum(L[j][k] * U[k][i] for k in range(i))
            if abs(U[i][i]) < 1e-10:
                raise ValueError("La matriz no puede descomponerse en LU")
            L[j][i] = (A[j][i] - sum_Lu) / U[i][i]
    
    # Resolver Ly = b (sustitución hacia adelante)
    y = [0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    
    # Resolver Ux = y (sustitución hacia atrás)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    
    return x

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Jacobi.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
        x0 (list, optional): Vector inicial. Si es None, se inicia con ceros.
        tol (float, optional): Tolerancia para la convergencia. Por defecto 1e-6.
        max_iter (int, optional): Número máximo de iteraciones. Por defecto 100.
    
    Returns:
        tuple: (Vector solución, Número de iteraciones realizadas)
    
    Raises:
        ValueError: Si el método no converge.
    """
    n = len(b)
    
    # Inicializar vector x
    if x0 is None:
        x = [0] * n
    else:
        x = x0.copy()
    
    # Iterar hasta convergencia o hasta alcanzar max_iter
    for iter_count in range(max_iter):
        x_new = [0] * n
        
        # Calcular x_new usando los valores de la iteración anterior
        for i in range(n):
            sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_ax) / A[i][i]
        
        # Verificar convergencia
        if all(abs(x_new[i] - x[i]) < tol for i in range(n)):
            return x_new, iter_count + 1
        
        x = x_new.copy()
    
    raise ValueError(f"El método de Jacobi no convergió después de {max_iter} iteraciones")

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Gauss-Seidel.
    
    Args:
        A (list): Matriz de coeficientes (lista de listas).
        b (list): Vector de términos independientes.
        x0 (list, optional): Vector inicial. Si es None, se inicia con ceros.
        tol (float, optional): Tolerancia para la convergencia. Por defecto 1e-6.
        max_iter (int, optional): Número máximo de iteraciones. Por defecto 100.
    
    Returns:
        tuple: (Vector solución, Número de iteraciones realizadas)
    
    Raises:
        ValueError: Si el método no converge.
    """
    n = len(b)
    
    # Inicializar vector x
    if x0 is None:
        x = [0] * n
    else:
        x = x0.copy()
    
    # Iterar hasta convergencia o hasta alcanzar max_iter
    for iter_count in range(max_iter):
        x_old = x.copy()
        
        # Calcular nuevos valores usando los valores ya actualizados
        for i in range(n):
            # Suma para j < i (usando valores actualizados)
            sum1 = sum(A[i][j] * x[j] for j in range(i))
            # Suma para j > i (usando valores de la iteración anterior)
            sum2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            
            x[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        # Verificar convergencia
        if all(abs(x[i] - x_old[i]) < tol for i in range(n)):
            return x, iter_count + 1
    
    raise ValueError(f"El método de Gauss-Seidel no convergió después de {max_iter} iteraciones")