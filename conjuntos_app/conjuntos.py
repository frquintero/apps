#!/usr/bin/env python3
"""
Aplicación interactiva de línea de comandos para aprender conjuntos de objetos en español.
El usuario debe adivinar el nombre del conjunto al que pertenece cada grupo de objetos.
"""

import random  # Para selección aleatoria controlada
import sys     # Para manejar la salida del programa si es necesario
import os      # Para limpiar la pantalla del terminal y manejar archivos
import json    # Para cargar los datos desde conjuntos.txt
# sin dependencias externas

# Versión de la aplicación
__version__ = "0.1.0"

# Diccionario de objetos y sus conjuntos en español
# Se carga desde conjuntos.txt
CONJUNTOS = {}

def cargar_conjuntos():
    """Carga los pares objeto:conjunto desde conjuntos.txt"""
    global CONJUNTOS
    try:
        with open('conjuntos.txt', 'r', encoding='utf-8') as f:
            CONJUNTOS = json.load(f)
        # Convertir a formato compatible con animal_sounds.py (lista de un elemento)
        for objeto, conjunto in CONJUNTOS.items():
            CONJUNTOS[objeto] = [conjunto]
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo conjuntos.txt")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: El archivo conjuntos.txt no tiene formato JSON válido")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al cargar conjuntos.txt: {e}")
        sys.exit(1)

REVIEW_EVERY = 4  # cada cuántas preguntas lanzar una de refuerzo si hay


def seleccionar_siguiente_por_etiquetas(labels, review_queue, num_preguntas):
    # ¿Toca refuerzo?
    if review_queue and num_preguntas > 0 and (num_preguntas % REVIEW_EVERY == 0):
        return review_queue[0], True

    # Elegir de 'n' si hay
    pool_n = [a for a, tag in labels.items() if tag == 'n']
    if pool_n:
        return random.choice(pool_n), False

    # Si todas están en 'p', reiniciar a 'n'
    if labels and all(tag == 'p' for tag in labels.values()):
        for a in labels:
            labels[a] = 'n'
        pool_n = list(labels.keys())
        return random.choice(pool_n), False

    # Si hay 'pn' pero no toca refuerzo, elegir de 'p' para espaciar
    pool_p = [a for a, tag in labels.items() if tag == 'p']
    if pool_p:
        return random.choice(pool_p), False

    # Si no hay 'p', usar refuerzo si existe
    if review_queue:
        return review_queue[0], True

    # Fallback
    return random.choice(list(labels.keys() or CONJUNTOS.keys())), False


def main():
    """
    Función principal que ejecuta el bucle del juego.
    """
    # Mostrar la versión y salir si se solicita antes de cualquier salida/limpieza
    if any(arg in ("--version", "-V") for arg in sys.argv[1:]):
        print(__version__)
        return

    # Cargar los conjuntos desde el archivo
    cargar_conjuntos()

    if not CONJUNTOS:
        print("❌ Error: No se encontraron conjuntos válidos en el archivo")
        sys.exit(1)

    # Estado de sesión (etiquetas + refuerzo)
    intentos_totales = 0
    respuestas_correctas = 0
    num_preguntas = 0
    labels = {objeto: 'n' for objeto in CONJUNTOS.keys()}
    asked_set = set()  # objetos preguntados al menos una vez en la sesión
    review_queue = []  # cola de objetos con etiqueta 'pn'

    # Configurar codificación robusta para I/O de consola
    try:
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    # Limpiar la pantalla del terminal antes de mostrar el mensaje de bienvenida
    os.system('clear')

    print("¡Bienvenido a la aplicación de conjuntos de objetos!")
    print("Escribe 'quit' o 'q' en cualquier momento para salir.\n")

    # Bucle principal del juego
    try:
        while True:
            # Seleccionar siguiente por etiquetas + refuerzo
            objeto, es_refuerzo = seleccionar_siguiente_por_etiquetas(labels, review_queue, num_preguntas)
            conjuntos_validos = CONJUNTOS[objeto]

            # Hacer la pregunta al usuario (sin prefijo para preguntas normales)
            prefijo = "🔄 Repaso - " if es_refuerzo else ""
            try:
                respuesta_usuario = input(f"{prefijo}¿Cuál es el conjunto formado por {objeto}? ").strip()
            except EOFError:
                print("\n\n❌ Error: No se pudo leer la entrada del usuario.")
                print("Esto puede suceder cuando se ejecuta el script sin una terminal interactiva.")
                print("Intenta ejecutar: python3 conjuntos.py")
                break
            except UnicodeError:
                # Fallback de lectura robusta si la terminal no es UTF-8
                try:
                    raw = sys.stdin.buffer.readline()
                    respuesta_usuario = raw.decode('utf-8', errors='replace').strip()
                except Exception:
                    print("\n\n❌ Error de codificación en la entrada. Intenta sin acentos o cambia la codificación de la terminal.")
                    continue

            # Verificar si el usuario quiere salir
            if respuesta_usuario.lower() in ['quit', 'q']:
                print("\nprograma terminado por el usuario")
                break

            # Incrementar contadores
            intentos_totales += 1
            num_preguntas += 1
            asked_set.add(objeto)

            # Verificar la respuesta (ignorando mayúsculas/minúsculas y espacios)
            # Comprobar si la respuesta está en la lista de conjuntos válidos
            respuesta_correcta = any(respuesta_usuario.lower() == conjunto.lower() for conjunto in conjuntos_validos)

            # Actualizar etiquetas y refuerzo
            if respuesta_correcta:
                print("¡Correcto! ✅")
                respuestas_correctas += 1
                labels[objeto] = 'p'
                if es_refuerzo and review_queue and review_queue[0] == objeto:
                    review_queue.pop(0)
            else:
                # Mostrar todas las opciones válidas
                opciones = " o ".join(f"'{conjunto}'" for conjunto in conjuntos_validos)
                print(f"Incorrecto – las respuestas correctas son {opciones}")
                labels[objeto] = 'pn'
                if objeto not in review_queue:
                    review_queue.append(objeto)
                    print(f"📝 {objeto} agregado a refuerzo.")

            print()  # Línea en blanco para mejor legibilidad

    except KeyboardInterrupt:
        print("\nprograma terminado por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print("La aplicación se cerrará por seguridad.")
    finally:
        # Mostrar estadísticas finales si se jugó al menos una ronda
        if intentos_totales > 0:
            print(f"\n📊 Estadísticas de la sesión:")
            preguntados = len(asked_set)
            total = len(CONJUNTOS)
            print(f"• Objetos preguntados {preguntados} de {total}")
            print(f"• En refuerzo: {len(review_queue)}")
            print(f"Puntuación final: {respuestas_correctas}/{intentos_totales} correctas")

    # Salir del programa
    sys.exit(0)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
