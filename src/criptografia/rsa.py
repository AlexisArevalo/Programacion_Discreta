"""Implementacion educativa de RSA."""

from __future__ import annotations

from math import gcd
from typing import List, Tuple


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


def euclides_extendido(a: int, b: int) -> Tuple[int, int, int]:
    """Retorna gcd(a, b) y coeficientes de Bezout."""
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0

    gcd_ab, x1, y1 = euclides_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_ab, x, y


def inverso_modular(e: int, modulo: int) -> int:
    """Calcula el inverso modular de e modulo `modulo`."""
    if modulo <= 0:
        raise ValueError("El modulo debe ser mayor que 0.")

    gcd_em, x, _ = euclides_extendido(e, modulo)
    if gcd_em != 1:
        raise ValueError("e no tiene inverso modular con phi(n).")
    return x % modulo


def generar_claves(p: int, q: int, e: int) -> Tuple[Tuple[int, int], Tuple[int, int], int, int]:
    """Genera n, phi(n), la clave publica y la clave privada de RSA."""
    _validar_primos(p, q)
    if e is None:
        raise ValueError("e es obligatorio.")

    n = p * q
    phi = (p - 1) * (q - 1)

    if not (1 < e < phi):
        raise ValueError("e debe estar entre 1 y phi(n).")

    if gcd(e, phi) != 1:
        raise ValueError("e debe ser coprimo con phi(n).")

    d = inverso_modular(e, phi)
    return (e, n), (d, n), n, phi


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


def procesar_rsa(texto: str, p: int, q: int, e: int) -> Tuple[Tuple[int, int], Tuple[int, int], List[int]]:
    """Genera claves y cifra un texto en un solo paso."""
    clave_publica, clave_privada, _, _ = generar_claves(p, q, e)
    return clave_publica, clave_privada, cifrar_texto(texto, clave_publica)
