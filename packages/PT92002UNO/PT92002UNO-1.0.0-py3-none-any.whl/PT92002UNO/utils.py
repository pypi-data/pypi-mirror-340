"""
utils.py - Módulo de utilidades para la librería PT92002UNO

Este módulo contiene funciones auxiliares para:
- Validación de matrices y vectores
- Cálculo de normas vectoriales y matriciales
- Generación de matrices especiales
- Otras utilidades numéricas

Autor: [Frany Esmeralda Peña Tobar]     
Carnet: PT92002
"""

import numpy as np
from typing import Tuple, Callable

def validar_sistema(A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Valida y prepara un sistema de ecuaciones para su procesamiento.
    
    Parámetros:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        
    Retorna:
        Tuple[np.ndarray, np.ndarray]: Matriz y vector validados
        
    Excepciones:
        ValueError: Si las dimensiones no son compatibles o la matriz no es cuadrada
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    if A.ndim != 2:
        raise ValueError("La matriz A debe ser bidimensional")
    
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada")
    
    if b.ndim != 1:
        b = b.flatten()
    
    if A.shape[0] != b.shape[0]:
        raise ValueError("Las dimensiones de A y b no coinciden")
    
    return A, b

def es_diagonal_dominante(A: np.ndarray) -> bool:
    """
    Determina si una matriz es diagonal dominante.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        bool: True si la matriz es diagonal dominante, False en caso contrario
    """
    diagonal = np.diag(np.abs(A))
    suma_filas = np.sum(np.abs(A), axis=1) - diagonal
    return np.all(diagonal > suma_filas)

def norma_vectorial(x: np.ndarray, p: int = 2) -> float:
    """
    Calcula la norma p de un vector.
    
    Parámetros:
        x: Vector de entrada
        p: Orden de la norma (1, 2, etc.)
        
    Retorna:
        float: Valor de la norma
        
    Ejemplo:
        >>> x = np.array([3, 4])
        >>> norma_vectorial(x, 2)
        5.0
    """
    return np.linalg.norm(x, ord=p)

def norma_matricial(A: np.ndarray, p: int = 2) -> float:
    """
    Calcula la norma p de una matriz.
    
    Parámetros:
        A: Matriz de entrada
        p: Orden de la norma (1, 2, np.inf, 'fro' para Frobenius)
        
    Retorna:
        float: Valor de la norma
    """
    return np.linalg.norm(A, ord=p)

def matriz_aumentada(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Crea la matriz aumentada [A|b] para un sistema de ecuaciones.
    
    Parámetros:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        
    Retorna:
        np.ndarray: Matriz aumentada
    """
    return np.hstack([A, b.reshape(-1, 1)])

def pivoteo_parcial(M: np.ndarray, i: int) -> np.ndarray:
    """
    Realiza pivoteo parcial en una matriz a partir de la fila i.
    
    Parámetros:
        M: Matriz a pivotear
        i: Índice de la fila actual
        
    Retorna:
        np.ndarray: Matriz pivotada
    """
    n = M.shape[0]
    max_row = np.argmax(np.abs(M[i:, i])) + i
    if max_row != i:
        M[[i, max_row]] = M[[max_row, i]]
    return M

def es_tolerancia_alcanzada(x_actual: np.ndarray, x_anterior: np.ndarray, 
                          tol: float = 1e-6, norma: int = 2) -> bool:
    """
    Determina si se ha alcanzado la tolerancia en métodos iterativos.
    
    Parámetros:
        x_actual: Vector actual
        x_anterior: Vector de la iteración anterior
        tol: Tolerancia permitida
        norma: Tipo de norma a utilizar
        
    Retorna:
        bool: True si se alcanzó la tolerancia, False en caso contrario
    """
    return norma_vectorial(x_actual - x_anterior, norma) < tol

def verificar_intervalo_raiz(f: Callable, a: float, b: float) -> bool:
    """
    Verifica si un intervalo [a, b] contiene una raíz (f(a)*f(b) < 0).
    
    Parámetros:
        f: Función a evaluar
        a: Extremo izquierdo del intervalo
        b: Extremo derecho del intervalo
        
    Retorna:
        bool: True si el intervalo contiene una raíz, False en caso contrario
        
    Excepciones:
        ValueError: Si a >= b
    """
    if a >= b:
        raise ValueError("El extremo izquierdo 'a' debe ser menor que el derecho 'b'")
    return f(a) * f(b) < 0

def crear_matriz_diagonal(A: np.ndarray) -> np.ndarray:
    """
    Crea una matriz diagonal a partir de los elementos diagonales de A.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        np.ndarray: Matriz diagonal
    """
    return np.diag(np.diag(A))

def crear_matriz_resto(A: np.ndarray) -> np.ndarray:
    """
    Crea una matriz con los elementos no diagonales de A.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        np.ndarray: Matriz con ceros en la diagonal y el resto de A
    """
    return A - crear_matriz_diagonal(A)

def condicion_matriz(A: np.ndarray) -> float:
    """
    Calcula el número de condición de una matriz.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        float: Número de condición de la matriz
    """
    return np.linalg.cond(A)

def es_matriz_simetrica(A: np.ndarray) -> bool:
    """
    Determina si una matriz es simétrica.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        bool: True si la matriz es simétrica, False en caso contrario
    """
    return np.allclose(A, A.T)

def es_matriz_definida_positiva(A: np.ndarray) -> bool:
    """
    Determina si una matriz es definida positiva.
    
    Parámetros:
        A: Matriz de entrada
        
    Retorna:
        bool: True si la matriz es definida positiva, False en caso contrario
    """
    if not es_matriz_simetrica(A):
        return False
    return np.all(np.linalg.eigvals(A) > 0)  