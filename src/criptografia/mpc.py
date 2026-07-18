"""Implementación educativa de MPC.

Este módulo modela una computación multipartita segura muy básica usando
compartición aditiva de secretos. La idea es que varios participantes
contribuyen con sus datos sin revelarlos directamente y luego se reconstruye
el resultado agregado.
"""

from __future__ import annotations

from fractions import Fraction
from secrets import randbelow


def _normalizar_modulo(modulo: int | None) -> int | None:
    """Valida el módulo opcional usado para trabajar con enteros cerrados."""
    if modulo is None:
        return None
    if modulo <= 1:
        raise ValueError("El modulo debe ser mayor que 1.")
    return modulo


def compartir_secreto(secreto: int, num_participantes: int = 3, modulo: int | None = None) -> list[int]:
    """Divide un secreto en partes que solo permiten reconstruirlo en conjunto."""
    if num_participantes < 2:
        raise ValueError("Se requieren al menos 2 participantes.")

    modulo = _normalizar_modulo(modulo)

    partes = []
    acumulado = 0

    for _ in range(num_participantes - 1):
        if modulo is None:
            valor = randbelow(abs(secreto) + 10_000)
            if secreto < 0 and valor == 0:
                valor = 1
        else:
            valor = randbelow(modulo)
        partes.append(valor)
        acumulado += valor

    ultima_parte = secreto - acumulado
    if modulo is not None:
        ultima_parte %= modulo
        partes = [parte % modulo for parte in partes]

    partes.append(ultima_parte)
    return partes


def reconstruir_secreto(partes: list[int], modulo: int | None = None) -> int:
    """Reconstruye el secreto a partir de sus partes."""
    if not partes:
        raise ValueError("Se requiere al menos una parte.")

    modulo = _normalizar_modulo(modulo)
    total = sum(partes)
    if modulo is not None:
        return total % modulo
    return total


def suma_privada(valores: list[int], num_participantes: int = 3, modulo: int | None = None) -> int:
    """Calcula una suma privada usando compartición aditiva."""
    if not valores:
        raise ValueError("Se requiere al menos un valor.")

    modulo = _normalizar_modulo(modulo)
    acumulado_por_participante = [0] * num_participantes

    for valor in valores:
        partes = compartir_secreto(valor, num_participantes=num_participantes, modulo=modulo)
        for indice, parte in enumerate(partes):
            acumulado_por_participante[indice] += parte

    return reconstruir_secreto(acumulado_por_participante, modulo=modulo)


def promedio_privado(valores: list[int], num_participantes: int = 3, modulo: int | None = None) -> float:
    """Calcula el promedio a partir de una suma privada."""
    if not valores:
        raise ValueError("Se requiere al menos un valor.")

    total = suma_privada(valores, num_participantes=num_participantes, modulo=modulo)
    return float(Fraction(total, len(valores)))


def ejecutar_mpc(valores: list[int], num_participantes: int = 3, modulo: int | None = None) -> dict[str, float | int | list[int]]:
    """Ejecuta una demostración completa de MPC para una lista de enteros."""
    modulo = _normalizar_modulo(modulo)
    total = suma_privada(valores, num_participantes=num_participantes, modulo=modulo)
    return {
        "valores": valores,
        "num_participantes": num_participantes,
        "modulo": modulo if modulo is not None else 0,
        "suma_privada": total,
        "promedio_privado": promedio_privado(valores, num_participantes=num_participantes, modulo=modulo),
    }
