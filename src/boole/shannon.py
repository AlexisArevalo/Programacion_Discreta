"""Entropia de Shannon."""

from __future__ import annotations

from math import log2
from typing import Any


def validar_distribucion(probabilidades: list[float]) -> None:
    """Valida que la distribucion sea coherente."""
    if not probabilidades:
        raise ValueError("La distribucion no puede estar vacia.")
    if any(probabilidad < 0 for probabilidad in probabilidades):
        raise ValueError("No se permiten probabilidades negativas.")

    total = sum(probabilidades)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("Las probabilidades deben sumar 1.")


def entropia_shannon(probabilidades: list[float]) -> float:
    """Calcula la entropia de Shannon."""
    validar_distribucion(probabilidades)
    entropia = 0.0
    for probabilidad in probabilidades:
        if probabilidad > 0:
            entropia -= probabilidad * log2(probabilidad)
    return entropia


def probabilidad_desde_frecuencias(frecuencias: list[int]) -> list[float]:
    """Convierte frecuencias a probabilidades."""
    if not frecuencias:
        raise ValueError("Se requieren frecuencias.")
    if any(frecuencia < 0 for frecuencia in frecuencias):
        raise ValueError("No se permiten frecuencias negativas.")

    total = sum(frecuencias)
    if total == 0:
        raise ValueError("La suma de frecuencias debe ser mayor que 0.")
    return [frecuencia / total for frecuencia in frecuencias]


def entropia_desde_frecuencias(frecuencias: list[int]) -> float:
    """Calcula la entropia a partir de frecuencias absolutas."""
    return entropia_shannon(probabilidad_desde_frecuencias(frecuencias))


def resumen_shannon(probabilidades: list[float]) -> dict[str, Any]:
    """Devuelve un resumen util para consola o pruebas."""
    return {
        "probabilidades": probabilidades,
        "entropia": entropia_shannon(probabilidades),
    }
