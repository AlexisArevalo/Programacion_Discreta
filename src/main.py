"""Punto de entrada del proyecto.

Agrupa la ejecucion de todos los ejercicios del taller.
"""

from __future__ import annotations

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from time import sleep
from typing import List

from src.boole.shannon import resumen_shannon
from src.boole.simplificacion import resumen_simplificacion
from src.boole.tablas_verdad import resumen_tabla_verdad
from src.cuantica.qubit import (
    aplicar_puerta_h,
    aplicar_puerta_x,
    ket_0,
    ket_1,
    resumen_qubit,
    superposicion,
)
from src.criptografia.cesar import procesar_cesar
from src.criptografia.mpc import ejecutar_mpc
from src.criptografia.rsa import cifrar_texto, descifrar_texto, generar_claves
from src.grafos.cierre_estacion import analizar_cierre
from src.grafos.coloreo import resumen_coloreo
from src.grafos.dijkstra import camino_mas_corto, cargar_grafo_desde_json


GRAFO_CIUDAD = "data/grafo_ciudad.json"
ANCHO_MENU = 58
RETRASO_LETRA = 0.01
RETRASO_LINEA = 0.05


def _imprimir_lento(texto: str, salto: bool = True, retraso: float = RETRASO_LETRA) -> None:
    """Imprime texto caracter por caracter para dar efecto de escritura."""
    for caracter in texto:
        print(caracter, end="", flush=True)
        sleep(retraso)
    if salto:
        print()


def _linea() -> str:
    return "=" * ANCHO_MENU


def _separador() -> str:
    return "-" * ANCHO_MENU


def _vaciar_pantalla() -> None:
    """Separa visualmente cada pantalla sin depender del sistema operativo."""
    print("\n" * 2)


def _mostrar_titulo(titulo: str, subtitulo: str = "") -> None:
    """Muestra un encabezado visual para cada menu o submenu."""
    _vaciar_pantalla()
    print(_linea())
    _imprimir_lento("TALLER 3 - PROGRAMACION DISCRETA", retraso=RETRASO_LETRA)
    print(_separador())
    _imprimir_lento(titulo, retraso=RETRASO_LETRA)
    if subtitulo:
        _imprimir_lento(subtitulo, retraso=RETRASO_LETRA)
    print(_linea())
    print()


def _mostrar_opcion(numero: str, texto: str) -> None:
    """Imprime una opcion de menu con espaciado consistente."""
    _imprimir_lento("  %s) %s" % (numero, texto), retraso=RETRASO_LETRA)


def _esperar_continuar() -> None:
    """Pausa corta entre pantallas para mejorar la lectura."""
    print()
    sleep(RETRASO_LINEA)


def _leer_enteros_separados(texto: str) -> List[int]:
    """Convierte una cadena de numeros separados por comas en una lista."""
    return [int(parte.strip()) for parte in texto.split(",") if parte.strip()]


def _mostrar_menu_principal() -> None:
    _mostrar_titulo("MENU PRINCIPAL", "Seleccione una opcion:")
    _mostrar_opcion("1", "Cifrado Cesar")
    _mostrar_opcion("2", "RSA")
    _mostrar_opcion("3", "MPC")
    _mostrar_opcion("4", "Dijkstra")
    _mostrar_opcion("5", "Cierre de estacion")
    _mostrar_opcion("6", "Coloreo de grafos")
    _mostrar_opcion("7", "Qubit")
    _mostrar_opcion("8", "Algebra de Boole")
    _mostrar_opcion("9", "Salir")
    print()


def _preguntar_continuacion() -> str:
    """Permite repetir el ejercicio, volver al menu principal o salir."""
    print()
    print(_separador())
    _imprimir_lento("Desea continuar?", retraso=RETRASO_LETRA)
    _mostrar_opcion("1", "Repetir ejercicio")
    _mostrar_opcion("2", "Volver al menu principal")
    _mostrar_opcion("9", "Salir")
    print()
    return input("Seleccione una opcion: ").strip()


def _ejecutar_cesar() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 1", "CIFRADO CESAR")
        _mostrar_opcion("1", "Cifrar")
        _mostrar_opcion("2", "Descifrar")
        _mostrar_opcion("0", "Volver al menu principal")
        print()

        modo = input("Seleccione una opcion: ").strip()
        if modo == "0":
            return

        if modo not in ("1", "2"):
            print("Opcion no valida. Use 0, 1 o 2.")
            _esperar_continuar()
            continue

        texto = input("Ingrese el texto: ")
        desplazamiento = int(input("Ingrese el desplazamiento: "))

        if modo == "1":
            resultado = procesar_cesar(texto, desplazamiento, "cifrar")
        else:
            resultado = procesar_cesar(texto, desplazamiento, "descifrar")

        print("Resultado: %s" % resultado)

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_rsa() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 2", "RSA")
        p = int(input("Ingrese el primo p: "))
        q = int(input("Ingrese el primo q: "))
        e_texto = input("Ingrese e (opcional, presione Enter para automatico): ").strip()
        e = int(e_texto) if e_texto else None

        clave_publica, clave_privada = generar_claves(p, q, e)
        print("Clave publica: %s" % (clave_publica,))
        print("Clave privada: %s" % (clave_privada,))

        while True:
            print()
            _mostrar_opcion("1", "Cifrar texto")
            _mostrar_opcion("2", "Descifrar bloques")
            _mostrar_opcion("0", "Volver al menu principal")
            print()
            modo = input("Seleccione una opcion: ").strip()

            if modo == "0":
                return

            if modo == "1":
                texto = input("Ingrese el texto ASCII a cifrar: ")
                cifrado = cifrar_texto(texto, clave_publica)
                print("Bloques cifrados: %s" % cifrado)
            elif modo == "2":
                bloques = _leer_enteros_separados(input("Ingrese los bloques separados por coma: "))
                texto = descifrar_texto(bloques, clave_privada)
                print("Texto descifrado: %s" % texto)
            else:
                print("Opcion no valida. Use 0, 1 o 2.")
                _esperar_continuar()
                continue

            opcion = _preguntar_continuacion()
            if opcion == "1":
                continue
            if opcion == "2":
                return
            if opcion == "9":
                raise SystemExit(0)
            print("Opcion no valida. Volviendo al menu principal.")
            return


def _ejecutar_mpc() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 3", "MPC")
        valores = _leer_enteros_separados(input("Ingrese los valores separados por coma: "))
        num_participantes = int(input("Ingrese el numero de participantes: "))
        modulo_texto = input("Ingrese el modulo opcional (Enter para omitir): ").strip()
        modulo = int(modulo_texto) if modulo_texto else None

        resultado = ejecutar_mpc(valores, num_participantes=num_participantes, modulo=modulo)
        print("Resultado MPC: %s" % resultado)

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_dijkstra() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 4", "DIJKSTRA")
        grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        origen = input("Ingrese el nodo origen: ").strip()
        destino = input("Ingrese el nodo destino: ").strip()

        distancia, camino = camino_mas_corto(grafo, origen, destino)
        print("Distancia minima: %s" % distancia)
        print("Camino: %s" % " -> ".join(camino))

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_cierre_estacion() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 5", "CIERRE DE ESTACION")
        grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        estacion = input("Ingrese la estacion a evaluar: ").strip()

        resultado = analizar_cierre(grafo, estacion)
        print("Estacion critica: %s" % ("si" if resultado["es_critica"] else "no"))
        print("Estaciones criticas: %s" % resultado["estaciones_criticas"])
        print("Componentes restantes: %s" % resultado["componentes_restantes"])
        print("Numero de componentes: %s" % resultado["numero_componentes"])

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_coloreo() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 6", "COLOREO DE GRAFOS")
        grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        resultado = resumen_coloreo(grafo)
        print("Coloreo: %s" % resultado["colores"])
        print("Numero de colores: %s" % resultado["numero_colores"])
        print("Coloreo valido: %s" % ("si" if resultado["es_valido"] else "no"))

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_qubit() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 7", "QUBIT")
        _mostrar_opcion("1", "Estado |0>")
        _mostrar_opcion("2", "Estado |1>")
        _mostrar_opcion("3", "Superposicion")
        _mostrar_opcion("4", "Aplicar puerta X a |0>")
        _mostrar_opcion("5", "Aplicar puerta H a |0>")
        _mostrar_opcion("0", "Volver al menu principal")
        print()

        modo = input("Seleccione una opcion: ").strip()
        if modo == "0":
            return
        if modo == "1":
            print("Resumen: %s" % resumen_qubit(ket_0()))
        elif modo == "2":
            print("Resumen: %s" % resumen_qubit(ket_1()))
        elif modo == "3":
            print("Resumen: %s" % resumen_qubit(superposicion()))
        elif modo == "4":
            print("Resumen: %s" % resumen_qubit(aplicar_puerta_x(ket_0())))
        elif modo == "5":
            print("Resumen: %s" % resumen_qubit(aplicar_puerta_h(ket_0())))
        else:
            print("Opcion no valida. Use 0, 1, 2, 3, 4 o 5.")
            _esperar_continuar()
            continue

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def _ejecutar_boole() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 8", "ALGEBRA DE BOOLE")
        _mostrar_opcion("1", "Tabla de verdad")
        _mostrar_opcion("2", "Simplificacion booleana")
        _mostrar_opcion("3", "Entropia de Shannon")
        _mostrar_opcion("0", "Volver al menu principal")
        print()

        modo = input("Seleccione una opcion: ").strip()
        if modo == "0":
            return
        if modo == "1":
            expresion = input("Ingrese la expresion booleana (use and/or/not o ^): ").strip()
            resultado = resumen_tabla_verdad(expresion)
            print("Variables: %s" % resultado["variables"])
            print("Filas: %s" % resultado["filas"])
            print("Verdaderos: %s" % resultado["verdaderos"])
            print("Falsos: %s" % resultado["falsos"])
        elif modo == "2":
            expresion = input("Ingrese la expresion booleana: ").strip()
            resultado = resumen_simplificacion(expresion)
            print("FDN: %s" % resultado["fdn"])
            print("FCN: %s" % resultado["fcn"])
            print("Simplificada: %s" % resultado["simplificada"])
        elif modo == "3":
            frecuencias = _leer_enteros_separados(input("Ingrese las frecuencias separadas por coma: "))
            total = sum(frecuencias)
            if total <= 0:
                raise ValueError("La suma de frecuencias debe ser mayor que 0.")
            probabilidades = [float(f) / total for f in frecuencias]
            resultado = resumen_shannon(probabilidades)
            print("Probabilidades: %s" % resultado["probabilidades"])
            print("Entropia: %s" % resultado["entropia"])
        else:
            print("Opcion no valida. Use 0, 1, 2 o 3.")
            _esperar_continuar()
            continue

        opcion = _preguntar_continuacion()
        if opcion == "1":
            continue
        if opcion == "2":
            return
        if opcion == "9":
            raise SystemExit(0)
        print("Opcion no valida. Volviendo al menu principal.")
        return


def main() -> None:
    """Interfaz minima por consola para todos los ejercicios."""
    while True:
        _mostrar_menu_principal()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            _ejecutar_cesar()
        elif opcion == "2":
            _ejecutar_rsa()
        elif opcion == "3":
            _ejecutar_mpc()
        elif opcion == "4":
            _ejecutar_dijkstra()
        elif opcion == "5":
            _ejecutar_cierre_estacion()
        elif opcion == "6":
            _ejecutar_coloreo()
        elif opcion == "7":
            _ejecutar_qubit()
        elif opcion == "8":
            _ejecutar_boole()
        elif opcion == "9":
            print("Salida solicitada.")
            return
        else:
            print("Opcion no valida. Use 1, 2, 3, 4, 5, 6, 7, 8 o 9.")
            continue


if __name__ == "__main__":
    main()
