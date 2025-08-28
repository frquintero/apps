#!/usr/bin/env python3
"""
Aplicación interactiva de línea de comandos para aprender sonidos de animales en español.
El usuario debe adivinar el sonido que hace cada animal o categoría de animales.
"""

import random  # Para selección aleatoria controlada
import sys     # Para manejar la salida del programa si es necesario
import os      # Para limpiar la pantalla del terminal y manejar archivos
# sin dependencias externas

# Diccionario de animales/categorías y sus sonidos en español
# Incluye sustantivo, verbo infinitivo y forma coloquial (3ª persona singular)
ANIMALES = {
    # Animales individuales
    "perro": ["ladrido", "ladrar", "ladra"],
    "gato": ["maullido", "maullar", "maúlla"],
    "vaca": ["mugido", "mugir", "muge"],
    "toro": ["bramido", "bramar", "brama"],
    "caballo": ["relincho", "relinchar", "relincha"],
    "mula": ["rebuzno", "rebuznar", "rebuzna"],
    "burro": ["rebuzno", "rebuznar", "rebuzna"],
    "oveja": ["balido", "balir", "bala"],
    "cabra": ["balido", "balir", "bala"],
    "cerdo": ["gruñido", "gruñir", "gruñe"],
    "gallina": ["cacareo", "cacarear", "cacarea"],
    "gallo": ["canto", "cantar", "canta"],
    "pollito": ["pío", "piar", "pía"],
    "pavo": ["gorgoteo", "gorgotear", "gorgotea"],
    "pato": ["graznido", "graznar", "grazna"],
    "ganso": ["graznido", "graznar", "grazna"],
    "elefante": ["barrito", "barritar", "barrita"],
    "león": ["rugido", "rugir", "ruge"],
    "tigre": ["rugido", "rugir", "ruge"],
    "oso": ["gruñido", "gruñir", "gruñe"],
    "mono": ["chillido", "chillar", "chilla"],
    "águila": ["chillido", "chillar", "chilla"],
    "búho": ["ululato", "ulular", "ulula"],
    "rana": ["croar", "croar", "croa"],
    "serpiente": ["siseo", "sisear", "sisea"],
    "mosquito": ["zumbido", "zumbar", "zumba"],
    "abeja": ["zumbido", "zumbar", "zumba"],
    "delfín": ["silbido", "silbar", "silba"],
    "ballena": ["canto", "cantar", "canta"],
    "cocodrilo": ["gruñido", "gruñir", "gruñe"],
    "pájaro": ["canto", "cantar", "canta"],
    "cuervo": ["graznido", "graznar", "grazna"],
    "paloma": ["arrullo", "arrullar", "arrulla"],
    "loro": ["parloteo", "parlotear", "parlotea"],
    "canario": ["trino", "trinar", "trina"],
    "lobo": ["aullido", "aullar", "aúlla"],
    "zorro": ["ladrido", "ladrar", "ladra"],
    "conejo": ["chillido", "chillar", "chilla"],
    "ratón": ["chillido", "chillar", "chilla"],
    "ardilla": ["chillido", "chillar", "chilla"],
    "ciervo": ["bramido", "bramar", "brama"],
    "jabalí": ["gruñido", "gruñir", "gruñe"],
    "grillo": ["chirrido", "chirriar", "chirría"],
    "saltamontes": ["chirrido", "chirriar", "chirría"],
    "avispa": ["zumbido", "zumbar", "zumba"],
    "mosca": ["zumbido", "zumbar", "zumba"],
    "culebra": ["siseo", "sisear", "sisea"],
    "víbora": ["siseo", "sisear", "sisea"],
    # Categorías agrupadas por sonidos similares
    "insectos voladores": ["zumbido", "zumbar", "zumba"],
    "aves pequeñas": ["trino", "trinar", "trina"],
    "felinos grandes": ["rugido", "rugir", "ruge"],
    "reptiles": ["siseo", "sisear", "sisea"],
    "mamíferos pequeños": ["chillido", "chillar", "chilla"],
    "aves acuáticas": ["graznido", "graznar", "grazna"],
    "insectos": ["chirrido", "chirriar", "chirría"],
    "mamíferos grandes": ["gruñido", "gruñir", "gruñe"],
}

# (SRS/persistencia eliminados para un flujo simple por etiquetas)

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
    return random.choice(list(labels.keys() or ANIMALES.keys())), False


def main():
    """
    Función principal que ejecuta el bucle del juego.
    """
    # Estado de sesión (etiquetas + refuerzo)
    intentos_totales = 0
    respuestas_correctas = 0
    num_preguntas = 0
    labels = {animal: 'n' for animal in ANIMALES.keys()}
    asked_set = set()  # animales preguntados al menos una vez en la sesión
    review_queue = []  # cola de animales con etiqueta 'pn'

    # Configurar codificación robusta para I/O de consola
    try:
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    # Limpiar la pantalla del terminal antes de mostrar el mensaje de bienvenida
    os.system('clear')

    print("¡Bienvenido a la aplicación de sonidos de animales!")
    print("Escribe 'quit' o 'q' en cualquier momento para salir.\n")
    print("💡 Modo etiquetas: prioriza no preguntados ('n') y refuerza fallos ('pn').")
    print("🔄 Refuerzo: preguntas falladas reaparecen cada cierto tiempo.\n")

    # Bucle principal del juego
    try:
        while True:
            # Seleccionar siguiente por etiquetas + refuerzo
            animal, es_refuerzo = seleccionar_siguiente_por_etiquetas(labels, review_queue, num_preguntas)
            sonidos_validos = ANIMALES[animal]

            # Hacer la pregunta al usuario
            pregunta_tipo = "🔄 Repaso" if es_refuerzo else "❓ Pregunta"
            try:
                respuesta_usuario = input(f"{pregunta_tipo} - ¿Cuál es el sonido que hace el/la {animal}? ").strip()
            except EOFError:
                print("\n\n❌ Error: No se pudo leer la entrada del usuario.")
                print("Esto puede suceder cuando se ejecuta el script sin una terminal interactiva.")
                print("Intenta ejecutar: python3 animal_sounds.py")
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
                break

            # Incrementar contadores
            intentos_totales += 1
            num_preguntas += 1
            asked_set.add(animal)

            # Verificar la respuesta (ignorando mayúsculas/minúsculas y espacios)
            # Comprobar si la respuesta está en la lista de sonidos válidos
            respuesta_correcta = any(respuesta_usuario.lower() == sonido.lower() for sonido in sonidos_validos)

            # Actualizar etiquetas y refuerzo
            if respuesta_correcta:
                print("¡Correcto! ✅")
                respuestas_correctas += 1
                labels[animal] = 'p'
                if es_refuerzo and review_queue and review_queue[0] == animal:
                    review_queue.pop(0)
            else:
                # Mostrar todas las opciones válidas
                opciones = " o ".join(f"'{sonido}'" for sonido in sonidos_validos)
                print(f"Incorrecto – las respuestas correctas son {opciones}")
                labels[animal] = 'pn'
                if animal not in review_queue:
                    review_queue.append(animal)
                    print(f"📝 {animal} agregado a refuerzo.")

            print()  # Línea en blanco para mejor legibilidad

    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar la aplicación de sonidos de animales.")
        print("Puedes continuar en otro momento.")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print("La aplicación se cerrará por seguridad.")
    finally:
        # Mostrar estadísticas finales si se jugó al menos una ronda
        if intentos_totales > 0:
            print(f"\n📊 Estadísticas de la sesión:")
            preguntados = len(asked_set)
            total = len(ANIMALES)
            print(f"• Animales preguntados {preguntados} de {total}")
            print(f"• En refuerzo: {len(review_queue)}")
            print(f"Puntuación final: {respuestas_correctas}/{intentos_totales} correctas")

    # Salir del programa
    sys.exit(0)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
