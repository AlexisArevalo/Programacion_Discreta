"""Simplificacion booleana.

El modulo ofrece formas canonicas y una simplificacion basica por
minimizacion de terminos de la forma suma de productos para funciones con
pocas variables.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from src.boole.tablas_verdad import obtener_variables, tabla_verdad


def _a_binario(numero: int, bits: int) -> str:
    return format(numero, "0%db" % bits)


def _contar_unos(termino: str) -> int:
    return termino.count("1")


def _combinar(a: str, b: str) -> Optional[str]:
    diferencias = 0
    resultado = []
    for char_a, char_b in zip(a, b):
        if char_a == char_b:
            resultado.append(char_a)
        else:
            diferencias += 1
            resultado.append("-")
    if diferencias == 1:
        return "".join(resultado)
    return None


def _cubierto(implicante: str, mintermino: str) -> bool:
    return all(i == "-" or i == m for i, m in zip(implicante, mintermino))


def forma_normal_disyuntiva(expresion: str) -> str:
    """Construye la forma normal disyuntiva canonica."""
    variables = obtener_variables(expresion)
    tabla = tabla_verdad(expresion)
    if not variables:
        return "1" if tabla[0]["resultado"] else "0"

    terminos: List[str] = []
    for indice, fila in enumerate(tabla):
        if fila["resultado"]:
            binario = _a_binario(indice, len(variables))
            partes = []
            for variable, bit in zip(variables, binario):
                partes.append(variable if bit == "1" else "not %s" % variable)
            terminos.append(" and ".join(partes))

    if not terminos:
        return "0"
    return " or ".join("(%s)" % termino for termino in terminos)


def forma_normal_conjuntiva(expresion: str) -> str:
    """Construye la forma normal conjuntiva canonica."""
    variables = obtener_variables(expresion)
    tabla = tabla_verdad(expresion)
    if not variables:
        return "0" if tabla[0]["resultado"] else "1"

    terminos: List[str] = []
    for indice, fila in enumerate(tabla):
        if not fila["resultado"]:
            binario = _a_binario(indice, len(variables))
            partes = []
            for variable, bit in zip(variables, binario):
                partes.append(variable if bit == "0" else "not %s" % variable)
            terminos.append(" or ".join(partes))

    if not terminos:
        return "1"
    return " and ".join("(%s)" % termino for termino in terminos)


def simplificar_sop(expresion: str) -> str:
    """Simplifica una expresion usando una estrategia tipo Quine-McCluskey."""
    variables = obtener_variables(expresion)
    tabla = tabla_verdad(expresion)
    minterminos = [indice for indice, fila in enumerate(tabla) if fila["resultado"]]

    if not minterminos:
        return "0"
    if len(minterminos) == 2 ** len(variables):
        return "1"
    if not variables:
        return "1" if tabla[0]["resultado"] else "0"

    grupos: Dict[int, Set[str]] = {}
    for mintermino in minterminos:
        termino = _a_binario(mintermino, len(variables))
        grupos.setdefault(_contar_unos(termino), set()).add(termino)

    implicantes_primos: Set[str] = set()

    while grupos:
        nuevos_grupos: Dict[int, Set[str]] = {}
        usados: Set[str] = set()
        llaves = sorted(grupos)

        for indice, llave in enumerate(llaves[:-1]):
            grupo_actual = grupos[llave]
            grupo_siguiente = grupos[llaves[indice + 1]]
            for termino_a in grupo_actual:
                for termino_b in grupo_siguiente:
                    combinado = _combinar(termino_a, termino_b)
                    if combinado is not None:
                        usados.add(termino_a)
                        usados.add(termino_b)
                        nuevos_grupos.setdefault(combinado.count("1"), set()).add(combinado)

        for grupo in grupos.values():
            for termino in grupo:
                if termino not in usados:
                    implicantes_primos.add(termino)

        grupos = nuevos_grupos

    cobertura: List[str] = []
    minterminos_bin = [_a_binario(mintermino, len(variables)) for mintermino in minterminos]
    for implicante in sorted(implicantes_primos):
        if any(_cubierto(implicante, mintermino) for mintermino in minterminos_bin):
            cobertura.append(implicante)

    if not cobertura:
        return forma_normal_disyuntiva(expresion)

    terminos_simplificados = []
    for implicante in cobertura:
        partes = []
        for variable, bit in zip(variables, implicante):
            if bit == "1":
                partes.append(variable)
            elif bit == "0":
                partes.append("not %s" % variable)
        if partes:
            terminos_simplificados.append(" and ".join(partes))
        else:
            return "1"

    return " or ".join("(%s)" % termino for termino in terminos_simplificados)


def resumen_simplificacion(expresion: str) -> Dict[str, Any]:
    """Resume las distintas formas de la expresion booleana."""
    return {
        "expresion": expresion,
        "fdn": forma_normal_disyuntiva(expresion),
        "fcn": forma_normal_conjuntiva(expresion),
        "simplificada": simplificar_sop(expresion),
    }
