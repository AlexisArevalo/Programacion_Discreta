"""Punto de entrada del proyecto.

Agrupa la ejecucion de todos los ejercicios del taller.
"""

from __future__ import annotations

from pathlib import Path

if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from time import sleep
from typing import List, Optional

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


GRAFO_CIUDAD = Path(__file__).resolve().parent.parent / "data" / "grafo_ciudad.json"
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


def _pedir_opcion(mensaje: str, opciones_validas: List[str]) -> str:
    """Pide una opcion hasta que el usuario ingrese una valida."""
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print("Entrada invalida. Opciones validas: %s" % ", ".join(opciones_validas))


def _pedir_entero(mensaje: str, minimo: int = None) -> int:
    """Pide un entero validando formato y rango."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
        except ValueError:
            print("Se espera un numero entero.")
            continue

        if minimo is not None and numero < minimo:
            print("Se espera un numero mayor o igual a %s." % minimo)
            continue
        return numero


def _pedir_entero_opcional(mensaje: str, minimo: int = None) -> Optional[int]:
    """Pide un entero opcional; Enter devuelve None."""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return None
        try:
            numero = int(valor)
        except ValueError:
            print("Se espera un numero entero o Enter para omitir.")
            continue
        if minimo is not None and numero < minimo:
            print("Se espera un numero mayor o igual a %s." % minimo)
            continue
        return numero


def _pedir_texto_no_vacio(mensaje: str) -> str:
    """Pide texto no vacio."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Se espera un texto no vacio.")


def _pedir_lista_enteros(mensaje: str, minimo: int = None) -> List[int]:
    """Pide una lista de enteros separados por coma."""
    while True:
        texto = input(mensaje).strip()
        try:
            valores = _leer_enteros_separados(texto)
        except ValueError:
            print("Se esperan numeros separados por coma.")
            continue
        if not valores:
            print("Se espera al menos un numero.")
            continue
        if minimo is not None and any(valor < minimo for valor in valores):
            print("Todos los numeros deben ser mayores o iguales a %s." % minimo)
            continue
        return valores


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
    return _pedir_opcion("Seleccione una opcion: ", ["1", "2", "9"])


def _ejecutar_cesar() -> None:
    while True:
        _mostrar_titulo("EJERCICIO 1", "CIFRADO CESAR")
        _mostrar_opcion("1", "Cifrar")
        _mostrar_opcion("2", "Descifrar")
        _mostrar_opcion("0", "Volver al menu principal")
        print()

        modo = _pedir_opcion("Seleccione una opcion: ", ["0", "1", "2"])
        if modo == "0":
            return

        texto = _pedir_texto_no_vacio("Ingrese el texto: ")
        desplazamiento = _pedir_entero("Ingrese el desplazamiento: ")

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
        p = _pedir_entero("Ingrese el primo p: ", minimo=2)
        q = _pedir_entero("Ingrese el primo q: ", minimo=2)
        e = _pedir_entero_opcional("Ingrese e (opcional, presione Enter para automatico): ", minimo=2)

        try:
            clave_publica, clave_privada = generar_claves(p, q, e)
        except ValueError as exc:
            print("No se pudieron generar las claves: %s" % exc)
            _esperar_continuar()
            continue
        print("Clave publica: %s" % (clave_publica,))
        print("Clave privada: %s" % (clave_privada,))

        while True:
            print()
            _mostrar_opcion("1", "Cifrar texto")
            _mostrar_opcion("2", "Descifrar bloques")
            _mostrar_opcion("0", "Volver al menu principal")
            print()
            modo = _pedir_opcion("Seleccione una opcion: ", ["0", "1", "2"])

            if modo == "0":
                return

            if modo == "1":
                texto = _pedir_texto_no_vacio("Ingrese el texto ASCII a cifrar: ")
                try:
                    cifrado = cifrar_texto(texto, clave_publica)
                except ValueError as exc:
                    print("No se pudo cifrar el texto: %s" % exc)
                    _esperar_continuar()
                    continue
                print("Bloques cifrados: %s" % cifrado)
            elif modo == "2":
                bloques = _pedir_lista_enteros("Ingrese los bloques separados por coma: ", minimo=0)
                try:
                    texto = descifrar_texto(bloques, clave_privada)
                except ValueError as exc:
                    print("No se pudo descifrar el mensaje: %s" % exc)
                    _esperar_continuar()
                    continue
                print("Texto descifrado: %s" % texto)

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
        valores = _pedir_lista_enteros("Ingrese los valores separados por coma: ")
        num_participantes = _pedir_entero("Ingrese el numero de participantes: ", minimo=2)
        modulo = _pedir_entero_opcional("Ingrese el modulo opcional (Enter para omitir): ", minimo=1)

        try:
            resultado = ejecutar_mpc(valores, num_participantes=num_participantes, modulo=modulo)
        except ValueError as exc:
            print("No se pudo ejecutar MPC: %s" % exc)
            _esperar_continuar()
            continue
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
        try:
            grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo cargar el grafo: %s" % exc)
            _esperar_continuar()
            return

        origen = _pedir_texto_no_vacio("Ingrese el nodo origen: ")
        destino = _pedir_texto_no_vacio("Ingrese el nodo destino: ")

        try:
            distancia, camino = camino_mas_corto(grafo, origen, destino)
        except (KeyError, ValueError) as exc:
            print("No se pudo calcular el camino: %s" % exc)
            _esperar_continuar()
            continue
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
        try:
            grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo cargar el grafo: %s" % exc)
            _esperar_continuar()
            return
        estacion = _pedir_texto_no_vacio("Ingrese la estacion a evaluar: ")

        try:
            resultado = analizar_cierre(grafo, estacion)
        except (KeyError, ValueError, TypeError) as exc:
            print("No se pudo analizar la estacion: %s" % exc)
            _esperar_continuar()
            continue
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
        try:
            grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
            resultado = resumen_coloreo(grafo)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo analizar el grafo: %s" % exc)
            _esperar_continuar()
            return
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

        modo = _pedir_opcion("Seleccione una opcion: ", ["0", "1", "2", "3", "4", "5"])
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

        modo = _pedir_opcion("Seleccione una opcion: ", ["0", "1", "2", "3"])
        if modo == "0":
            return
        if modo == "1":
            expresion = _pedir_texto_no_vacio("Ingrese la expresion booleana (use and/or/not o ^): ")
            try:
                resultado = resumen_tabla_verdad(expresion)
            except Exception as exc:
                print("No se pudo evaluar la expresion: %s" % exc)
                _esperar_continuar()
                continue
            print("Variables: %s" % resultado["variables"])
            print("Filas: %s" % resultado["filas"])
            print("Verdaderos: %s" % resultado["verdaderos"])
            print("Falsos: %s" % resultado["falsos"])
        elif modo == "2":
            expresion = _pedir_texto_no_vacio("Ingrese la expresion booleana: ")
            try:
                resultado = resumen_simplificacion(expresion)
            except Exception as exc:
                print("No se pudo simplificar la expresion: %s" % exc)
                _esperar_continuar()
                continue
            print("FDN: %s" % resultado["fdn"])
            print("FCN: %s" % resultado["fcn"])
            print("Simplificada: %s" % resultado["simplificada"])
        elif modo == "3":
            frecuencias = _pedir_lista_enteros("Ingrese las frecuencias separadas por coma: ", minimo=0)
            try:
                total = sum(frecuencias)
                if total <= 0:
                    print("La suma de frecuencias debe ser mayor que 0.")
                    _esperar_continuar()
                    continue
                resultado = resumen_shannon([float(f) / total for f in frecuencias])
            except ZeroDivisionError:
                print("La suma de frecuencias debe ser mayor que 0.")
                _esperar_continuar()
                continue
            except ValueError as exc:
                print("No se pudo calcular Shannon: %s" % exc)
                _esperar_continuar()
                continue
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
        opcion = _pedir_opcion("Seleccione una opcion: ", ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

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
