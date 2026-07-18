"""Pruebas para Dijkstra."""

import tempfile
import unittest
from pathlib import Path

from src.grafos.dijkstra import (
    camino_mas_corto,
    cargar_grafo_desde_json,
    dijkstra,
    reconstruir_camino,
)


GRAFO_EJEMPLO = {
    "A": {"B": 4, "C": 2},
    "B": {"C": 1, "D": 5},
    "C": {"B": 1, "D": 8},
    "D": {},
}


class TestDijkstra(unittest.TestCase):
    def test_calcula_distancias_minimas(self) -> None:
        distancias, predecesores = dijkstra(GRAFO_EJEMPLO, "A")
        self.assertEqual(distancias["A"], 0.0)
        self.assertEqual(distancias["B"], 3.0)
        self.assertEqual(distancias["D"], 8.0)
        self.assertEqual(predecesores["B"], "C")

    def test_reconstruye_camino(self) -> None:
        _, predecesores = dijkstra(GRAFO_EJEMPLO, "A")
        self.assertEqual(reconstruir_camino(predecesores, "A", "D"), ["A", "C", "B", "D"])

    def test_camino_mas_corto(self) -> None:
        distancia, camino = camino_mas_corto(GRAFO_EJEMPLO, "A", "D")
        self.assertEqual(distancia, 8.0)
        self.assertEqual(camino, ["A", "C", "B", "D"])

    def test_carga_grafo_desde_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ruta = Path(tmpdir) / "grafo.json"
            ruta.write_text('{"X": {"Y": 7}, "Y": {"X": 7}}', encoding="utf-8")

            grafo = cargar_grafo_desde_json(ruta)
            self.assertEqual(grafo["X"]["Y"], 7.0)


if __name__ == "__main__":
    unittest.main()
