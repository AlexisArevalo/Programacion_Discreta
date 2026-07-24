"""Pruebas para cierre de estación."""

import unittest

from src.grafos.cierre_estacion import (
    analizar_cierre,
    analizar_impacto_cierre,
    componentes_con_estacion_cerrada,
    estaciones_criticas,
)


GRAFO_EJEMPLO = {
    "A": {"B": 1, "C": 1},
    "B": {"A": 1, "C": 1, "D": 1},
    "C": {"A": 1, "B": 1},
    "D": {"B": 1, "E": 1, "F": 1},
    "E": {"D": 1, "F": 1},
    "F": {"D": 1, "E": 1},
}

GRAFO_IMPACTO = {
    "A": {"B": 1, "C": 1},
    "B": {"A": 1, "C": 1, "E": 5},
    "C": {"A": 1, "B": 1, "D": 1, "F": 5},
    "D": {"C": 1, "E": 1, "F": 1},
    "E": {"B": 5, "D": 1, "F": 1},
    "F": {"C": 5, "D": 1, "E": 1},
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

    def test_analizar_impacto_cierre(self) -> None:
        pares = [("A", "D"), ("A", "E"), ("A", "F"), ("B", "D"), ("B", "F"), ("C", "E")]
        resultado = analizar_impacto_cierre(GRAFO_IMPACTO, "D", pares)

        self.assertEqual(resultado["estacion_cerrada"], "D")
        self.assertEqual(resultado["pares_con_aumento"], [("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")])
        self.assertEqual(resultado["pares_desconectados"], [("A", "D"), ("B", "D")])

        tabla = resultado["tabla"]
        self.assertEqual(tabla[0]["estado"], "desconectado")
        self.assertEqual(tabla[1]["distancia_antes"], 3.0)
        self.assertEqual(tabla[1]["distancia_despues"], 6.0)
        self.assertEqual(tabla[1]["estado"], "aumento")
        self.assertEqual(tabla[3]["estado"], "desconectado")
        self.assertEqual(tabla[4]["distancia_despues"], 6.0)
        self.assertEqual(tabla[5]["estado"], "aumento")


if __name__ == "__main__":
    unittest.main()
