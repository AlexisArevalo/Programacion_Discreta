"""Algoritmo de Dijkstra.

Se trabaja con un grafo representado como un diccionario de adyacencia:

    {
        "A": {"B": 4, "C": 2},
        "B": {"C": 1},
    }

Las aristas deben tener pesos no negativos.
"""

from __future__ import annotations

import json
from heapq import heappop, heappush
from pathlib import Path
from typing import Any


Grafo = dict[str, dict[str, float]]


def validar_grafo(grafo: Grafo) -> None:
    """Valida que el grafo tenga pesos no negativos."""
    if not grafo:
        raise ValueError("El grafo no puede estar vacio.")

    for nodo, vecinos in grafo.items():
        if not isinstance(vecinos, dict):
            raise TypeError(f"Los vecinos de {nodo} deben estar en un diccionario.")
        for vecino, peso in vecinos.items():
            if peso < 0:
                raise ValueError(f"La arista {nodo} -> {vecino} tiene peso negativo.")


def cargar_grafo_desde_json(ruta: str | Path) -> Grafo:
    """Carga un grafo desde un archivo JSON."""
    ruta = Path(ruta)
    with ruta.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if not isinstance(datos, dict):
        raise TypeError("El JSON debe contener un objeto con nodos y adyacencias.")

    grafo: Grafo = {}
    for nodo, vecinos in datos.items():
        if not isinstance(vecinos, dict):
            raise TypeError("Cada nodo debe mapear a un diccionario de vecinos.")
        grafo[str(nodo)] = {str(vecino): float(peso) for vecino, peso in vecinos.items()}

    validar_grafo(grafo)
    return grafo


def dijkstra(grafo: Grafo, origen: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """Calcula las distancias mínimas desde un nodo origen."""
    validar_grafo(grafo)
    if origen not in grafo:
        raise KeyError(f"El nodo origen {origen!r} no existe en el grafo.")

    distancias = {nodo: float("inf") for nodo in grafo}
    predecesores: dict[str, str | None] = {nodo: None for nodo in grafo}
    visitados: set[str] = set()
    cola: list[tuple[float, str]] = [(0.0, origen)]
    distancias[origen] = 0.0

    while cola:
        distancia_actual, nodo_actual = heappop(cola)
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heappush(cola, (nueva_distancia, vecino))

    return distancias, predecesores


def reconstruir_camino(
    predecesores: dict[str, str | None],
    origen: str,
    destino: str,
) -> list[str]:
    """Reconstruye el camino mínimo usando la tabla de predecesores."""
    if origen == destino:
        return [origen]

    camino = [destino]
    actual = destino

    while actual != origen:
        actual = predecesores.get(actual)
        if actual is None:
            raise ValueError(f"No existe camino desde {origen!r} hasta {destino!r}.")
        camino.append(actual)

    camino.reverse()
    return camino


def camino_mas_corto(grafo: Grafo, origen: str, destino: str) -> tuple[float, list[str]]:
    """Calcula la distancia y el camino mínimo entre dos nodos."""
    distancias, predecesores = dijkstra(grafo, origen)
    distancia = distancias.get(destino, float("inf"))
    if distancia == float("inf"):
        raise ValueError(f"No existe camino desde {origen!r} hasta {destino!r}.")

    camino = reconstruir_camino(predecesores, origen, destino)
    return distancia, camino


def resumen_distancias(grafo: Grafo, origen: str) -> dict[str, Any]:
    """Devuelve un resumen útil para mostrar en consola."""
    distancias, predecesores = dijkstra(grafo, origen)
    return {
        "origen": origen,
        "distancias": distancias,
        "predecesores": predecesores,
    }
