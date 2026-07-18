"""Punto de entrada del proyecto.

Agrupa la ejecucion de todos los ejercicios del taller.
"""

from __future__ import annotations

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


def _leer_enteros_separados(texto: str) -> list[int]:
    """Convierte una cadena de numeros separados por comas en una lista."""
    return [int(parte.strip()) for parte in texto.split(",") if parte.strip()]


def _mostrar_menu_principal() -> None:
    print("Taller 3 - Programacion Discreta")
    print("1) Cifrado Cesar")
    print("2) RSA")
    print("3) MPC")
    print("4) Dijkstra")
    print("5) Cierre de estacion")
    print("6) Coloreo de grafos")
    print("7) Qubit")
    print("8) Algebra de Boole")
    print("9) Salir")


def _ejecutar_cesar() -> None:
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


def _ejecutar_rsa() -> None:
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


def _ejecutar_mpc() -> None:
    print("Ejercicio 3: MPC")
    valores = _leer_enteros_separados(input("Ingrese los valores separados por coma: "))
    num_participantes = int(input("Ingrese el numero de participantes: "))
    modulo_texto = input("Ingrese el modulo opcional (Enter para omitir): ").strip()
    modulo = int(modulo_texto) if modulo_texto else None

    resultado = ejecutar_mpc(valores, num_participantes=num_participantes, modulo=modulo)
    print(f"Resultado MPC: {resultado}")


def _ejecutar_dijkstra() -> None:
    print("Ejercicio 4: Dijkstra")
    grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
    origen = input("Ingrese el nodo origen: ").strip()
    destino = input("Ingrese el nodo destino: ").strip()

    distancia, camino = camino_mas_corto(grafo, origen, destino)
    print(f"Distancia minima: {distancia}")
    print(f"Camino: {' -> '.join(camino)}")


def _ejecutar_cierre_estacion() -> None:
    print("Ejercicio 5: Cierre de estacion")
    grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
    estacion = input("Ingrese la estacion a evaluar: ").strip()

    resultado = analizar_cierre(grafo, estacion)
    print(f"Estacion critica: {'si' if resultado['es_critica'] else 'no'}")
    print(f"Estaciones criticas: {resultado['estaciones_criticas']}")
    print(f"Componentes restantes: {resultado['componentes_restantes']}")
    print(f"Numero de componentes: {resultado['numero_componentes']}")


def _ejecutar_coloreo() -> None:
    print("Ejercicio 6: Coloreo de grafos")
    grafo = cargar_grafo_desde_json(GRAFO_CIUDAD)
    resultado = resumen_coloreo(grafo)
    print(f"Coloreo: {resultado['colores']}")
    print(f"Numero de colores: {resultado['numero_colores']}")
    print(f"Coloreo valido: {'si' if resultado['es_valido'] else 'no'}")


def _ejecutar_qubit() -> None:
    print("Ejercicio 7: Qubit")
    print("1) Estado |0>")
    print("2) Estado |1>")
    print("3) Superposicion")
    print("4) Aplicar puerta X a |0>")
    print("5) Aplicar puerta H a |0>")

    modo = input("Seleccione una opcion (1/2/3/4/5): ").strip()
    if modo == "1":
        print(f"Resumen: {resumen_qubit(ket_0())}")
        return
    if modo == "2":
        print(f"Resumen: {resumen_qubit(ket_1())}")
        return
    if modo == "3":
        print(f"Resumen: {resumen_qubit(superposicion())}")
        return
    if modo == "4":
        print(f"Resumen: {resumen_qubit(aplicar_puerta_x(ket_0()))}")
        return
    if modo == "5":
        print(f"Resumen: {resumen_qubit(aplicar_puerta_h(ket_0()))}")
        return

    raise ValueError("Opcion no valida. Use 1, 2, 3, 4 o 5.")


def _ejecutar_boole() -> None:
    print("Ejercicio 8: Algebra de Boole")
    print("1) Tabla de verdad")
    print("2) Simplificacion booleana")
    print("3) Entropia de Shannon")

    modo = input("Seleccione una opcion (1/2/3): ").strip()
    if modo == "1":
        expresion = input("Ingrese la expresion booleana (use and/or/not o ^): ").strip()
        resultado = resumen_tabla_verdad(expresion)
        print(f"Variables: {resultado['variables']}")
        print(f"Filas: {resultado['filas']}")
        print(f"Verdaderos: {resultado['verdaderos']}")
        print(f"Falsos: {resultado['falsos']}")
        return

    if modo == "2":
        expresion = input("Ingrese la expresion booleana: ").strip()
        resultado = resumen_simplificacion(expresion)
        print(f"FDN: {resultado['fdn']}")
        print(f"FCN: {resultado['fcn']}")
        print(f"Simplificada: {resultado['simplificada']}")
        return

    if modo == "3":
        frecuencias = _leer_enteros_separados(input("Ingrese las frecuencias separadas por coma: "))
        total = sum(frecuencias)
        if total <= 0:
            raise ValueError("La suma de frecuencias debe ser mayor que 0.")
        probabilidades = [f / total for f in frecuencias]
        resultado = resumen_shannon(probabilidades)
        print(f"Probabilidades: {resultado['probabilidades']}")
        print(f"Entropia: {resultado['entropia']}")
        return

    raise ValueError("Opcion no valida. Use 1, 2 o 3.")


def main() -> None:
    """Interfaz minima por consola para todos los ejercicios."""
    _mostrar_menu_principal()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        _ejecutar_cesar()
        return
    if opcion == "2":
        _ejecutar_rsa()
        return
    if opcion == "3":
        _ejecutar_mpc()
        return
    if opcion == "4":
        _ejecutar_dijkstra()
        return
    if opcion == "5":
        _ejecutar_cierre_estacion()
        return
    if opcion == "6":
        _ejecutar_coloreo()
        return
    if opcion == "7":
        _ejecutar_qubit()
        return
    if opcion == "8":
        _ejecutar_boole()
        return
    if opcion == "9":
        print("Salida solicitada.")
        return

    raise ValueError("Opcion no valida. Use 1, 2, 3, 4, 5, 6, 7, 8 o 9.")


if __name__ == "__main__":
    main()
