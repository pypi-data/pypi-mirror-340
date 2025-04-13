import numpy as np
from scipy.linalg import lu

# Metodo Eliminacion de Gauss
def elimina_Gauss(coeficiente_M, vector_I):
    
    num_Ecuaciones = len(vector_I)
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    
    # eliminación hacia adelante
    for fila_Pivot in range(num_Ecuaciones):
        for fila_Actual in range(fila_Pivot+1, num_Ecuaciones):
            factor = coeficiente_M[fila_Actual, fila_Pivot] / coeficiente_M[fila_Pivot, fila_Pivot]
            coeficiente_M[fila_Actual, fila_Pivot:] -= factor * coeficiente_M[fila_Pivot, fila_Pivot:]
            vector_I[fila_Actual] -= factor * vector_I[fila_Pivot]
    
    # sustitución hacia atrás
    solucion = np.zeros(num_Ecuaciones)
    for fila in range(num_Ecuaciones-1, -1, -1):
        solucion[fila] = (vector_I[fila] - np.dot(coeficiente_M[fila, fila+1:], solucion[fila+1:])) / coeficiente_M[fila, fila]
    return solucion

#Metodo de Gauss-Jordan
def gauss_Jordan(coeficiente_M, vector_I):
    
    num_Ecuaciones = len(vector_I)
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    
    # formar la matriz aumentada
    matriz_Aumentada = np.hstack([coeficiente_M, vector_I.reshape(-1, 1)])
    
    # eliminación de Gauss-Jordan
    for fila_Pivot in range(num_Ecuaciones):
        # normalizar la fila i
        matriz_Aumentada[fila_Pivot] = matriz_Aumentada[fila_Pivot] / matriz_Aumentada[fila_Pivot, fila_Pivot]
        # hacer ceros en las demás filas
        for fila_Actuall in range(num_Ecuaciones):
            if fila_Pivot != fila_Actuall:
                matriz_Aumentada[fila_Actuall] -= matriz_Aumentada[fila_Actuall, fila_Pivot] * matriz_Aumentada[fila_Pivot]
    
    return matriz_Aumentada[:, -1]

#Metodo de Crammer
def crammer(coeficiente_M, vector_I):
    
    num_Ecuaciones = len(vector_I)
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    
    det_Principal = np.linalg.det(coeficiente_M)
    if det_Principal == 0:
        raise ValueError("La matriz A es singular.")
    
    solucion = np.zeros(num_Ecuaciones)
    for indice_Variable in range(num_Ecuaciones):
        matriz_mod = coeficiente_M.copy()
        matriz_mod[:, indice_Variable] = vector_I
        solucion[indice_Variable] = np.linalg.det(matriz_mod) / det_Principal
    return solucion

# Metodo de descomposicion LU
def descomposicion_LU(coeficiente_M, vector_I):
   
   # convierte las entradas a arrays de NumPY con tipo float
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    
    matriz_p, matriz_l, matriz_u = lu(coeficiente_M)
    vector_inter = np.linalg.solve(matriz_l, np.dot(matriz_p, vector_I))
    solucion = np.linalg.solve(matriz_u, vector_inter)
    return solucion

#Metodo de Jacobi
def jacobi(coeficiente_M, vector_I, estimacion_Ini=None, tolerancia=1e-6, max_Iteraciones=100):
    
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    num_Ecuaciones = len(vector_I)
    
    if estimacion_Ini is None:
        estimacion_Ini = np.zeros(num_Ecuaciones)
    
    diagonal_prin = np.diag(coeficiente_M)
    matriz_Fudiagonal = coeficiente_M - np.diagflat(diagonal_prin)
    
    for _ in range(max_Iteraciones):
        estimacion_Nueva = (vector_I - np.dot(matriz_Fudiagonal, estimacion_Ini)) / diagonal_prin
        if np.linalg.norm(estimacion_Nueva - estimacion_Ini) < tolerancia:
            return estimacion_Nueva
        estimacion_Ini = estimacion_Nueva
    
    raise ValueError("El método no converge.")

#Metodo de Gauss-Seidel
def gauss_Seidel(coeficiente_M, vector_I, estimacion_Ini=None, tolerancia=1e-6, max_iteraciones=100):
    
    coeficiente_M = np.array(coeficiente_M, dtype=float)
    vector_I = np.array(vector_I, dtype=float)
    num_Ecuaciones = len(vector_I)
    
    if estimacion_Ini is None:
        estimacion_Ini = np.zeros(num_Ecuaciones)
    
    for _ in range(max_iteraciones):
        estimacion_nueva = np.copy(estimacion_Ini)
        for indice_Variable in range(num_Ecuaciones):
            suma_Infe = np.dot(coeficiente_M[indice_Variable, :indice_Variable], estimacion_nueva[:indice_Variable])
            suma_super = np.dot(coeficiente_M[indice_Variable, indice_Variable+1:], estimacion_Ini[indice_Variable+1:])
            estimacion_nueva[indice_Variable] = (vector_I[indice_Variable] - suma_Infe - suma_super) / coeficiente_M[indice_Variable, indice_Variable]
        if np.linalg.norm(estimacion_nueva - estimacion_Ini) < tolerancia:
            return estimacion_nueva
        estimacion_Ini = estimacion_nueva
    
    raise ValueError("El método no converge.")