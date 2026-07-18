"""Implementación del cifrado César.

El algoritmo desplaza cada letra dentro del alfabeto latino estándar,
preservando mayúsculas, minúsculas y caracteres no alfabéticos.
"""

from __future__ import annotations

import string

ALFABETO_MAYUSCULA = string.ascii_uppercase
ALFABETO_MINUSCULA = string.ascii_lowercase


def normalizar_desplazamiento(desplazamiento: int, longitud: int = 26) -> int:
    """Reduce cualquier desplazamiento al rango del alfabeto."""
    return desplazamiento % longitud


def _desplazar_caracter(caracter: str, desplazamiento: int) -> str:
    """Desplaza un único carácter si pertenece al alfabeto latino."""
    if caracter in ALFABETO_MAYUSCULA:
        alfabeto = ALFABETO_MAYUSCULA
    elif caracter in ALFABETO_MINUSCULA:
        alfabeto = ALFABETO_MINUSCULA
    else:
        return caracter

    indice = alfabeto.index(caracter)
    nuevo_indice = (indice + desplazamiento) % len(alfabeto)
    return alfabeto[nuevo_indice]


def cifrar_cesar(texto: str, desplazamiento: int) -> str:
    """Cifra `texto` usando el algoritmo de César."""
    desplazamiento = normalizar_desplazamiento(desplazamiento)
    return "".join(_desplazar_caracter(caracter, desplazamiento) for caracter in texto)


def descifrar_cesar(texto: str, desplazamiento: int) -> str:
    """Descifra `texto` usando el algoritmo de César."""
    return cifrar_cesar(texto, -desplazamiento)


def procesar_cesar(texto: str, desplazamiento: int, modo: str = "cifrar") -> str:
    """Procesa texto en modo cifrar o descifrar."""
    modo_normalizado = modo.strip().lower()
    if modo_normalizado == "cifrar":
        return cifrar_cesar(texto, desplazamiento)
    if modo_normalizado == "descifrar":
        return descifrar_cesar(texto, desplazamiento)
    raise ValueError("El modo debe ser 'cifrar' o 'descifrar'.")
