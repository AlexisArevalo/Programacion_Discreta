"""Algoritmo de Dijkstra.

Se trabaja con un grafo representado como un diccionario de adyacencia.
"""

from __future__ import annotations

import json
from heapq import heappop, heappush
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


Grafo = Dict[str, Dict[str, float]]


def validar_grafo(grafo: Grafo) -> None:
    """Valida que el grafo tenga pesos no negativos."""
    if not grafo:
        raise ValueError("El grafo no puede estar vacio.")

    for nodo, vecinos in grafo.items():
        if not isinstance(vecinos, dict):
            raise TypeError("Los vecinos de %s deben estar en un diccionario." % nodo)
        for vecino, peso in vecinos.items():
            if peso < 0:
                raise ValueError("La arista %s -> %s tiene peso negativo." % (nodo, vecino))


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


def dijkstra(grafo: Grafo, origen: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """Calcula las distancias minimas desde un nodo origen."""
    validar_grafo(grafo)
    if origen not in grafo:
        raise KeyError("El nodo origen %r no existe en el grafo." % origen)

    distancias = {nodo: float("inf") for nodo in grafo}
    predecesores: Dict[str, Optional[str]] = {nodo: None for nodo in grafo}
    visitados: set = set()
    cola: List[Tuple[float, str]] = [(0.0, origen)]
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
    predecesores: Dict[str, Optional[str]],
    origen: str,
    destino: str,
) -> List[str]:
    """Reconstruye el camino minimo usando la tabla de predecesores."""
    if origen == destino:
        return [origen]

    camino = [destino]
    actual = destino

    while actual != origen:
        actual = predecesores.get(actual)
        if actual is None:
            raise ValueError("No existe camino desde %r hasta %r." % (origen, destino))
        camino.append(actual)

    camino.reverse()
    return camino


def camino_mas_corto(grafo: Grafo, origen: str, destino: str) -> Tuple[float, List[str]]:
    """Calcula la distancia y el camino minimo entre dos nodos."""
    distancias, predecesores = dijkstra(grafo, origen)
    distancia = distancias.get(destino, float("inf"))
    if distancia == float("inf"):
        raise ValueError("No existe camino desde %r hasta %r." % (origen, destino))

    camino = reconstruir_camino(predecesores, origen, destino)
    return distancia, camino


def resumen_distancias(grafo: Grafo, origen: str) -> Dict[str, Any]:
    """Devuelve un resumen util para mostrar en consola."""
    distancias, predecesores = dijkstra(grafo, origen)
    return {
        "origen": origen,
        "distancias": distancias,
        "predecesores": predecesores,
    }
