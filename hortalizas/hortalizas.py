#!/usr/bin/env python3
"""
Aplicación interactiva de línea de comandos para aprender hortalizas en español.
El usuario debe identificar la clasificación (verdura/legumbre) y la parte comestible de cada hortaliza.
"""

import random
import sys
import os
import json
import inquirer

# Versión de la aplicación
__version__ = "0.1.0"

# Diccionario de hortalizas cargado desde hortalizas.json
HORTALIZAS = {}

def cargar_hortalizas():
    """Carga las hortalizas desde hortalizas.json"""
    global HORTALIZAS
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, 'hortalizas.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            HORTALIZAS = {item['name']: item for item in data['items']}
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo hortalizas.json en {path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo hortalizas.json no tiene formato JSON válido")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al cargar hortalizas.json: {e}")
        sys.exit(1)

REVIEW_EVERY = 4  # cada cuántas preguntas lanzar una de refuerzo si hay

def seleccionar_siguiente_por_etiquetas(labels, review_queue, num_preguntas):
    """Selecciona la siguiente hortaliza basándose en el sistema de etiquetas"""
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
    return random.choice(list(labels.keys() or HORTALIZAS.keys())), False

def hacer_pregunta_clasificacion(hortaliza_name, es_refuerzo):
    """Hace la pregunta sobre la clasificación de la hortaliza"""
    prefijo = "🔄 Repaso - " if es_refuerzo else ""
    
    opciones = ['verdura', 'legumbre']
    
    questions = [
        inquirer.List('clasificacion',
                     message=f"{prefijo}¿Cómo clasificarías '{hortaliza_name}'?",
                     choices=opciones,
                     carousel=True)
    ]
    
    try:
        answers = inquirer.prompt(questions)
        if answers is None:  # El usuario presionó Ctrl+C
            return None
        return answers['clasificacion']
    except KeyboardInterrupt:
        return None

def hacer_pregunta_parte_comestible(hortaliza_name, es_refuerzo):
    """Hace la pregunta sobre la parte comestible de la hortaliza"""
    prefijo = "🔄 Repaso - " if es_refuerzo else ""
    
    # Opciones basadas en las partes comestibles del JSON
    opciones = ['raíz', 'tubérculo', 'bulbo', 'tallo', 'hoja', 'brote', 'flor', 
                'fruto', 'vaina', 'semilla', 'hierba', 'hongo']
    
    questions = [
        inquirer.List('parte_comestible',
                     message=f"{prefijo}¿Cuál es la parte comestible de '{hortaliza_name}'?",
                     choices=opciones,
                     carousel=True)
    ]
    
    try:
        answers = inquirer.prompt(questions)
        if answers is None:  # El usuario presionó Ctrl+C
            return None
        return answers['parte_comestible']
    except KeyboardInterrupt:
        return None

def evaluar_respuesta(hortaliza_name, respuesta_clasificacion, respuesta_parte, hortaliza_data):
    """Evalúa las respuestas del usuario y devuelve si fueron correctas"""
    clasificacion_correcta = respuesta_clasificacion == hortaliza_data['classification']
    parte_correcta = respuesta_parte == hortaliza_data['edible_part']
    
    ambas_correctas = clasificacion_correcta and parte_correcta
    
    if ambas_correctas:
        print("¡Ambas respuestas correctas! ✅✅")
    else:
        print("Respuestas:")
        if clasificacion_correcta:
            print(f"  Clasificación: ✅ Correcto ({respuesta_clasificacion})")
        else:
            print(f"  Clasificación: ❌ Incorrecto. Respuesta correcta: {hortaliza_data['classification']}")
        
        if parte_correcta:
            print(f"  Parte comestible: ✅ Correcto ({respuesta_parte})")
        else:
            print(f"  Parte comestible: ❌ Incorrecto. Respuesta correcta: {hortaliza_data['edible_part']}")
    
    return ambas_correctas

def main():
    """Función principal que ejecuta el bucle del juego"""
    # Mostrar la versión y salir si se solicita
    if any(arg in ("--version", "-V") for arg in sys.argv[1:]):
        print(__version__)
        return

    # Cargar las hortalizas desde el archivo
    cargar_hortalizas()

    if not HORTALIZAS:
        print("❌ Error: No se encontraron hortalizas válidas en el archivo")
        sys.exit(1)

    # Estado de sesión (etiquetas + refuerzo)
    intentos_totales = 0
    respuestas_correctas = 0
    num_preguntas = 0
    labels = {hortaliza: 'n' for hortaliza in HORTALIZAS.keys()}
    asked_set = set()  # hortalizas preguntadas al menos una vez en la sesión
    review_queue = []  # cola de hortalizas con etiqueta 'pn'

    # Configurar codificación robusta para I/O de consola
    try:
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    # Limpiar la pantalla del terminal antes de mostrar el mensaje de bienvenida
    os.system('clear')

    print("🥕 ¡Bienvenido a la aplicación de aprendizaje de hortalizas! 🌽")
    print("Usa las flechas ↑↓ para navegar y Enter para seleccionar.")
    print("Presiona Ctrl+C en cualquier momento para salir.\n")

    # Bucle principal del juego
    try:
        while True:
            # Seleccionar siguiente hortaliza por etiquetas + refuerzo
            hortaliza_name, es_refuerzo = seleccionar_siguiente_por_etiquetas(labels, review_queue, num_preguntas)
            hortaliza_data = HORTALIZAS[hortaliza_name]

            print(f"\n{'='*50}")
            print(f"🌱 Hortaliza: {hortaliza_name}")
            print(f"{'='*50}")

            # Hacer pregunta sobre clasificación
            respuesta_clasificacion = hacer_pregunta_clasificacion(hortaliza_name, es_refuerzo)
            if respuesta_clasificacion is None:
                break

            # Incrementar contadores
            intentos_totales += 1
            num_preguntas += 1
            asked_set.add(hortaliza_name)

            # Verificar si la clasificación es correcta
            clasificacion_correcta = respuesta_clasificacion == hortaliza_data['classification']
            
            if not clasificacion_correcta:
                # Si la clasificación es incorrecta, mostrar ambas respuestas correctas y continuar
                print(f"❌ Incorrecto.")
                print(f"Respuestas correctas:")
                print(f"  • Clasificación: {hortaliza_data['classification']}")
                print(f"  • Parte comestible: {hortaliza_data['edible_part']}")
                
                # Marcar como incorrecta y agregar a refuerzo
                labels[hortaliza_name] = 'pn'
                if hortaliza_name not in review_queue:
                    review_queue.append(hortaliza_name)
                    print(f"📝 {hortaliza_name} agregado a refuerzo.")
            else:
                # Si la clasificación es correcta, hacer la segunda pregunta
                respuesta_parte = hacer_pregunta_parte_comestible(hortaliza_name, False)
                if respuesta_parte is None:
                    break

                # Evaluar respuestas
                ambas_correctas = evaluar_respuesta(hortaliza_name, respuesta_clasificacion, respuesta_parte, hortaliza_data)

                # Actualizar etiquetas y refuerzo
                if ambas_correctas:
                    respuestas_correctas += 1
                    labels[hortaliza_name] = 'p'
                    if es_refuerzo and review_queue and review_queue[0] == hortaliza_name:
                        review_queue.pop(0)
                else:
                    labels[hortaliza_name] = 'pn'
                    if hortaliza_name not in review_queue:
                        review_queue.append(hortaliza_name)
                        print(f"📝 {hortaliza_name} agregado a refuerzo.")

            print()  # Línea en blanco para mejor legibilidad

    except KeyboardInterrupt:
        print("\n\n🛑 Programa terminado por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        print("La aplicación se cerrará por seguridad.")
    finally:
        # Mostrar estadísticas finales si se jugó al menos una ronda
        if intentos_totales > 0:
            print(f"\n📊 Estadísticas de la sesión:")
            preguntados = len(asked_set)
            total = len(HORTALIZAS)
            print(f"• Hortalizas preguntadas: {preguntados} de {total}")
            print(f"• En refuerzo: {len(review_queue)}")
            porcentaje = (respuestas_correctas / intentos_totales) * 100 if intentos_totales > 0 else 0
            print(f"• Puntuación final: {respuestas_correctas}/{intentos_totales} correctas ({porcentaje:.1f}%)")

    # Salir del programa
    sys.exit(0)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
