"""Tablas de verdad.

Este modulo evalua expresiones booleanas sobre un conjunto de variables y
genera la tabla completa de resultados.
"""

from __future__ import annotations

import ast
import itertools
from typing import Any


ALLOWED_BOOLNODES = (
    ast.Expression,
    ast.BoolOp,
    ast.UnaryOp,
    ast.Name,
    ast.Constant,
    ast.Load,
    ast.Compare,
    ast.And,
    ast.Or,
    ast.Not,
    ast.NotEq,
)


class BooleanExpressionError(ValueError):
    """Se lanza cuando la expresion booleana no es valida."""


def _normalizar_expresion(expresion: str) -> str:
    """Normaliza sintaxis alternativa a operadores validos de Python."""
    return (
        expresion.replace("∧", " and ")
        .replace("∨", " or ")
        .replace("¬", " not ")
        .replace("^", " != ")
    )


def validar_expresion(expresion: str) -> ast.Expression:
    """Valida que una expresion use solo nodos booleanos permitidos."""
    if not expresion or not expresion.strip():
        raise BooleanExpressionError("La expresion no puede estar vacia.")

    expresion = _normalizar_expresion(expresion)
    arbol = ast.parse(expresion, mode="eval")

    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ALLOWED_BOOLNODES):
            raise BooleanExpressionError(f"Nodo no permitido en la expresion: {type(nodo).__name__}")
        if isinstance(nodo, ast.BoolOp) and not isinstance(nodo.op, (ast.And, ast.Or)):
            raise BooleanExpressionError("Solo se permiten operadores booleanos and/or.")
        if isinstance(nodo, ast.UnaryOp) and not isinstance(nodo.op, ast.Not):
            raise BooleanExpressionError("Solo se permite el operador not.")
        if isinstance(nodo, ast.Compare) and len(nodo.ops) != 1:
            raise BooleanExpressionError("No se permiten comparaciones encadenadas.")
        if isinstance(nodo, ast.Compare) and not isinstance(nodo.ops[0], ast.NotEq):
            raise BooleanExpressionError("Solo se permite el operador xor mediante ^.")

    return arbol


def obtener_variables(expresion: str) -> list[str]:
    """Obtiene las variables usadas en una expresion booleana."""
    arbol = validar_expresion(expresion)
    variables = sorted({nodo.id for nodo in ast.walk(arbol) if isinstance(nodo, ast.Name)})
    return variables


def evaluar_expresion(expresion: str, valores: dict[str, bool]) -> bool:
    """Evalua una expresion booleana con un conjunto de valores."""
    arbol = validar_expresion(expresion)
    contexto = {nombre: bool(valor) for nombre, valor in valores.items()}
    codigo = compile(arbol, "<expresion_booleana>", "eval")
    return bool(eval(codigo, {"__builtins__": {}}, contexto))


def generar_combinaciones(variables: list[str]) -> list[dict[str, bool]]:
    """Genera todas las combinaciones posibles de variables."""
    combinaciones = []
    for valores in itertools.product([False, True], repeat=len(variables)):
        combinaciones.append(dict(zip(variables, valores, strict=False)))
    return combinaciones


def tabla_verdad(expresion: str) -> list[dict[str, Any]]:
    """Construye la tabla de verdad de una expresion."""
    variables = obtener_variables(expresion)
    filas = []
    for combinacion in generar_combinaciones(variables):
        resultado = evaluar_expresion(expresion, combinacion)
        fila = dict(combinacion)
        fila["resultado"] = resultado
        filas.append(fila)
    return filas


def contar_verdaderos(expresion: str) -> int:
    """Cuenta cuantas filas hacen verdadera la expresion."""
    return sum(1 for fila in tabla_verdad(expresion) if fila["resultado"])


def contar_falsos(expresion: str) -> int:
    """Cuenta cuantas filas hacen falsa la expresion."""
    filas = tabla_verdad(expresion)
    return sum(1 for fila in filas if not fila["resultado"])


def resumen_tabla_verdad(expresion: str) -> dict[str, Any]:
    """Devuelve un resumen util para consola o pruebas."""
    filas = tabla_verdad(expresion)
    variables = obtener_variables(expresion)
    return {
        "expresion": expresion,
        "variables": variables,
        "filas": filas,
        "numero_filas": len(filas),
        "verdaderos": contar_verdaderos(expresion),
        "falsos": contar_falsos(expresion),
    }
