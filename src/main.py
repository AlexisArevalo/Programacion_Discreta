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
from src.criptografia.mpc import ejecutar_mpc, simular_mpc
from src.criptografia.rsa import cifrar_numero, descifrar_numero, generar_claves
from src.grafos.cierre_estacion import analizar_impacto_cierre
from src.grafos.coloreo import resumen_coloreo
from src.grafos.dijkstra import camino_mas_corto, cargar_grafo_desde_json


GRAFO_CIUDAD = Path(__file__).resolve().parent.parent / "data" / "grafo_ciudad.json"
GRAFO_CIERRE = Path(__file__).resolve().parent.parent / "data" / "grafo_cierre.json"
GRAFO_COLOREO = Path(__file__).resolve().parent.parent / "data" / "grafo_coloreo.json"
ANCHO_MENU = 58
RETRASO_LETRA = 0.01
RETRASO_LINEA = 0.05
RETRASO_RESULTADO = 0.25


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
    print()


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


def _mostrar_resultado(lineas) -> None:
    """Imprime resultados con pausas para facilitar la lectura."""
    if isinstance(lineas, str):
        lineas = [lineas]

    print()
    for indice, linea in enumerate(lineas):
        _imprimir_lento(linea, retraso=RETRASO_LETRA)
        if indice < len(lineas) - 1:
            sleep(RETRASO_RESULTADO)
    print()
    sleep(RETRASO_LINEA)


def _formatear_distancia(valor: Optional[float]) -> str:
    """Convierte distancias para mostrarlas en tabla."""
    if valor is None:
        return "-"
    if valor == float("inf"):
        return "sin camino"
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def _mostrar_grafo_ascii(grafo) -> None:
    """Muestra una vista simple del grafo en consola."""
    aristas = set()
    lineas = ["Nodos disponibles: %s" % ", ".join(sorted(grafo.keys())), "", "Conexiones:"]

    for origen, vecinos in sorted(grafo.items()):
        adyacencias = []
        for destino, peso in sorted(vecinos.items()):
            arista = tuple(sorted((origen, destino))) + (peso,)
            if arista in aristas:
                continue
            aristas.add(arista)
            adyacencias.append("%s(%s)" % (destino, _formatear_distancia(peso)))
        if adyacencias:
            lineas.append("%s -> %s" % (origen, ", ".join(adyacencias)))
    _mostrar_resultado(lineas)


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
    _mostrar_opcion("2", "Criptografia RSA")
    _mostrar_opcion("3", "Computacion Multipartita Segura (MPC)")
    _mostrar_opcion("4", "Algoritmo de Dijkstra")
    _mostrar_opcion("5", "Cierre de estacion")
    _mostrar_opcion("6", "Coloreo de grafos")
    _mostrar_opcion("7", "Simulacion de qubit")
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

        _mostrar_resultado("Resultado: %s" % resultado)

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
        _mostrar_titulo("EJERCICIO 2", "CRIPTOGRAFIA RSA")
        p = _pedir_entero("Ingrese el primo p: ", minimo=2)
        q = _pedir_entero("Ingrese el primo q: ", minimo=2)
        e = _pedir_entero("Ingrese el exponente publico e: ", minimo=2)
        mensaje = _pedir_entero("Ingrese el mensaje entero M: ", minimo=0)

        try:
            clave_publica, clave_privada, n, phi = generar_claves(p, q, e)
        except ValueError as exc:
            print("No se pudieron generar las claves: %s" % exc)
            _esperar_continuar()
            continue
        _mostrar_resultado([
            "n = %s" % n,
            "phi(n) = %s" % phi,
            "Clave publica: %s" % (clave_publica,),
            "Clave privada: %s" % (clave_privada,),
        ])

        try:
            cifrado = cifrar_numero(mensaje, clave_publica)
            recuperado = descifrar_numero(cifrado, clave_privada)
        except ValueError as exc:
            print("No se pudo procesar el mensaje: %s" % exc)
            _esperar_continuar()
            continue

        _mostrar_resultado([
            "M = %s" % mensaje,
            "C = %s" % cifrado,
            "M recuperado = %s" % recuperado,
        ])

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
        _mostrar_titulo("EJERCICIO 3", "COMPUTACION MULTIPARTITA SEGURA")
        notas = _pedir_lista_enteros("Ingrese las notas separadas por coma (0 a 50): ", minimo=0)
        if any(nota > 50 for nota in notas):
            print("Cada nota debe estar entre 0 y 50.")
            _esperar_continuar()
            continue
        modulo = _pedir_entero_opcional("Ingrese el modulo opcional (Enter para usar 1000003): ", minimo=2)

        try:
            resultado = simular_mpc(notas, modulo=modulo)
        except ValueError as exc:
            print("No se pudo ejecutar MPC: %s" % exc)
            _esperar_continuar()
            continue
        pasos = resultado["pasos"]
        lineas = [
            "Modulo usado: %s" % resultado["modulo"],
            "",
            "Proceso de reparto por servidor:",
        ]
        for paso in pasos:
            lineas.append("Nota %s = %s" % (paso["numero_nota"], paso["nota"]))
            lineas.append(
                "  Servidor 1 recibe %s | Servidor 2 recibe %s | Servidor 3 recibe %s"
                % tuple(paso["partes"])
            )
            lineas.append(
                "  Acumulado S1=%s, S2=%s, S3=%s"
                % tuple(paso["acumulado_por_servidor"])
            )
            lineas.append("  Reconstruccion parcial = %s" % paso["suma_parcial"])
            lineas.append("")

        lineas.extend([
            "Reconstruccion final:",
            "  Suma total = %s" % resultado["suma_total"],
            "  Promedio = %s" % resultado["promedio"],
        ])
        _mostrar_resultado(lineas)

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
        _mostrar_titulo("EJERCICIO 4", "ALGORITMO DE DIJKSTRA")
        try:
            grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo cargar el grafo: %s" % exc)
            _esperar_continuar()
            return

        _mostrar_resultado([
            "Grafo de ciudad cargado.",
            "Nodos disponibles: %s" % ", ".join(sorted(grafo.keys())),
        ])
        _mostrar_grafo_ascii(grafo)

        origen = _pedir_texto_no_vacio("Nodo origen: ")
        destino = _pedir_texto_no_vacio("Nodo destino: ")

        if origen not in grafo or destino not in grafo:
            print("El origen y/o el destino no existen en el grafo.")
            _esperar_continuar()
            continue

        try:
            distancia, camino = camino_mas_corto(grafo, origen, destino)
        except (KeyError, ValueError) as exc:
            print("No se pudo calcular el camino: %s" % exc)
            _esperar_continuar()
            continue
        _mostrar_resultado([
            "Resultado de Dijkstra:",
            "  Distancia minima: %s" % distancia,
            "  Camino: %s" % " -> ".join(camino),
        ])

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
        _mostrar_titulo("EJERCICIO 5", "CIERRE DE UNA ESTACION")
        try:
            grafo = cargar_grafo_desde_json(GRAFO_CIERRE)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo cargar el grafo: %s" % exc)
            _esperar_continuar()
            return
        estacion = "D"
        pares = [
            ("A", "D"),
            ("A", "E"),
            ("A", "F"),
            ("B", "D"),
            ("B", "F"),
            ("C", "E"),
        ]

        try:
            resultado = analizar_impacto_cierre(grafo, estacion, pares)
        except (KeyError, ValueError, TypeError) as exc:
            print("No se pudo analizar el cierre: %s" % exc)
            _esperar_continuar()
            continue

        resumen = [
            "Estacion cerrada: %s" % resultado["estacion_cerrada"],
            "Pares comparados: %s" % len(resultado["tabla"]),
            "Se analiza el impacto sobre la red antes y despues del cierre.",
            "",
            "Tabla de impacto:",
        ]
        tabla = [
            "Origen   Destino   Antes      Despues   Dif.       Estado",
            "--------------------------------------------------------",
        ]
        for fila in resultado["tabla"]:
            diferencia = _formatear_distancia(fila["diferencia"])
            tabla.append(
                "%-8s %-8s %-10s %-10s %-10s %-12s"
                % (
                    fila["origen"],
                    fila["destino"],
                    _formatear_distancia(fila["distancia_antes"]),
                    _formatear_distancia(fila["distancia_despues"]),
                    diferencia,
                    fila["estado"],
                )
            )
        tabla.extend([
            "",
            "Pares con aumento: %s" % resultado["pares_con_aumento"],
            "Pares desconectados: %s" % resultado["pares_desconectados"],
        ])
        _mostrar_resultado(resumen + tabla)

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
            grafo = cargar_grafo_desde_json(GRAFO_COLOREO)
            if len(grafo) < 10:
                raise ValueError("El grafo de coloreo debe tener al menos 10 vertices.")
            resultado = resumen_coloreo(grafo)
        except (OSError, ValueError, TypeError) as exc:
            print("No se pudo analizar el grafo: %s" % exc)
            _esperar_continuar()
            return
        _mostrar_resultado([
            "Grafo de exámenes cargado con %s vertices." % len(grafo),
            "Coloreo: %s" % resultado["colores"],
            "Numero de colores: %s" % resultado["numero_colores"],
            "Coloreo valido: %s" % ("si" if resultado["es_valido"] else "no"),
            "Vertices por color: %s" % resultado["vertices_por_color"],
        ])

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
        _mostrar_titulo("EJERCICIO 7", "SIMULACION DE QUBIT")
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
            _mostrar_resultado("Resumen: %s" % resumen_qubit(ket_0()))
        elif modo == "2":
            _mostrar_resultado("Resumen: %s" % resumen_qubit(ket_1()))
        elif modo == "3":
            _mostrar_resultado("Resumen: %s" % resumen_qubit(superposicion()))
        elif modo == "4":
            _mostrar_resultado("Resumen: %s" % resumen_qubit(aplicar_puerta_x(ket_0())))
        elif modo == "5":
            _mostrar_resultado("Resumen: %s" % resumen_qubit(aplicar_puerta_h(ket_0())))
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
            _mostrar_resultado([
                "Variables: %s" % resultado["variables"],
                "Filas: %s" % resultado["filas"],
                "Verdaderos: %s" % resultado["verdaderos"],
                "Falsos: %s" % resultado["falsos"],
            ])
        elif modo == "2":
            expresion = _pedir_texto_no_vacio("Ingrese la expresion booleana: ")
            try:
                resultado = resumen_simplificacion(expresion)
            except Exception as exc:
                print("No se pudo simplificar la expresion: %s" % exc)
                _esperar_continuar()
                continue
            _mostrar_resultado([
                "FDN: %s" % resultado["fdn"],
                "FCN: %s" % resultado["fcn"],
                "Simplificada: %s" % resultado["simplificada"],
            ])
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
            _mostrar_resultado([
                "Probabilidades: %s" % resultado["probabilidades"],
                "Entropia: %s" % resultado["entropia"],
            ])
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
