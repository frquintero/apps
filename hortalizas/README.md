# Hortalizas Learning App

Una aplicación interactiva de línea de comandos en Python para aprender sobre hortalizas en español: su clasificación (verdura/legumbre) y su parte comestible.

## Flujo de Aprendizaje Inteligente

La aplicación utiliza el mismo sistema basado en etiquetas que la aplicación de conjuntos, con una cola de refuerzo para priorizar elementos no vistos y revisar errores:

### Cómo funciona
1. **Etiquetas por pregunta**: `n` (no preguntado), `p` (preguntado y correcto), `pn` (preguntado e incorrecto).
2. **Prioridad de selección**: Siempre elegir aleatoriamente de `n` cuando esté disponible.
3. **Refuerzo de errores**: Los elementos `pn` van a una cola y reaparecen periódicamente (intercalados).
4. **Reinicio de ciclo**: Cuando todo está en `p`, reiniciar todo a `n` para otra ronda.

### Beneficios
- **Cobertura eficiente**: Prioriza elementos no vistos antes de repetir.
- **Refuerzo útil**: Los errores reaparecen en una cadencia corta para consolidar la memoria.
- **Simple y predecible**: No hay repeticiones inmediatas mientras haya `n` pendientes.

### Indicadores visuales
- 🔄 **Repaso**: Mostrado cuando una pregunta viene de la cola de refuerzo.
- 📝 **Agregado a refuerzo**: Mostrado cuando fallas una pregunta.
- 📊 **Estadísticas**: "Hortalizas preguntadas X de Y" y tamaño de cola al final.

## Descripción

Esta aplicación te ayuda a aprender sobre hortalizas en español. Para cada hortaliza, debes identificar:
1. **Clasificación**: Si es una verdura o legumbre
2. **Parte comestible**: Qué parte de la planta consumimos (solo si aciertas la clasificación)

### Partes comestibles incluidas:
- **raíz**: zanahoria, remolacha, rábano
- **tubérculo**: patata, boniato, ñame  
- **bulbo**: cebolla, ajo, hinojo
- **tallo**: apio, espárrago, puerro
- **hoja**: espinaca, lechuga, col (verduras de hoja grande)
- **hierba**: perejil, cilantro, albahaca (hierbas aromáticas)
- **brote**: coles de Bruselas
- **flor**: brócoli, coliflor, alcachofa
- **fruto**: tomate, pepino, berenjena
- **vaina**: judía verde, guisante de nieve
- **semilla**: guisante, haba (frescos), frijol, lenteja (secos)
- **hongo**: setas, champiñones

**Nota importante**: Si respondes incorrectamente la clasificación, el programa mostrará ambas respuestas correctas (clasificación y parte comestible) y pasará directamente a la siguiente hortaliza.

## Características

- **60+ hortalizas**: Incluye verduras y legumbres comunes con sus nombres en español.
- **Navegación interactiva**: Usa las teclas de flechas ↑↓ para navegar entre opciones.
- **Pregunta condicional**: Solo se hace la segunda pregunta si aciertas la primera.
- **CLI interactiva**: Preguntas con menús navegables y retroalimentación inmediata.
- **Pantalla limpia**: La terminal se limpia antes del mensaje de bienvenida.
- **Planificador basado en etiquetas**: Prioriza `n`, refuerza `pn`, reinicia `p→n`.
- **Refuerzo intercalado**: Los errores resurgen cada pocas preguntas.

## Requisitos

- Python 3.6+
- Biblioteca `inquirer` para la navegación interactiva

## Instalación

1. Clona o descarga `hortalizas.py` y `hortalizas.json`.
2. Instala las dependencias:
   ```bash
   pip install inquirer
   ```

### Ejecución

Local:

```bash
python3 hortalizas.py
```

Verificar versión:

```bash
python3 hortalizas.py --version
```

## Ejemplo de uso

```
🥕 ¡Bienvenido a la aplicación de aprendizaje de hortalizas! 🌽
Usa las flechas ↑↓ para navegar y Enter para seleccionar.
Presiona Ctrl+C en cualquier momento para salir.

==================================================
🌱 Hortaliza: tomate
==================================================

? ¿Cómo clasificarías 'tomate'? 
❯ verdura
  legumbre

? ¿Cuál es la parte comestible de 'tomate'? 
  raíz
  tubérculo
  bulbo
  tallo
  hoja
  brote
  flor
❯ fruto
  vaina
  semilla
  hierba
  hongo

¡Ambas respuestas correctas! ✅✅

==================================================
🌱 Hortaliza: zanahoria
==================================================

? ¿Cómo clasificarías 'zanahoria'? 
❯ verdura
  legumbre

❌ Incorrecto.
Respuestas correctas:
  • Clasificación: legumbre
  • Parte comestible: semilla
📝 zanahoria agregado a refuerzo.

==================================================
🌱 Hortaliza: garbanzo
==================================================

? ¿Cómo clasificarías 'garbanzo'? 
  verdura
❯ legumbre

? ¿Cuál es la parte comestible de 'garbanzo'? 
  raíz
  tubérculo
  bulbo
  tallo
  hoja
  brote
  flor
  fruto
  vaina
❯ semilla
  hierba
  hongo

¡Ambas respuestas correctas! ✅✅

[Ctrl+C para salir]

🛑 Programa terminado por el usuario

📊 Estadísticas de la sesión:
• Hortalizas preguntadas: 2 de 61
• En refuerzo: 0
• Puntuación final: 2/2 correctas (100.0%)
```

## Datos incluidos

### Ejemplos de hortalizas
- **Verduras**:
  - **Raíces**: zanahoria, remolacha, rábano
  - **Tubérculos**: patata, boniato, ñame
  - **Bulbos**: cebolla, ajo, hinojo
  - **Tallos**: apio, espárrago, puerro
  - **Hojas**: espinaca, lechuga, col (verduras de hoja grande)
  - **Hierbas**: perejil, cilantro, albahaca (hierbas aromáticas)
  - **Flores**: brócoli, coliflor, alcachofa
  - **Frutos**: tomate, pepino, berenjena, calabacín

- **Legumbres**:
  - **Semillas secas**: frijol, lenteja, garbanzo, soja

### Navegación
- **↑↓**: Navegar entre opciones
- **Enter**: Seleccionar opción
- **Ctrl+C**: Salir del programa

## Estructura del código

- `HORTALIZAS`: Diccionario cargado desde `hortalizas.json`
- `main()`: Bucle principal del juego
- `hacer_pregunta_clasificacion()`: Pregunta sobre verdura/legumbre
- `hacer_pregunta_parte_comestible()`: Pregunta sobre la parte comestible
- `evaluar_respuesta()`: Evalúa ambas respuestas y proporciona retroalimentación

## Personalización

Puedes modificar el archivo `hortalizas.json` para:
- Añadir más hortalizas
- Cambiar clasificaciones
- Agregar nuevas partes comestibles
- Adaptar para otros idiomas

## Solución de problemas

### Error de importación de inquirer
```bash
pip install inquirer
```

### Problemas de codificación UTF-8
La aplicación maneja automáticamente problemas de codificación, pero asegúrate de que tu terminal soporte UTF-8.

### Interrumpido (Ctrl+C)
Comportamiento normal para salir del programa. Las estadísticas se mostrarán antes de terminar.
