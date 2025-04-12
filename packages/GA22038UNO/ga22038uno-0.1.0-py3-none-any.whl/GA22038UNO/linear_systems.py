import numpy as np

def gauss_elimination(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de eliminación de Gauss.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    """
    n = len(b)
    # Crear matriz aumentada
    Ab = np.column_stack((A, b))
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
            
        for j in range(i+1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (Ab[i, -1] - np.sum(Ab[i, i+1:n] * x[i+1:])) / Ab[i, i]
        
    return x

def gauss_jordan(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    """
    n = len(b)
    # Crear matriz aumentada
    Ab = np.column_stack((A, b))
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Normalizar la fila i
        Ab[i] = Ab[i] / Ab[i, i]
        
        # Eliminación
        for j in range(n):
            if j != i:
                Ab[j] = Ab[j] - Ab[j, i] * Ab[i]
    
    # Extraer solución
    x = Ab[:, -1]
    return x

def cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la regla de Cramer.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    """
    n = len(b)
    det_A = np.linalg.det(A)
    
    if np.isclose(det_A, 0):
        raise ValueError("El determinante de la matriz A es cero, no se puede aplicar el método de Cramer")
    
    x = np.zeros(n)
    for i in range(n):
        # Crear matriz Ai sustituyendo la columna i por el vector b
        Ai = A.copy()
        Ai[:, i] = b
        # Calcular xi = det(Ai) / det(A)
        x[i] = np.linalg.det(Ai) / det_A
        
    return x

def lu_decomposition(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando la descomposición LU.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    """
    n = len(b)
    
    # Inicializar matrices L y U
    L = np.zeros((n, n))
    U = np.zeros((n, n))
    
    # Descomposición LU
    for i in range(n):
        # Elementos de U
        for j in range(i, n):
            U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
        
        # Elementos de L
        L[i, i] = 1  # Diagonal de L siempre es 1
        for j in range(i + 1, n):
            L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]
    
    # Resolver Ly = b (sustitución hacia adelante)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(L[i, j] * y[j] for j in range(i))
    
    # Resolver Ux = y (sustitución hacia atrás)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i+1, n))) / U[i, i]
    
    return x

def jacobi(A, b, x0=None, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Jacobi.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
    x0 : numpy.ndarray, optional
        Vector inicial de aproximación
    tol : float, optional
        Tolerancia para el criterio de convergencia
    max_iter : int, optional
        Número máximo de iteraciones
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    int
        Número de iteraciones realizadas
    """
    n = len(b)
    
    # Verificar si la matriz es diagonalmente dominante
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            print("Advertencia: La matriz no es diagonalmente dominante, el método puede no converger.")
            break
    
    # Inicializar solución
    if x0 is None:
        x0 = np.zeros(n)
    
    x = x0.copy()
    x_new = x.copy()
    
    # Iteraciones
    for k in range(max_iter):
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        
        # Verificar convergencia
        if np.linalg.norm(x_new - x) < tol:
            return x_new, k+1
        
        # Actualizar x para la siguiente iteración
        x = x_new.copy()
    
    print(f"Advertencia: Alcanzado el número máximo de iteraciones ({max_iter}) sin convergencia.")
    return x, max_iter

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100):
    """
    Resuelve un sistema de ecuaciones lineales usando el método iterativo de Gauss-Seidel.
    
    Parameters:
    ----------
    A : numpy.ndarray
        Matriz de coeficientes del sistema
    b : numpy.ndarray
        Vector de términos independientes
    x0 : numpy.ndarray, optional
        Vector inicial de aproximación
    tol : float, optional
        Tolerancia para el criterio de convergencia
    max_iter : int, optional
        Número máximo de iteraciones
        
    Returns:
    -------
    numpy.ndarray
        Solución del sistema
    int
        Número de iteraciones realizadas
    """
    n = len(b)
    
    # Verificar si la matriz es diagonalmente dominante
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            print("Advertencia: La matriz no es diagonalmente dominante, el método puede no converger.")
            break
    
    # Inicializar solución
    if x0 is None:
        x0 = np.zeros(n)
    
    x = x0.copy()
    
    # Iteraciones
    for k in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            # Suma con los valores actualizados
            s1 = sum(A[i, j] * x[j] for j in range(i))
            # Suma con los valores antiguos
            s2 = sum(A[i, j] * x_old[j] for j in range(i+1, n))
            
            x[i] = (b[i] - s1 - s2) / A[i, i]
        
        # Verificar convergencia
        if np.linalg.norm(x - x_old) < tol:
            return x, k+1
    
    print(f"Advertencia: Alcanzado el número máximo de iteraciones ({max_iter}) sin convergencia.")
    return x, max_iter