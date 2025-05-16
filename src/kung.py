from typing import List, Tuple

# Regresa True si p1 domina a p2 (en un problema de maximización)
def domina_max(p1: Tuple[float], p2: Tuple[float]) -> bool:
    mejor_o_igual = all(a >= b for a, b in zip(p1, p2))
    estrictamente_mejor = any(a > b for a, b in zip(p1, p2))
    return mejor_o_igual and estrictamente_mejor

# Regresa True si p1 domina a p2 (en un problema de minimización)
def domina_min(p1: Tuple[float], p2: Tuple[float]) -> bool:
    mejor_o_igual = all(a <= b for a, b in zip(p1, p2))
    estrictamente_mejor = any(a < b for a, b in zip(p1, p2))
    return mejor_o_igual and estrictamente_mejor

# Algoritmo de Kung para calcular el conjunto de soluciones no dominadas
def kung_max(P: List[Tuple[float]]) -> List[Tuple[float]]:    
    if len(P) == 1:
        return P[:]

    mid = len(P)//2
    
    T = kung_max(P[:mid]) # Primera mitad: ( P(1: [ |P|/2 ]) )
    B = kung_max(P[mid:]) # Segunda mitad: ( P( [ |P|/2 + 1 ] : |P|) )

    M = T[:]
    for b in B:
        if not any(domina_max(t, b) for t in T):
            M.append(b)
    return M

# Algoritmo de Kung para calcular el conjunto de soluciones no dominadas
def kung_min(P: List[Tuple[float]]) -> List[Tuple[float]]:    
    if len(P) == 1:
        return P[:]

    mid = len(P)//2
    
    T = kung_min(P[:mid]) # Primera mitad: ( P(1: [ |P|/2 ]) )
    B = kung_min(P[mid:]) # Segunda mitad: ( P( [ |P|/2 + 1 ] : |P|) )

    M = T[:]
    for b in B:
        if not any(domina_min(t, b) for t in T):
            M.append(b)
    return M
