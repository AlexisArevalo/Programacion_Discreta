"""Pruebas para el cifrado César."""

import unittest

from src.criptografia.cesar import cifrar_cesar, descifrar_cesar, procesar_cesar


class TestCesar(unittest.TestCase):
    def test_cifrado_basico(self) -> None:
        self.assertEqual(cifrar_cesar("ABC", 3), "DEF")

    def test_cifrado_con_salto_y_signos(self) -> None:
        self.assertEqual(cifrar_cesar("Hola, mundo!", 5), "Mtqf, rzsit!")

    def test_descifrado_y_desplazamiento_negativo(self) -> None:
        cifrado = cifrar_cesar("Programacion", 29)
        self.assertEqual(cifrado, "Surjudpdflrq")
        self.assertEqual(descifrar_cesar(cifrado, 29), "Programacion")
        self.assertEqual(procesar_cesar("ABC", -3, "cifrar"), "XYZ")


if __name__ == "__main__":
    unittest.main()
