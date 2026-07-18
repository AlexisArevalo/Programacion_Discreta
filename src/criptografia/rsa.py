"""Implementacion educativa de RSA."""

from __future__ import annotations

from math import gcd
from typing import List, Optional, Tuple


def es_primo(numero: int) -> bool:
    """Determina si un numero es primo usando division de prueba."""
    if numero < 2:
        return False
    if numero in (2, 3):
        return True
    if numero % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2
    return True


def _validar_primos(p: int, q: int) -> None:
    if not es_primo(p) or not es_primo(q):
        raise ValueError("p y q deben ser numeros primos.")
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")


def _e_por_defecto(phi: int) -> int:
    """Busca un exponente publico pequeno y coprimo con phi."""
    candidato = 65537
    if candidato < phi and gcd(candidato, phi) == 1:
        return candidato

    candidato = 3
    while candidato < phi:
        if gcd(candidato, phi) == 1:
            return candidato
        candidato += 2

    raise ValueError("No se pudo encontrar un exponente publico valido.")


def generar_claves(p: int, q: int, e: Optional[int] = None) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Genera la clave publica y privada de RSA."""
    _validar_primos(p, q)

    n = p * q
    phi = (p - 1) * (q - 1)

    if e is None:
        e = _e_por_defecto(phi)
    elif not (1 < e < phi):
        raise ValueError("e debe estar entre 1 y phi(n).")

    if gcd(e, phi) != 1:
        raise ValueError("e debe ser coprimo con phi(n).")

    d = pow(e, -1, phi)
    return (e, n), (d, n)


def cifrar_numero(mensaje: int, clave_publica: Tuple[int, int]) -> int:
    """Cifra un numero entero con RSA."""
    e, n = clave_publica
    if mensaje < 0 or mensaje >= n:
        raise ValueError("El mensaje debe estar en el rango [0, n).")
    return pow(mensaje, e, n)


def descifrar_numero(cifrado: int, clave_privada: Tuple[int, int]) -> int:
    """Descifra un numero entero con RSA."""
    d, n = clave_privada
    if cifrado < 0 or cifrado >= n:
        raise ValueError("El cifrado debe estar en el rango [0, n).")
    return pow(cifrado, d, n)


def texto_a_codigos(texto: str) -> List[int]:
    """Convierte texto a codigos ASCII."""
    return [ord(caracter) for caracter in texto]


def codigos_a_texto(codigos: List[int]) -> str:
    """Convierte codigos ASCII a texto."""
    return "".join(chr(codigo) for codigo in codigos)


def cifrar_texto(texto: str, clave_publica: Tuple[int, int]) -> List[int]:
    """Cifra texto ASCII caracter por caracter."""
    return [cifrar_numero(codigo, clave_publica) for codigo in texto_a_codigos(texto)]


def descifrar_texto(cifrado: List[int], clave_privada: Tuple[int, int]) -> str:
    """Descifra una secuencia de bloques RSA."""
    codigos = [descifrar_numero(bloque, clave_privada) for bloque in cifrado]
    return codigos_a_texto(codigos)


def procesar_rsa(texto: str, p: int, q: int, e: Optional[int] = None) -> Tuple[Tuple[int, int], Tuple[int, int], List[int]]:
    """Genera claves y cifra un texto en un solo paso."""
    clave_publica, clave_privada = generar_claves(p, q, e)
    return clave_publica, clave_privada, cifrar_texto(texto, clave_publica)
