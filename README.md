# Taller 3 - Programacion Discreta

Universidad Nacional de Colombia

## Integrante

- Sebastian Arevalo

## Lenguaje

- Python 3.8 o superior

---

## Descripcion

Este proyecto implementa una interfaz por consola para resolver los ocho ejercicios del Taller 3 de Matematicas Discretas I.

La aplicacion agrupa algoritmos de criptografia, grafos, computacion cuantica basica, algebra de Boole y entropia de Shannon.

---

## Estructura

```text
Programacion_Discreta/
|-- README.md
|-- LICENSE
|-- .gitignore
|-- requirements.txt
|-- src/
|-- tests/
|-- data/
|-- docs/
```

---

## Ejercicios

### 1. Cifrado Cesar

- Cifra y descifra texto desplazando letras dentro del alfabeto latino.
- Conserva mayusculas, minusculas y caracteres no alfabeticos.
- Los resultados se muestran con pausas para facilitar la lectura.

### 2. RSA de juguete

- Recibe dos primos `p` y `q`, un exponente publico `e` y un mensaje entero `M`.
- Calcula `n = p q`, `phi(n) = (p - 1)(q - 1)`, el inverso modular `d` de `e` modulo `phi(n)`, el cifrado `C` y el descifrado de `M`.
- Implementa Euclides extendido para calcular el inverso modular.
- Si `gcd(e, phi(n)) != 1`, el programa avisa que `e` no es valido.
- Caso obligatorio del taller:
  - `p = 61`
  - `q = 53`
  - `e = 17`
  - `M = 65`
  - Resultado esperado: `n = 3233`, `phi(n) = 3120`, `d = 2753`, `C = 2790`, `M = 65`

### 3. Computacion multipartita segura (MPC)

- Simula un protocolo de suma secreta con tres servidores.
- Recibe una lista de notas enteras entre `0` y `50`.
- Cada nota se divide en tres partes aleatorias modulo `M`.
- Usa `M = 1000003` por defecto.
- Ningun servidor recibe la lista original completa.
- La salida principal muestra solo la suma total y el promedio.
- Ejemplo del taller:
  - Notas: `[40, 35, 50, 25]`
  - Suma reconstruida: `150`
  - Promedio: `37.5`

### 4. Algoritmo de Dijkstra

- Calcula la ruta mas corta entre dos nodos de un grafo cargado desde `data/grafo_ciudad.json`.
- Muestra la distancia minima y el camino encontrado.

### 5. Cierre de estacion

- Analiza si una estacion es critica dentro del grafo de ciudad.
- Reporta la estacion evaluada, las estaciones criticas y los componentes restantes.

### 6. Coloreo de grafos

- Aplica coloreo greedy sobre el grafo de ciudad.
- Muestra la asignacion de colores, el numero de colores usados y si el coloreo es valido.

### 7. Simulacion de qubit

- Muestra estados basicos `|0>` y `|1>`.
- Incluye superposicion y aplicacion de puertas `X` y `H`.
- Presenta un resumen de amplitudes y probabilidades.

### 8. Algebra de Boole

- Calcula tablas de verdad.
- Realiza simplificacion booleana.
- Calcula entropia de Shannon a partir de frecuencias.

---

## Ejecucion

Clonar el repositorio:

```bash
git clone https://github.com/AlexisArevalo/Programacion_Discreta.git
```

Entrar al proyecto:

```bash
cd Programacion_Discreta
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar la aplicacion:

```bash
python src/main.py
```

Si estas en Windows y tienes Python instalado con una ruta fija, tambien puedes usarla directamente:

```powershell
& "C:\Users\sebas\AppData\Local\Programs\Python\Python38\python.exe" src\main.py
```

---

## Pruebas

Ejecutar toda la bateria automatica:

```bash
python -m unittest discover -s tests
```

Ejecutar pruebas puntuales:

```bash
python -m unittest tests.test_cesar tests.test_rsa tests.test_mpc
```

---

## Documentacion

La explicacion matematica de cada algoritmo se encuentra en la carpeta `docs`.

---

## Notas

- La interfaz por consola fue pensada para mostrar los resultados con pausas de lectura.
- RSA y MPC son versiones didacticas para entender la idea matematica, no implementaciones de seguridad real.
