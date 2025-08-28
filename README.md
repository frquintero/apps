# Animal Sounds Learning App

An interactive command-line app in Python to learn the sounds animals make in Spanish.

Note: The app prompts and accepted answers are in Spanish. It is intended for Spanish learners/users.

## Intelligent Learning Flow

The app uses a simple label-based flow with a reinforcement queue to prioritize unseen items and revisit mistakes without unnecessary repetition:

### How it works
1. Labels per question: `n` (not asked), `p` (asked and correct), `pn` (asked and incorrect).
2. Selection priority: Always pick randomly from `n` when available.
3. Mistake reinforcement: `pn` items go into a queue and reappear periodically (interleaved).
4. Cycle reset: When everything is `p`, reset all back to `n` for another round.

### Benefits
- Efficient coverage: Prioritizes unseen items before repeating.
- Helpful reinforcement: Mistakes reappear on a short cadence to consolidate memory.
- Simple and predictable: No immediate repeats while there are pending `n`.
- Clear stats: Session coverage and reinforcement queue size.

### Visual indicators
- 🔄 Review: Shown when a question comes from the reinforcement queue.
- 📝 Added to reinforcement: Shown when you miss a question.
- 📊 Stats: “Animals asked X of Y” and queue size at the end.

## Description

This app helps you practice the sounds of many animals and animal categories in Spanish. It randomly selects an animal or category and asks for the sound. Great for Spanish learners, kids, or anyone curious about nature.

🚀 Global access: Once configured, you can run `animals` from anywhere.

## Features

- 40+ animals and categories: Includes individual animals and grouped categories (e.g., “insectos voladores” make “zumbido”).
- Flexible answers: Accepts Spanish nouns, infinitive verbs, and common forms (e.g., “ladrido”, “ladrar”, “ladra”).
- Interactive CLI: Random questions with immediate feedback.
- Clean screen: The terminal clears before the welcome message.
- Label-based scheduler: Prioritizes `n`, reinforces `pn`, resets `p→n`.
- Interleaved reinforcement: Errors resurface every few questions.

## Requirements

- Python 3.6+
- Standard library only (random, sys)

## Installation

1. Clone or download `animal_sounds.py`.
2. Make sure Python 3 is installed.
3. Optional global access: create a small wrapper to run `animals` from anywhere.

### Running

Global (if configured):

```bash
animals
```

Local:

```bash
python3 animal_sounds.py
```

## Example

The UI is in Spanish by design; here’s a short sample:

```
[Clean terminal]

¡Bienvenido a la aplicación de sonidos de animales!
Escribe 'quit' o 'q' en cualquier momento para salir.

💡 Modo etiquetas: prioriza no preguntados ('n') y refuerza fallos ('pn').
🔄 Refuerzo: preguntas falladas reaparecen cada cierto tiempo.

¿Cuál es el sonido que hace el/la perro? ladra
¡Correcto! ✅

¿Cuál es el sonido que hace el/la vaca? mugir
Incorrecto – las respuestas correctas son 'mugido' o 'mugir' o 'muge'
📝 vaca agregado a refuerzo.

🔄 Repaso: vaca
¿Cuál es el sonido que hace el/la vaca? muge
¡Correcto! ✅

quit

📊 Estadísticas de la sesión:
• Animales preguntados 6 de 50
• En refuerzo: 0
Puntuación final: 6/7 correctas
```

## Included animals

### Individual animals
- perro, gato, vaca, caballo, oveja, cerdo, gallina, gallo, pato, ganso
- elefante, león, tigre, oso, mono, águila, búho, rana, serpiente
- mosquito, abeja, delfín, ballena, cocodrilo, pájaro, cuervo, paloma
- loro, canario, lobo, zorro, conejo, ratón, ardilla, ciervo, jabalí
- grillo, saltamontes, avispa, mosca, culebra, víbora

### Categories
- insectos voladores (zumbido)
- aves pequeñas (trino)
- felinos grandes (rugido)
- reptiles (siseo)
- mamíferos pequeños (chillido)
- aves acuáticas (graznido)
- insectos (chirrido)
- mamíferos grandes (gruñido)

## Code structure

- `ANIMALES`: Spanish animal/category dictionary mapping to valid sounds (noun, verb, common forms)
- `main()`: Main game loop
- Label-based selection with a simple reinforcement queue
- Case-insensitive answer checking

## Customization

You can modify the `ANIMALES` dictionary to:
- Add more animals
- Change or expand valid sounds
- Add new categories
- Adapt for other languages

## Troubleshooting

### `animals` command not found (global setup)
If the global command doesn’t work:

1. Reload your shell config:
   ```bash
   source ~/.zshrc
   ```

2. Verify it’s on PATH:
   ```bash
   which animals
   ```

3. Ensure the wrapper is executable:
   ```bash
   ls -la ~/bin/animals
   ```

4. If it still fails, run locally:
   ```bash
   python3 animal_sounds.py
   ```

### EOFError on input
- Handled gracefully by the app; typically happens without a real TTY.
- Recommendation: run in a real terminal: `python3 animal_sounds.py`.

### Interrupted (Ctrl+C)
- Exits cleanly and shows final stats.
