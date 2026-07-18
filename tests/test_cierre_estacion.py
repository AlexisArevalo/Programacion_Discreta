"""Pruebas para cierre de estación."""

import unittest

from src.grafos.cierre_estacion import analizar_cierre, componentes_con_estacion_cerrada, estaciones_criticas


GRAFO_EJEMPLO = {
    "A": {"B": 1, "C": 1},
    "B": {"A": 1, "C": 1, "D": 1},
    "C": {"A": 1, "B": 1},
    "D": {"B": 1, "E": 1, "F": 1},
    "E": {"D": 1, "F": 1},
    "F": {"D": 1, "E": 1},
}


class TestCierreEstacion(unittest.TestCase):
    def test_estaciones_criticas(self) -> None:
        self.assertEqual(estaciones_criticas(GRAFO_EJEMPLO), ["B", "D"])

    def test_componentes_con_estacion_cerrada(self) -> None:
        componentes = componentes_con_estacion_cerrada(GRAFO_EJEMPLO, "B")
        self.assertEqual(componentes, [["A", "C"], ["D", "E", "F"]])

    def test_analizar_cierre(self) -> None:
        resultado = analizar_cierre(GRAFO_EJEMPLO, "D")
        self.assertTrue(resultado["es_critica"])
        self.assertEqual(resultado["numero_componentes"], 2)


if __name__ == "__main__":
    unittest.main()
