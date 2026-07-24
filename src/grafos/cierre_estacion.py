"""Analisis de cierre de estacion.

El problema se modela como el estudio del impacto que produce la eliminacion
de un nodo en un grafo no dirigido. En la practica se compara la distancia
minima antes y despues del cierre para varios pares origen-destino.
"""

from __future__ import annotations

from collections import deque
from math import inf
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from src.grafos.dijkstra import camino_mas_corto


Grafo = Dict[str, Dict[str, float]]
ParRuta = Tuple[str, str]


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


def cerrar_estacion(grafo: Grafo, estacion: str) -> Grafo:
    """Devuelve una copia del grafo sin la estacion indicada."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError("La estacion %r no existe en el grafo." % estacion)

    grafo_cerrado: Grafo = {}
    for nodo, vecinos in grafo.items():
        if nodo == estacion:
            continue
        grafo_cerrado[nodo] = {vecino: peso for vecino, peso in vecinos.items() if vecino != estacion}
    return grafo_cerrado


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


def _calcular_distancia(grafo: Grafo, origen: str, destino: str) -> float:
    """Calcula la distancia minima o infinito si no existe camino."""
    if origen not in grafo or destino not in grafo:
        return inf
    try:
        distancia, _ = camino_mas_corto(grafo, origen, destino)
    except ValueError:
        return inf
    return distancia


def analizar_impacto_cierre(grafo: Grafo, estacion: str, pares: Sequence[ParRuta]) -> Dict[str, Any]:
    """Compara las distancias antes y despues del cierre de una estacion."""
    _validar_grafo_no_dirigido(grafo)
    if estacion not in grafo:
        raise KeyError("La estacion %r no existe en el grafo." % estacion)
    if len(pares) < 5:
        raise ValueError("Se requieren al menos cinco pares origen-destino.")

    grafo_cerrado = cerrar_estacion(grafo, estacion)
    tabla: List[Dict[str, Any]] = []
    aumentaron: List[ParRuta] = []
    desconectados: List[ParRuta] = []

    for origen, destino in pares:
        if origen not in grafo or destino not in grafo:
            raise KeyError("Los nodos %r y/o %r no existen en el grafo." % (origen, destino))
        distancia_antes = _calcular_distancia(grafo, origen, destino)
        distancia_despues = _calcular_distancia(grafo_cerrado, origen, destino)

        if distancia_antes == inf and distancia_despues == inf:
            estado = "sin camino"
            diferencia = None
        elif distancia_antes == inf:
            estado = "solo despues"
            diferencia = None
        elif distancia_despues == inf:
            estado = "desconectado"
            diferencia = None
            desconectados.append((origen, destino))
        elif distancia_despues > distancia_antes:
            estado = "aumento"
            diferencia = distancia_despues - distancia_antes
            aumentaron.append((origen, destino))
        else:
            estado = "sin cambio"
            diferencia = distancia_despues - distancia_antes

        tabla.append(
            {
                "origen": origen,
                "destino": destino,
                "distancia_antes": distancia_antes,
                "distancia_despues": distancia_despues,
                "diferencia": diferencia,
                "estado": estado,
            }
        )

    return {
        "estacion_cerrada": estacion,
        "tabla": tabla,
        "pares_con_aumento": aumentaron,
        "pares_desconectados": desconectados,
    }
