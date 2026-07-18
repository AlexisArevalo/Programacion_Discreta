"""Coloreo de grafos.

Se usa un algoritmo voraz sencillo: se recorren los nodos en un orden
determinista y se asigna el menor color disponible que no esté en conflicto
con los vecinos.
"""

from __future__ import annotations

from typing import Any


Grafo = dict[str, dict[str, float]]


def _validar_grafo_no_dirigido(grafo: Grafo) -> None:
    """Valida que el grafo sea no dirigido y no vacío."""
    if not grafo:
        raise ValueError("El grafo no puede estar vacio.")

    for nodo, vecinos in grafo.items():
        if not isinstance(vecinos, dict):
            raise TypeError(f"Los vecinos de {nodo} deben estar en un diccionario.")
        for vecino, peso in vecinos.items():
            if peso < 0:
                raise ValueError(f"La arista {nodo} -> {vecino} tiene peso negativo.")
            if vecino not in grafo:
                raise KeyError(f"El vecino {vecino!r} no existe como nodo del grafo.")
            if nodo not in grafo[vecino]:
                raise ValueError(f"El grafo debe ser no dirigido: falta {vecino} -> {nodo}.")


def colorear_grafo(grafo: Grafo) -> dict[str, int]:
    """Colorea un grafo usando la estrategia voraz."""
    _validar_grafo_no_dirigido(grafo)

    coloreado: dict[str, int] = {}
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


def verificar_coloreo(grafo: Grafo, colores: dict[str, int]) -> bool:
    """Comprueba que el coloreo sea válido."""
    _validar_grafo_no_dirigido(grafo)
    for nodo, vecinos in grafo.items():
        if nodo not in colores:
            return False
        for vecino in vecinos:
            if colores[nodo] == colores.get(vecino):
                return False
    return True


def resumen_coloreo(grafo: Grafo) -> dict[str, Any]:
    """Devuelve un resumen útil para mostrar en consola."""
    colores = colorear_grafo(grafo)
    return {
        "colores": colores,
        "numero_colores": numero_cromatico_aproximado(grafo),
        "es_valido": verificar_coloreo(grafo, colores),
    }
