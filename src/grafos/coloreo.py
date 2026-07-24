"""Coloreo de grafos.

Se usa un algoritmo voraz sencillo: se recorren los nodos en un orden
determinista y se asigna el menor color disponible que no este en conflicto
con los vecinos.
"""

from __future__ import annotations

from typing import Any, Dict, List


Grafo = Dict[str, Dict[str, float]]


def _validar_grafo_no_dirigido(grafo: Grafo) -> None:
    """Valida que el grafo sea no dirigido y no vacio."""
    if not grafo:
        raise ValueError("El grafo no puede estar vacio.")

    for nodo, vecinos in grafo.items():
        if not isinstance(vecinos, dict):
            raise TypeError("Los vecinos de %s deben estar en un diccionario." % nodo)
        for vecino, peso in vecinos.items():
            if peso < 0:
                raise ValueError("La arista %s -> %s tiene peso negativo." % (nodo, vecino))
            if vecino not in grafo:
                raise KeyError("El vecino %r no existe como nodo del grafo." % vecino)
            if nodo not in grafo[vecino]:
                raise ValueError("El grafo debe ser no dirigido: falta %s -> %s." % (vecino, nodo))


def colorear_grafo(grafo: Grafo) -> Dict[str, int]:
    """Colorea un grafo usando la estrategia voraz."""
    _validar_grafo_no_dirigido(grafo)

    coloreado: Dict[str, int] = {}
    for nodo in sorted(grafo):
        colores_vecinos = {coloreado[vecino] for vecino in grafo[nodo] if vecino in coloreado}
        color = 1
        while color in colores_vecinos:
            color += 1
        coloreado[nodo] = color

    return coloreado


def numero_cromatico_aproximado(grafo: Grafo) -> int:
    """Devuelve el mayor color usado por el algoritmo voraz."""
    colores = colorear_grafo(grafo)
    return max(colores.values())


def verificar_coloreo(grafo: Grafo, colores: Dict[str, int]) -> bool:
    """Comprueba que el coloreo sea valido."""
    _validar_grafo_no_dirigido(grafo)
    for nodo, vecinos in grafo.items():
        if nodo not in colores:
            return False
        for vecino in vecinos:
            if colores[nodo] == colores.get(vecino):
                return False
    return True


def resumen_coloreo(grafo: Grafo) -> Dict[str, Any]:
    """Devuelve un resumen util para mostrar en consola."""
    colores = colorear_grafo(grafo)
    vertices_por_color: Dict[int, List[str]] = {}
    for vertice, color in colores.items():
        vertices_por_color.setdefault(color, []).append(vertice)

    for vertice_list in vertices_por_color.values():
        vertice_list.sort()

    return {
        "colores": colores,
        "numero_colores": numero_cromatico_aproximado(grafo),
        "es_valido": verificar_coloreo(grafo, colores),
        "vertices_por_color": dict(sorted(vertices_por_color.items())),
    }
