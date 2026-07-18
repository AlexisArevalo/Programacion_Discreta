"""Pruebas para tablas de verdad."""

import unittest

from src.boole.tablas_verdad import contar_falsos, contar_verdaderos, obtener_variables, resumen_tabla_verdad, tabla_verdad


class TestTablasVerdad(unittest.TestCase):
    def test_obtener_variables(self) -> None:
        self.assertEqual(obtener_variables("a and b"), ["a", "b"])

    def test_tabla_verdad(self) -> None:
        filas = tabla_verdad("a and b")
        self.assertEqual(len(filas), 4)
        self.assertFalse(filas[0]["resultado"])
        self.assertTrue(filas[-1]["resultado"])

    def test_conteo(self) -> None:
        self.assertEqual(contar_verdaderos("a or b"), 3)
        self.assertEqual(contar_falsos("a or b"), 1)

    def test_resumen(self) -> None:
        resumen = resumen_tabla_verdad("a and not b")
        self.assertEqual(resumen["verdaderos"], 1)


if __name__ == "__main__":
    unittest.main()
