"""Simulación de un qubit.

Se modela un qubit como un vector de dos amplitudes complejas:

    |psi> = alpha |0> + beta |1>

Las funciones de este módulo permiten crear estados base, aplicar puertas
cuánticas simples y consultar probabilidades de medición.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, sqrt
from typing import Any


TOLERANCIA = 1e-9


@dataclass(frozen=True)
class Qubit:
    """Representa un qubit de un solo bit cuántico."""

    alpha: complex
    beta: complex

    def __post_init__(self) -> None:
        norma_cuadrada = abs(self.alpha) ** 2 + abs(self.beta) ** 2
        if not isclose(norma_cuadrada, 1.0, rel_tol=0.0, abs_tol=TOLERANCIA):
            raise ValueError("Las amplitudes del qubit deben estar normalizadas.")


def crear_qubit(alpha: complex, beta: complex) -> Qubit:
    """Crea un qubit validando la normalización."""
    return Qubit(alpha, beta)


def ket_0() -> Qubit:
    """Devuelve el estado base |0>."""
    return Qubit(1 + 0j, 0 + 0j)


def ket_1() -> Qubit:
    """Devuelve el estado base |1>."""
    return Qubit(0 + 0j, 1 + 0j)


def superposicion() -> Qubit:
    """Devuelve el estado de superposición uniforme."""
    coeficiente = 1 / sqrt(2)
    return Qubit(coeficiente, coeficiente)


def probabilidades(qubit: Qubit) -> dict[str, float]:
    """Calcula las probabilidades de medir 0 o 1."""
    prob_cero = abs(qubit.alpha) ** 2
    prob_uno = abs(qubit.beta) ** 2
    return {"0": prob_cero, "1": prob_uno}


def aplicar_puerta_x(qubit: Qubit) -> Qubit:
    """Aplica la puerta Pauli-X."""
    return Qubit(qubit.beta, qubit.alpha)


def aplicar_puerta_h(qubit: Qubit) -> Qubit:
    """Aplica la puerta de Hadamard."""
    factor = 1 / sqrt(2)
    alpha = (qubit.alpha + qubit.beta) * factor
    beta = (qubit.alpha - qubit.beta) * factor
    return Qubit(alpha, beta)


def medir_probabilidad(qubit: Qubit) -> dict[str, Any]:
    """Devuelve un resumen de medición sin introducir aleatoriedad."""
    probs = probabilidades(qubit)
    resultado = "0" if probs["0"] >= probs["1"] else "1"
    return {
        "probabilidades": probs,
        "resultado_mas_probable": resultado,
    }


def resumen_qubit(qubit: Qubit) -> dict[str, Any]:
    """Devuelve un resumen completo del estado del qubit."""
    return {
        "alpha": qubit.alpha,
        "beta": qubit.beta,
        "probabilidades": probabilidades(qubit),
        "medicion": medir_probabilidad(qubit),
    }
