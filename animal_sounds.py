#!/usr/bin/env python3
"""
Aplicación interactiva de línea de comandos para aprender sonidos de animales en español.
El usuario debe adivinar el sonido que hace cada animal o categoría de animales.
"""

import random  # Para seleccionar animales aleatoriamente
import sys     # Para manejar la salida del programa si es necesario
import os      # Para limpiar la pantalla del terminal

# Diccionario de animales/categorías y sus sonidos en español
# Incluye sustantivo, verbo infinitivo y forma coloquial (3ª persona singular)
ANIMALES = {
    # Animales individuales
    "perro": ["ladrido", "ladrar", "ladra"],
    "gato": ["maullido", "maullar", "maúlla"],
    "vaca": ["mugido", "mugir", "muge"],
    "caballo": ["relincho", "relinchar", "relincha"],
    "oveja": ["balido", "balir", "bala"],
    "cerdo": ["gruñido", "gruñir", "gruñe"],
    "gallina": ["cacareo", "cacarear", "cacarea"],
    "gallo": ["canto", "cantar", "canta"],
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

def main():
    """
    Función principal que ejecuta el bucle del juego.
    """
    # Inicializar variables de puntuación
    intentos_totales = 0  # Contador de intentos realizados
    respuestas_correctas = 0  # Contador de respuestas correctas

    # Limpiar la pantalla del terminal antes de mostrar el mensaje de bienvenida
    os.system('clear')

    print("¡Bienvenido a la aplicación de sonidos de animales!")
    print("Escribe 'quit' o 'q' en cualquier momento para salir.\n")

    # Bucle principal del juego
    while True:
        # Seleccionar un animal/categoría aleatoriamente
        animal = random.choice(list(ANIMALES.keys()))
        sonidos_validos = ANIMALES[animal]

        # Hacer la pregunta al usuario
        respuesta_usuario = input(f"¿Cuál es el sonido que hace el/la {animal}? ").strip()

        # Verificar si el usuario quiere salir
        if respuesta_usuario.lower() in ['quit', 'q']:
            break

        # Incrementar contador de intentos
        intentos_totales += 1

        # Verificar la respuesta (ignorando mayúsculas/minúsculas y espacios)
        # Comprobar si la respuesta está en la lista de sonidos válidos
        respuesta_correcta = False
        for sonido in sonidos_validos:
            if respuesta_usuario.lower() == sonido.lower():
                respuesta_correcta = True
                break

        if respuesta_correcta:
            print("¡Correcto!")
            respuestas_correctas += 1
        else:
            # Mostrar todas las opciones válidas
            opciones = " o ".join(f"'{sonido}'" for sonido in sonidos_validos)
            print(f"Incorrecto – las respuestas correctas son {opciones}")

        print()  # Línea en blanco para mejor legibilidad

    # Mostrar puntuación final al salir
    print(f"\n¡Gracias por jugar!")
    print(f"Puntuación final: {respuestas_correctas}/{intentos_totales} correctas")

    # Salir del programa
    sys.exit(0)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
