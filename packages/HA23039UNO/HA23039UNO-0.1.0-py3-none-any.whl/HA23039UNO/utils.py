"""
Funciones auxiliares para la librería.
"""

def is_diagonally_dominant(A):
    """
    Verifica si una matriz es diagonalmente dominante.
    
    Args:
        A (list): Matriz cuadrada (lista de listas).
    
    Returns:
        bool: True si la matriz es diagonalmente dominante, False en caso contrario.
    """
    n = len(A)
    for i in range(n):
        diagonal = abs(A[i][i])
        sum_row = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diagonal <= sum_row:
            return False
    return True

def absolute_error(real_value, approximate_value):
    """
    Calcula el error absoluto entre un valor real y un valor aproximado.
    
    Args:
        real_value (float): Valor real.
        approximate_value (float): Valor aproximado.
    
    Returns:
        float: Error absoluto.
    """
    return abs(real_value - approximate_value)

def relative_error(real_value, approximate_value):
    """
    Calcula el error relativo entre un valor real y un valor aproximado.
    
    Args:
        real_value (float): Valor real.
        approximate_value (float): Valor aproximado.
    
    Returns:
        float: Error relativo, o None si real_value es cero.
    """
    if real_value == 0:
        return None
    return absolute_error(real_value, approximate_value) / abs(real_value)