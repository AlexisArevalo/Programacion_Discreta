"""Análisis de cierre de estación.

El problema se modela como el estudio del impacto que produce la eliminación
de un nodo en un grafo no dirigido. En la práctica esto equivale a encontrar
estaciones críticas, es decir, puntos de articulación.
"""

from __future__ import annotations

from collections import deque
from typing import Any


Grafo = dict[str, dict[str, float]]


def _validar_grafo_no_dirigido(grafo: Grafo) -> None:
    """Valida que el grafo tenga estructura de adyacencia consistente."""
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


def estaciones_criticas(grafo: Grafo) -> list[str]:
    """Encuentra los puntos de articulación del grafo."""
    _validar_grafo_no_dirigido(grafo)

    tiempo = 0
    visitado: set[str] = set()
    descubierto: dict[str, int] = {}
    bajo: dict[str, int] = {}
    padre: dict[str, str | None] = {nodo: None for nodo in grafo}
    criticos: set[str] = set()

    def dfs(nodo: str) -> None:
        nonlocal tiempo
        visitado.add(nodo)
        descubierto[nodo] = tiempo
        bajo[nodo] = tiempo
        tiempo += 1

        hijos = 0
        for vecino in grafo[nodo]:
            if vecino not in visitado:
                padre[vecino] = nodo
                hijos += 1
                dfs(vecino)
                bajo[nodo] = min(bajo[nodo], bajo[vecino])

                if padre[nodo] is None and hijos > 1:
                    criticos.add(nodo)
                if padre[nodo] is not None and bajo[vecino] >= descubierto[nodo]:
                    criticos.add(nodo)
            elif vecino != padre[nodo]:
                bajo[nodo] = min(bajo[nodo], descubierto[vecino])

    for nodo in grafo:
        if nodo not in visitado:
            dfs(nodo)

    return sorted(criticos)


def componentes_con_estacion_cerrada(grafo: Grafo, estacion: str) -> list[list[str]]:
    """Devuelve las componentes conexas luego de cerrar una estación."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError(f"La estacion {estacion!r} no existe en el grafo.")

    visitado: set[str] = {estacion}
    componentes: list[list[str]] = []

    for nodo in grafo:
        if nodo in visitado:
            continue

        componente: list[str] = []
        cola: deque[str] = deque([nodo])
        visitado.add(nodo)

        while cola:
            actual = cola.popleft()
            componente.append(actual)
            for vecino in grafo[actual]:
                if vecino not in visitado and vecino != estacion:
                    visitado.add(vecino)
                    cola.append(vecino)

        componentes.append(sorted(componente))

    componentes.sort(key=lambda comp: (len(comp), comp))
    return componentes


def analizar_cierre(grafo: Grafo, estacion: str) -> dict[str, Any]:
    """Resume el efecto de cerrar una estación sobre el grafo."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError(f"La estacion {estacion!r} no existe en el grafo.")

    componentes = componentes_con_estacion_cerrada(grafo, estacion)
    criticos = estaciones_criticas(grafo)

    return {
        "estacion": estacion,
        "es_critica": estacion in criticos,
        "estaciones_criticas": criticos,
        "componentes_restantes": componentes,
        "numero_componentes": len(componentes),
    }
