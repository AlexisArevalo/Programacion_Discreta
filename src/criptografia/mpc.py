"""Implementacion educativa de MPC."""

from __future__ import annotations

from fractions import Fraction
from secrets import randbelow
from typing import Dict, List, Optional

NUM_SERVIDORES = 3
MODULO_POR_DEFECTO = 1_000_003
 

def _normalizar_modulo(modulo: Optional[int]) -> Optional[int]:
    """Valida el modulo opcional usado para trabajar con enteros cerrados."""
    if modulo is None:
        return MODULO_POR_DEFECTO
    if modulo <= 1:
        raise ValueError("El modulo debe ser mayor que 1.")
    return modulo


def compartir_secreto(secreto: int, modulo: Optional[int] = None) -> List[int]:
    """Divide un secreto en partes que solo permiten reconstruirlo en conjunto."""
    modulo = _normalizar_modulo(modulo)

    partes: List[int] = []
    acumulado = 0

    for _ in range(NUM_SERVIDORES - 1):
        valor = randbelow(modulo)
        partes.append(valor)
        acumulado += valor

    ultima_parte = secreto - acumulado
    ultima_parte %= modulo
    partes = [parte % modulo for parte in partes]

    partes.append(ultima_parte)
    return partes


def reconstruir_secreto(partes: List[int], modulo: Optional[int] = None) -> int:
    """Reconstruye el secreto a partir de sus partes."""
    if not partes:
        raise ValueError("Se requiere al menos una parte.")

    modulo = _normalizar_modulo(modulo)
    total = sum(partes)
    return total % modulo


def suma_privada(valores: List[int], modulo: Optional[int] = None) -> int:
    """Calcula una suma privada usando comparticion aditiva."""
    if not valores:
        raise ValueError("Se requiere al menos un valor.")

    modulo = _normalizar_modulo(modulo)
    acumulado_por_participante = [0] * NUM_SERVIDORES

    for valor in valores:
        partes = compartir_secreto(valor, modulo=modulo)
        for indice, parte in enumerate(partes):
            acumulado_por_participante[indice] += parte

    return reconstruir_secreto(acumulado_por_participante, modulo=modulo)


def promedio_privado(valores: List[int], modulo: Optional[int] = None) -> float:
    """Calcula el promedio a partir de una suma privada."""
    if not valores:
        raise ValueError("Se requiere al menos un valor.")

    total = suma_privada(valores, modulo=modulo)
    return float(Fraction(total, len(valores)))


def ejecutar_mpc(valores: List[int], modulo: Optional[int] = None) -> Dict[str, float]:
    """Ejecuta una demostracion completa de MPC para una lista de enteros."""
    modulo = _normalizar_modulo(modulo)
    total = suma_privada(valores, modulo=modulo)
    return {
        "suma_total": total,
        "promedio": promedio_privado(valores, modulo=modulo),
    }


def simular_mpc(valores: List[int], modulo: Optional[int] = None) -> Dict[str, object]:
    """Simula el reparto y la reconstruccion paso a paso."""
    if not valores:
        raise ValueError("Se requiere al menos un valor.")

    modulo = _normalizar_modulo(modulo)
    acumulado_por_servidor = [0] * NUM_SERVIDORES
    pasos: List[Dict[str, object]] = []

    for indice, valor in enumerate(valores, start=1):
        partes = compartir_secreto(valor, modulo=modulo)
        for servidor, parte in enumerate(partes):
            acumulado_por_servidor[servidor] = (acumulado_por_servidor[servidor] + parte) % modulo

        suma_parcial = reconstruir_secreto(acumulado_por_servidor, modulo=modulo)
        pasos.append(
            {
                "numero_nota": indice,
                "nota": valor,
                "partes": partes,
                "acumulado_por_servidor": acumulado_por_servidor.copy(),
                "suma_parcial": suma_parcial,
            }
        )

    suma_total = reconstruir_secreto(acumulado_por_servidor, modulo=modulo)
    return {
        "modulo": modulo,
        "pasos": pasos,
        "acumulado_por_servidor": acumulado_por_servidor,
        "suma_total": suma_total,
        "promedio": float(Fraction(suma_total, len(valores))),
    }
