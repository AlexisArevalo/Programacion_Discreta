"""Punto de entrada del proyecto.

Por ahora se exponen los ejercicios 1, 2 y 3: César, RSA y MPC.
"""

from __future__ import annotations

from src.criptografia.cesar import procesar_cesar
from src.criptografia.mpc import ejecutar_mpc
from src.criptografia.rsa import cifrar_texto, descifrar_texto, generar_claves


def _leer_enteros_separados(texto: str) -> list[int]:
    """Convierte una cadena de números separados por comas en una lista."""
    return [int(parte.strip()) for parte in texto.split(",") if parte.strip()]


def main() -> None:
    """Interfaz mínima por consola para los ejercicios 1, 2 y 3."""
    print("Taller 3 - Programacion Discreta")
    print("1) Cifrado Cesar")
    print("2) RSA")
    print("3) MPC")
    print("4) Salir")

    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        print("Ejercicio 1: Cifrado Cesar")
        print("1) Cifrar")
        print("2) Descifrar")

        modo = input("Seleccione una opcion (1/2): ").strip()
        texto = input("Ingrese el texto: ")
        desplazamiento = int(input("Ingrese el desplazamiento: "))

        if modo == "1":
            resultado = procesar_cesar(texto, desplazamiento, "cifrar")
        elif modo == "2":
            resultado = procesar_cesar(texto, desplazamiento, "descifrar")
        else:
            raise ValueError("Opcion no valida. Use 1 o 2.")

        print(f"Resultado: {resultado}")
        return

    if opcion == "2":
        print("Ejercicio 2: RSA")
        p = int(input("Ingrese el primo p: "))
        q = int(input("Ingrese el primo q: "))
        e_texto = input("Ingrese e (opcional, presione Enter para automatico): ").strip()
        e = int(e_texto) if e_texto else None

        clave_publica, clave_privada = generar_claves(p, q, e)
        print(f"Clave publica: {clave_publica}")
        print(f"Clave privada: {clave_privada}")

        print("1) Cifrar texto")
        print("2) Descifrar bloques")
        modo = input("Seleccione una opcion (1/2): ").strip()

        if modo == "1":
            texto = input("Ingrese el texto ASCII a cifrar: ")
            cifrado = cifrar_texto(texto, clave_publica)
            print(f"Bloques cifrados: {cifrado}")
            return

        if modo == "2":
            bloques = _leer_enteros_separados(input("Ingrese los bloques separados por coma: "))
            texto = descifrar_texto(bloques, clave_privada)
            print(f"Texto descifrado: {texto}")
            return

        raise ValueError("Opcion no valida. Use 1 o 2.")

    if opcion == "3":
        print("Ejercicio 3: MPC")
        valores = _leer_enteros_separados(input("Ingrese los valores separados por coma: "))
        num_participantes = int(input("Ingrese el numero de participantes: "))
        modulo_texto = input("Ingrese el modulo opcional (Enter para omitir): ").strip()
        modulo = int(modulo_texto) if modulo_texto else None

        resultado = ejecutar_mpc(valores, num_participantes=num_participantes, modulo=modulo)
        print(f"Resultado MPC: {resultado}")
        return

    if opcion == "4":
        print("Salida solicitada.")
        return

    raise ValueError("Opcion no valida. Use 1, 2, 3 o 4.")


if __name__ == "__main__":
    main()
