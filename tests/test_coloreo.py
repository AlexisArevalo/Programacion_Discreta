"""Pruebas para coloreo de grafos."""

import unittest

from src.grafos.coloreo import colorear_grafo, numero_cromatico_aproximado, resumen_coloreo, verificar_coloreo
from src.grafos.dijkstra import cargar_grafo_desde_json


GRAFO_EJEMPLO = {
    "A": {"B": 1, "C": 1},
    "B": {"A": 1, "C": 1, "D": 1},
    "C": {"A": 1, "B": 1, "D": 1},
    "D": {"B": 1, "C": 1},
}

GRAFO_EXAMENES = cargar_grafo_desde_json("data/grafo_coloreo.json")


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

    def test_coloreo_con_mas_de_diez_vertices(self) -> None:
        resultado = resumen_coloreo(GRAFO_EXAMENES)
        self.assertTrue(resultado["es_valido"])
        self.assertGreaterEqual(len(GRAFO_EXAMENES), 10)
        self.assertEqual(sum(len(vertices) for vertices in resultado["vertices_por_color"].values()), len(GRAFO_EXAMENES))
        self.assertGreaterEqual(resultado["numero_colores"], 1)


if __name__ == "__main__":
    unittest.main()
