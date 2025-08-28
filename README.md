# Animal Sounds Learning App

Una aplicación interactiva de línea de comandos escrita en Python para apr## Estructura del código

- `ANIMALES`: Diccionario que contiene los animales/categorías y listas de sonidos válidos (sustantivo, verbo infinitivo y forma coloquial)
- `main()`: Función principal que maneja el bucle del juego
- Sistema de puntuación simple con contadores de intentos y aciertos
- Verificación flexible que acepta múltiples formas de respuesta por animal (formal e informal)
- Manejo de entrada del usuario con verificación case-insensitiveos sonidos que hacen los animales en español.

## Descripción

Esta aplicación te ayuda a aprender los sonidos de diversos animales y categorías de animales en español. El programa selecciona aleatoriamente un animal o categoría y te pide que escribas el sonido correspondiente. Es perfecta para estudiantes de español, niños o cualquier persona interesada en la naturaleza.

**🚀 Acceso global**: Una vez configurado, puedes ejecutar `animals` desde cualquier directorio del sistema.

## Características

- **Más de 40 animales y categorías**: Incluye animales individuales y grupos categorizados por sonidos similares (ej. "insectos voladores" hacen "zumbido").
- **Respuestas flexibles**: Acepta sustantivos, verbos infinitivos y formas coloquiales (ej. "ladrido", "ladrar" o "ladra" para el perro).
- **Interfaz interactiva**: Preguntas aleatorias con retroalimentación inmediata.
- **Pantalla limpia**: La terminal se limpia automáticamente antes de mostrar el mensaje de bienvenida.
- **Sistema de puntuación**: Rastrea tus intentos y respuestas correctas.
- **Salida fácil**: Escribe 'quit' o 'q' para salir en cualquier momento.
- **Solo librería estándar**: No requiere instalación de paquetes adicionales.
- **Comentarios detallados**: Código bien documentado para facilitar el aprendizaje.

## Requisitos

- Python 3.6 o superior
- Solo utiliza la librería estándar de Python (random, sys)

## Instalación

1. Clona o descarga el archivo `animal_sounds.py`
2. Asegúrate de tener Python 3 instalado en tu sistema
3. **Para acceso global (opcional)**: Ejecuta el comando desde cualquier directorio usando `animals`

### Configuración de acceso global

Si seguiste los pasos de instalación global, puedes ejecutar el juego desde cualquier directorio:

```bash
animals
```

Si no configuraste el acceso global, ejecuta:

```bash
python3 animal_sounds.py
```

## Ejemplo de uso

```
[Terminal limpia - sin texto anterior visible]

¡Bienvenido a la aplicación de sonidos de animales!
Escribe 'quit' o 'q' en cualquier momento para salir.

¿Cuál es el sonido que hace el/la perro? ladra
¡Correcto!

¿Cuál es el sonido que hace el/la gato? maullar
¡Correcto!

¿Cuál es el sonido que hace el/la vaca? muge
¡Correcto!

¿Cuál es el sonido que hace el/la caballo? relincho
¡Correcto!

¿Cuál es el sonido que hace el/la rana? croa
¡Correcto!

¿Cuál es el sonido que hace el/la elefante? barrita
¡Correcto!

¿Cuál es el sonido que hace el/la insectos voladores? zumba
¡Correcto!

¿Cuál es el sonido que hace el/la loro? parlotea
¡Correcto!

¿Cuál es el sonido que hace el/la lobo? aúlla
¡Correcto!

¿Cuál es el sonido que hace el/la grillo? chirría
¡Correcto!

¿Cuál es el sonido que hace el/la reptil? sisea
Incorrecto – las respuestas correctas son 'siseo' o 'sisear' o 'sisea'

quit

¡Gracias por jugar!
Puntuación final: 10/11 correctas
```

## Lista de animales incluidos

### Animales individuales:
- perro, gato, vaca, caballo, oveja, cerdo, gallina, gallo, pato, ganso
- elefante, león, tigre, oso, mono, águila, búho, rana, serpiente
- mosquito, abeja, delfín, ballena, cocodrilo, pájaro, cuervo, paloma
- loro, canario, lobo, zorro, conejo, ratón, ardilla, ciervo, jabalí
- grillo, saltamontes, avispa, mosca, culebra, víbora

### Categorías:
- insectos voladores (zumbido)
- aves pequeñas (trino)
- felinos grandes (rugido)
- reptiles (siseo)
- mamíferos pequeños (chillido)
- aves acuáticas (graznido)
- insectos (chirrido)
- mamíferos grandes (gruñido)

## Estructura del código

- `ANIMALES`: Diccionario que contiene los animales/categorías y listas de sonidos válidos (sustantivo, verbo y formas coloquiales)
- `main()`: Función principal que maneja el bucle del juego
- Sistema de puntuación simple con contadores de intentos y aciertos
- Verificación flexible que acepta múltiples formas de respuesta por animal
- Manejo de entrada del usuario con verificación case-insensitive

## Personalización

Puedes modificar el diccionario `ANIMALES` para:
- Agregar más animales
- Cambiar sonidos
- Añadir nuevas categorías
- Adaptar para otros idiomas

## Solución de problemas

### El comando `animals` no se encuentra
Si después de la instalación global el comando no funciona:

1. **Recarga la configuración de zsh**:
   ```bash
   source ~/.zshrc
   ```

2. **Verifica que el comando esté en PATH**:
   ```bash
   which animals
   ```

3. **Verifica que el script sea ejecutable**:
   ```bash
   ls -la ~/bin/animals
   ```

4. **Si no funciona, usa el método local**:
   ```bash
   python3 animal_sounds.py
   ```

### El script no encuentra Python 3
Asegúrate de que Python 3 esté instalado y disponible en el PATH:
```bash
python3 --version
```
