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

def seleccionar_animal_inteligente(animales_preguntados, cola_revision, contador_preguntas):
    """
    Selecciona un animal usando un algoritmo inteligente:
    - Animales respondidos correctamente tienen menor probabilidad de ser preguntados
    - Animales respondidos incorrectamente se agregan a una cola de revisión
    - Después de 5 preguntas, se prioriza la cola de revisión
    """
    # Si hay animales en la cola de revisión y han pasado 8 preguntas, priorizarlos
    if cola_revision and contador_preguntas % 9 == 0:  # Cada 9 preguntas (contando desde 0)
        animal = cola_revision.pop(0)  # Sacar el primer animal de la cola
        print(f"🔄 Repasando: {animal}")
        return animal

    # Crear lista de animales disponibles con pesos
    animales_disponibles = []
    pesos = []

    for animal in ANIMALES.keys():
        if animal in animales_preguntados:
            # Si ya fue preguntado, reducir su peso (menor probabilidad)
            if animales_preguntados[animal]:  # Respondido correctamente
                peso = 0.5  # Peso muy bajo para animales ya acertados (10x menos probable)
            else:  # Respondido incorrectamente
                peso = 2  # Peso medio para animales fallados (pero no en cola de revisión)
        else:
            # Nunca preguntado - peso alto
            peso = 10  # Peso mucho más alto para animales nunca preguntados

        animales_disponibles.append(animal)
        pesos.append(peso)

    # Seleccionar animal basado en pesos
    animal_seleccionado = random.choices(animales_disponibles, weights=pesos, k=1)[0]

    # Debug: mostrar estadísticas de selección (opcional - descomentar para debugging)
    # if contador_preguntas < 5:  # Solo mostrar las primeras 5 preguntas
    #     print(f"DEBUG - Pesos: Correctos={sum(1 for p in pesos if p == 0.5)}, Incorrectos={sum(1 for p in pesos if p == 2)}, Nuevos={sum(1 for p in pesos if p == 10)}")

    return animal_seleccionado

def main():
    """
    Función principal que ejecuta el bucle del juego.
    """
    # Inicializar variables de puntuación
    intentos_totales = 0  # Contador de intentos realizados
    respuestas_correctas = 0  # Contador de respuestas correctas

    # Variables para el algoritmo inteligente
    animales_preguntados = {}  # Diccionario: animal -> True (correcto) / False (incorrecto)
    cola_revision = []  # Cola de animales que necesitan revisión
    contador_preguntas = 0  # Contador para saber cuándo revisar

    # Limpiar la pantalla del terminal antes de mostrar el mensaje de bienvenida
    os.system('clear')

    print("¡Bienvenido a la aplicación de sonidos de animales!")
    print("Escribe 'quit' o 'q' en cualquier momento para salir.\n")
    print("💡 Sistema inteligente: Los animales que aciertes tendrán menor probabilidad de repetirse.")
    print("🔄 Los que falles serán repasados después de varias preguntas.\n")

    # Bucle principal del juego
    try:
        while True:
            # Seleccionar un animal usando el algoritmo inteligente
            animal = seleccionar_animal_inteligente(animales_preguntados, cola_revision, contador_preguntas)
            sonidos_validos = ANIMALES[animal]

            # Hacer la pregunta al usuario
            pregunta_tipo = "🔄 Repaso" if animal in cola_revision else "❓ Pregunta"
            try:
                respuesta_usuario = input(f"{pregunta_tipo} - ¿Cuál es el sonido que hace el/la {animal}? ").strip()
            except EOFError:
                print("\n\n❌ Error: No se pudo leer la entrada del usuario.")
                print("Esto puede suceder cuando se ejecuta el script sin una terminal interactiva.")
                print("Intenta ejecutar: python3 animal_sounds.py")
                break

            # Verificar si el usuario quiere salir
            if respuesta_usuario.lower() in ['quit', 'q']:
                break

            # Incrementar contador de intentos y preguntas
            intentos_totales += 1
            contador_preguntas += 1

            # Verificar la respuesta (ignorando mayúsculas/minúsculas y espacios)
            # Comprobar si la respuesta está en la lista de sonidos válidos
            respuesta_correcta = False
            for sonido in sonidos_validos:
                if respuesta_usuario.lower() == sonido.lower():
                    respuesta_correcta = True
                    break

            # Actualizar el seguimiento del animal
            if respuesta_correcta:
                print("¡Correcto! ✅")
                respuestas_correctas += 1
                animales_preguntados[animal] = True

                # Si el animal estaba en la cola de revisión, removerlo
                if animal in cola_revision:
                    cola_revision.remove(animal)
                    print(f"🎯 {animal} dominado - removido de la lista de repaso.")
            else:
                # Mostrar todas las opciones válidas
                opciones = " o ".join(f"'{sonido}'" for sonido in sonidos_validos)
                print(f"Incorrecto – las respuestas correctas son {opciones}")
                animales_preguntados[animal] = False

                # Agregar a la cola de revisión si no está ya
                if animal not in cola_revision:
                    cola_revision.append(animal)
                    print(f"📝 {animal} agregado a la lista de repaso.")

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
            print(f"\n📊 Estadísticas de aprendizaje:")
            print(f"• Animales preguntados: {len(animales_preguntados)}")
            animales_acertados = sum(1 for resultado in animales_preguntados.values() if resultado)
            print(f"• Animales dominados: {animales_acertados}")
            print(f"• Animales en lista de repaso: {len(cola_revision)}")

            if animales_preguntados:
                porcentaje_dominio = (animales_acertados / len(animales_preguntados)) * 100
                print(f"• Nivel de dominio: {porcentaje_dominio:.1f}%")

            print(f"Puntuación final: {respuestas_correctas}/{intentos_totales} correctas")

    # Salir del programa
    sys.exit(0)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
