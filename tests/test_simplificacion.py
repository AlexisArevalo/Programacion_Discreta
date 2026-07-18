"""Pruebas para simplificacion booleana."""

import unittest

from src.boole.simplificacion import forma_normal_conjuntiva, forma_normal_disyuntiva, resumen_simplificacion, simplificar_sop


class TestSimplificacion(unittest.TestCase):
    def test_formas_canonicas(self) -> None:
        fdn = forma_normal_disyuntiva("a and b")
        fcn = forma_normal_conjuntiva("a and b")
        self.assertIn("a", fdn)
        self.assertIn("a", fcn)

    def test_simplificar_sop(self) -> None:
        self.assertEqual(simplificar_sop("a or (a and b)"), "(a)")

    def test_resumen(self) -> None:
        resumen = resumen_simplificacion("a and b")
        self.assertIn("simplificada", resumen)


if __name__ == "__main__":
    unittest.main()
