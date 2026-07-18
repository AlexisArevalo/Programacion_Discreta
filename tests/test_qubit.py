"""Pruebas para qubit."""

import unittest

from src.cuantica.qubit import (
    aplicar_puerta_h,
    aplicar_puerta_x,
    crear_qubit,
    ket_0,
    ket_1,
    probabilidades,
    resumen_qubit,
    superposicion,
)


class TestQubit(unittest.TestCase):
    def test_estados_base(self) -> None:
        self.assertEqual(ket_0().alpha, 1 + 0j)
        self.assertEqual(ket_1().beta, 1 + 0j)

    def test_puerta_x_intercambia_amplitudes(self) -> None:
        self.assertEqual(aplicar_puerta_x(ket_0()), ket_1())

    def test_puerta_h_crea_superposicion(self) -> None:
        qubit = aplicar_puerta_h(ket_0())
        self.assertAlmostEqual(abs(qubit.alpha) ** 2, 0.5)
        self.assertAlmostEqual(abs(qubit.beta) ** 2, 0.5)

    def test_probabilidades_y_resumen(self) -> None:
        qubit = superposicion()
        probs = probabilidades(qubit)
        self.assertAlmostEqual(probs["0"], 0.5)
        self.assertAlmostEqual(probs["1"], 0.5)
        resumen = resumen_qubit(qubit)
        self.assertIn("medicion", resumen)

    def test_crear_qubit_normalizado(self) -> None:
        qubit = crear_qubit(1 + 0j, 0 + 0j)
        self.assertEqual(qubit, ket_0())


if __name__ == "__main__":
    unittest.main()
