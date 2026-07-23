"""Pruebas para MPC."""

import unittest

from src.criptografia.mpc import (
    compartir_secreto,
    ejecutar_mpc,
    promedio_privado,
    reconstruir_secreto,
    suma_privada,
)


class TestMPC(unittest.TestCase):
    def test_compartir_y_reconstruir_secreto(self) -> None:
        partes = compartir_secreto(42, modulo=97)
        self.assertEqual(len(partes), 3)
        self.assertEqual(reconstruir_secreto(partes, modulo=97), 42)

    def test_suma_privada(self) -> None:
        self.assertEqual(suma_privada([3, 5, 7], modulo=101), 15)

    def test_promedio_privado(self) -> None:
        self.assertEqual(promedio_privado([2, 4, 6, 8]), 5.0)

    def test_ejecutar_mpc(self) -> None:
        resultado = ejecutar_mpc([40, 35, 50, 25])
        self.assertEqual(resultado["suma_total"], 150)
        self.assertEqual(resultado["promedio"], 37.5)


if __name__ == "__main__":
    unittest.main()
