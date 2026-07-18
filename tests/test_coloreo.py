"""Pruebas para coloreo de grafos."""

import unittest

from src.grafos.coloreo import colorear_grafo, numero_cromatico_aproximado, resumen_coloreo, verificar_coloreo


GRAFO_EJEMPLO = {
    "A": {"B": 1, "C": 1},
    "B": {"A": 1, "C": 1, "D": 1},
    "C": {"A": 1, "B": 1, "D": 1},
    "D": {"B": 1, "C": 1},
}


class TestColoreo(unittest.TestCase):
    def test_colorear_grafo(self) -> None:
        colores = colorear_grafo(GRAFO_EJEMPLO)
        self.assertTrue(verificar_coloreo(GRAFO_EJEMPLO, colores))
        self.assertEqual(colores["A"], 1)
        self.assertEqual(colores["B"], 2)

    def test_numero_cromatico_aproximado(self) -> None:
        self.assertEqual(numero_cromatico_aproximado(GRAFO_EJEMPLO), 3)

    def test_resumen_coloreo(self) -> None:
        resultado = resumen_coloreo(GRAFO_EJEMPLO)
        self.assertTrue(resultado["es_valido"])
        self.assertEqual(resultado["numero_colores"], 3)


if __name__ == "__main__":
    unittest.main()
