"""Pruebas para Shannon."""

import unittest

from src.boole.shannon import entropia_desde_frecuencias, entropia_shannon, probabilidad_desde_frecuencias, resumen_shannon


class TestShannon(unittest.TestCase):
    def test_entropia_basica(self) -> None:
        self.assertAlmostEqual(entropia_shannon([0.5, 0.5]), 1.0)

    def test_probabilidades_desde_frecuencias(self) -> None:
        self.assertEqual(probabilidad_desde_frecuencias([2, 2]), [0.5, 0.5])

    def test_entropia_desde_frecuencias(self) -> None:
        self.assertAlmostEqual(entropia_desde_frecuencias([1, 1, 2]), 1.5)

    def test_resumen(self) -> None:
        resumen = resumen_shannon([0.25, 0.75])
        self.assertIn("entropia", resumen)


if __name__ == "__main__":
    unittest.main()
