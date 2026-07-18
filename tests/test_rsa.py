"""Pruebas para RSA."""

import unittest

from src.criptografia.rsa import (
    cifrar_texto,
    descifrar_texto,
    es_primo,
    generar_claves,
)


class TestRSA(unittest.TestCase):
    def test_identificacion_de_primos(self) -> None:
        self.assertTrue(es_primo(61))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(21))

    def test_generacion_de_claves(self) -> None:
        clave_publica, clave_privada = generar_claves(61, 53, 17)
        self.assertEqual(clave_publica, (17, 3233))
        self.assertEqual(clave_privada, (2753, 3233))

    def test_cifrado_y_descifrado_de_texto(self) -> None:
        clave_publica, clave_privada = generar_claves(61, 53, 17)
        mensaje = "HOLA"
        cifrado = cifrar_texto(mensaje, clave_publica)

        self.assertEqual(len(cifrado), len(mensaje))
        self.assertEqual(descifrar_texto(cifrado, clave_privada), mensaje)

    def test_rechaza_primos_invalidos(self) -> None:
        with self.assertRaises(ValueError):
            generar_claves(15, 53, 17)


if __name__ == "__main__":
    unittest.main()
