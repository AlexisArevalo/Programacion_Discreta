"""Punto de entrada del proyecto.

Por ahora se expone el primer ejercicio: cifrado César.
"""

from __future__ import annotations

from src.criptografia.cesar import procesar_cesar


def main() -> None:
    """Interfaz mínima por consola para el ejercicio 1."""
    print("Taller 3 - Programacion Discreta")
    print("Ejercicio 1: Cifrado Cesar")
    print("1) Cifrar")
    print("2) Descifrar")

    opcion = input("Seleccione una opcion (1/2): ").strip()
    texto = input("Ingrese el texto: ")
    desplazamiento = int(input("Ingrese el desplazamiento: "))

    if opcion == "1":
        resultado = procesar_cesar(texto, desplazamiento, "cifrar")
    elif opcion == "2":
        resultado = procesar_cesar(texto, desplazamiento, "descifrar")
    else:
        raise ValueError("Opcion no valida. Use 1 o 2.")

    print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()
