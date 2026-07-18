"""Analisis de cierre de estacion.

El problema se modela como el estudio del impacto que produce la eliminacion
de un nodo en un grafo no dirigido. En la practica esto equivale a encontrar
estaciones criticas, es decir, puntos de articulacion.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Optional, Set


Grafo = Dict[str, Dict[str, float]]


def _validar_grafo_no_dirigido(grafo: Grafo) -> None:
    """Valida que el grafo tenga estructura de adyacencia consistente."""
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


def estaciones_criticas(grafo: Grafo) -> List[str]:
    """Encuentra los puntos de articulacion del grafo."""
    _validar_grafo_no_dirigido(grafo)

    tiempo = 0
    visitado: Set[str] = set()
    descubierto: Dict[str, int] = {}
    bajo: Dict[str, int] = {}
    padre: Dict[str, Optional[str]] = {nodo: None for nodo in grafo}
    criticos: Set[str] = set()

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


def componentes_con_estacion_cerrada(grafo: Grafo, estacion: str) -> List[List[str]]:
    """Devuelve las componentes conexas luego de cerrar una estacion."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError("La estacion %r no existe en el grafo." % estacion)

    visitado: Set[str] = {estacion}
    componentes: List[List[str]] = []

    for nodo in grafo:
        if nodo in visitado:
            continue

        componente: List[str] = []
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


def analizar_cierre(grafo: Grafo, estacion: str) -> Dict[str, Any]:
    """Resume el efecto de cerrar una estacion sobre el grafo."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError("La estacion %r no existe en el grafo." % estacion)

    componentes = componentes_con_estacion_cerrada(grafo, estacion)
    criticos = estaciones_criticas(grafo)

    return {
        "estacion": estacion,
        "es_critica": estacion in criticos,
        "estaciones_criticas": criticos,
        "componentes_restantes": componentes,
        "numero_componentes": len(componentes),
    }
