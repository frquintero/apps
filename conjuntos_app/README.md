# Conjuntos Learning App

Una aplicación interactiva de línea de comandos en Python para aprender los nombres de los conjuntos de objetos en español.

Nota: La aplicación hace las preguntas y acepta respuestas en español. Está pensada para estudiantes/usuarios de español.

## Flujo de Aprendizaje Inteligente

La aplicación usa un sistema simple basado en etiquetas con una cola de refuerzo para priorizar elementos no vistos y revisar errores sin repetición innecesaria:

### Cómo funciona
1. Etiquetas por pregunta: `n` (no preguntado), `p` (preguntado y correcto), `pn` (preguntado e incorrecto).
2. Prioridad de selección: Siempre elegir aleatoriamente de `n` cuando esté disponible.
3. Refuerzo de errores: Los elementos `pn` van a una cola y reaparecen periódicamente (intercalados).
4. Reinicio de ciclo: Cuando todo está en `p`, reiniciar todo a `n` para otra ronda.

### Beneficios
- Cobertura eficiente: Prioriza elementos no vistos antes de repetir.
- Refuerzo útil: Los errores reaparecen en una cadencia corta para consolidar la memoria.
- Simple y predecible: No hay repeticiones inmediatas mientras haya `n` pendientes.
- Estadísticas claras: Cobertura de sesión y tamaño de cola de refuerzo.

### Indicadores visuales
- 🔄 Repaso: Mostrado cuando una pregunta viene de la cola de refuerzo.
- 📝 Agregado a refuerzo: Mostrado cuando fallas una pregunta.
- 📊 Estadísticas: "Objetos preguntados X de Y" y tamaño de cola al final.

## Descripción

Esta aplicación te ayuda a practicar los nombres de conjuntos de objetos en español. Selecciona aleatoriamente un tipo de objeto y pregunta por el nombre del conjunto. Ideal para estudiantes de español, niños o cualquiera curioso sobre la lengua.

## Características

- 60+ objetos y conjuntos: Incluye animales, personas, objetos y conceptos (ej. "lobos" forman una "jauría").
- Respuestas flexibles: Acepta el nombre del conjunto correspondiente.
- CLI interactiva: Preguntas aleatorias con retroalimentación inmediata.
- Pantalla limpia: La terminal se limpia antes del mensaje de bienvenida.
- Planificador basado en etiquetas: Prioriza `n`, refuerza `pn`, reinicia `p→n`.
- Refuerzo intercalado: Los errores resurgen cada pocas preguntas.

## Requisitos

- Python 3.6+
- Solo biblioteca estándar (random, sys, json)

## Instalación

1. Clona o descarga `conjuntos.py` y `conjuntos.txt`.
2. Asegúrate de que Python 3 esté instalado.

### Ejecución

Local:

```bash
python3 conjuntos.py
```

Verificar versión:

```bash
python3 conjuntos.py --version
```

## Ejemplo

La interfaz está en español por diseño; aquí tienes una muestra corta:

```
[Terminal limpio]

¡Bienvenido a la aplicación de conjuntos de objetos!
Escribe 'quit' o 'q' en cualquier momento para salir.

¿Cuál es el conjunto formado por lobos? jauría
¡Correcto! ✅

¿Cuál es el conjunto formado por abejas? colmena
Incorrecto – las respuestas correctas son 'enjambre'
📝 abejas agregado a refuerzo.

🔄 Repaso - abejas
¿Cuál es el conjunto formado por abejas? enjambre
¡Correcto! ✅

quit

📊 Estadísticas de la sesión:
• Objetos preguntados 6 de 65
• En refuerzo: 0
Puntuación final: 6/7 correctas
```

## Objetos incluidos

### Ejemplos de conjuntos
- lobos → jauría
- abejas → enjambre
- libros → colección
- jugadores → equipo
- barcos → flota
- estudiantes → clase
- músicos → banda
- soldados → pelotón
- y muchos más...

## Estructura del código

- `CONJUNTOS`: Diccionario español objeto→conjunto cargado desde `conjuntos.txt`
- `main()`: Bucle principal del juego
- Selección basada en etiquetas con una cola simple de refuerzo
- Verificación de respuestas insensible a mayúsculas/minúsculas

## Personalización

Puedes modificar el archivo `conjuntos.txt` para:
- Añadir más objetos y conjuntos
- Cambiar o expandir conjuntos válidos
- Adaptar para otros idiomas

## Solución de problemas

### EOFError en entrada
- Manejado graciosamente por la aplicación; típicamente ocurre sin una TTY real.
- Recomendación: ejecutar en una terminal real: `python3 conjuntos.py`.

### Interrumpido (Ctrl+C)
- Sale limpiamente y muestra estadísticas finales.
