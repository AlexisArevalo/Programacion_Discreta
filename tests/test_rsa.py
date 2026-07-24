"""Pruebas para RSA."""

import unittest

from src.criptografia.rsa import (
    cifrar_numero,
    descifrar_numero,
    es_primo,
    generar_claves,
    inverso_modular,
)


class TestRSA(unittest.TestCase):
    def test_identificacion_de_primos(self) -> None:
        self.assertTrue(es_primo(61))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(21))

    def test_inverso_modular(self) -> None:
        self.assertEqual(inverso_modular(17, 3120), 2753)

    def test_caso_obligatorio_del_enunciado(self) -> None:
        clave_publica, clave_privada, n, phi = generar_claves(61, 53, 17)
        mensaje = 65
        cifrado = cifrar_numero(mensaje, clave_publica)
        recuperado = descifrar_numero(cifrado, clave_privada)

        self.assertEqual(n, 3233)
        self.assertEqual(phi, 3120)
        self.assertEqual(clave_publica, (17, 3233))
        self.assertEqual(clave_privada, (2753, 3233))
        self.assertEqual(cifrado, 2790)
        self.assertEqual(recuperado, 65)

    def test_rechaza_primos_invalidos(self) -> None:
        with self.assertRaises(ValueError):
            generar_claves(15, 53, 17)

    def test_rechaza_exponente_no_valido(self) -> None:
        with self.assertRaises(ValueError):
            generar_claves(61, 53, 12)


if __name__ == "__main__":
    unittest.main()
