# Animal Sounds Learning App

Una aplicación interactiva de línea de comandos escrita en Python para apr## 💡 Sistema Inteligente de Aprendizaje

La aplicación utiliza un algoritmo adaptativo que optimiza el proceso de aprendizaje:

### **Cómo funciona:**
1. **Selección inteligente**: Los animales se eligen basándose en pesos dinámicos
2. **Refuerzo positivo**: Animales acertados tienen menor probabilidad de repetirse
3. **Repaso automático**: Animales fallados se agregan a una cola de revisión
4. **Revisión programada**: Después de cada 5 preguntas, se prioriza el repaso de animales fallados

### **Beneficios:**
- ✅ **Aprendizaje eficiente**: Se enfoca en conceptos que necesitas practicar más
- ✅ **Motivación**: Menos repetición de lo que ya sabes, más práctica de lo que necesitas
- ✅ **Progreso visible**: Estadísticas finales muestran tu nivel de dominio
- ✅ **Adaptativo**: El algoritmo se ajusta a tu rendimiento en tiempo real

### **Indicadores visuales:**
- 🔄 **Repasando**: Cuando se revisa un animal previamente fallado
- 📝 **Agregado a repaso**: Cuando un animal fallado se añade a la lista de revisión
- 📊 **Estadísticas**: Nivel de dominio y animales en lista de repaso al finalizaros sonidos que hacen los animales en español.

## Descripción

Esta aplicación te ayuda a aprender los sonidos de diversos animales y categorías de animales en español. El programa selecciona aleatoriamente un animal o categoría y te pide que escribas el sonido correspondiente. Es perfecta para estudiantes de español, niños o cualquier persona interesada en la naturaleza.

**🚀 Acceso global**: Una vez configurado, puedes ejecutar `animals` desde cualquier directorio del sistema.

## Características

- **Más de 40 animales y categorías**: Incluye animales individuales y grupos categorizados por sonidos similares (ej. "insectos voladores" hacen "zumbido").
- **Respuestas flexibles**: Acepta sustantivos, verbos infinitivos y formas coloquiales (ej. "ladrido", "ladrar" o "ladra" para el perro).
- **Interfaz interactiva**: Preguntas aleatorias con retroalimentación inmediata.
- **Pantalla limpia**: La terminal se limpia automáticamente antes de mostrar el mensaje de bienvenida.
- **Sistema inteligente de aprendizaje**: Algoritmo adaptativo que ajusta la frecuencia de preguntas
- **Repaso automático**: Animales fallados se revisan después de 5 preguntas hasta acertarlos
- **Pesos dinámicos**: Animales acertados tienen menor probabilidad de repetirse

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

💡 Sistema inteligente: Los animales que aciertes tendrán menor probabilidad de repetirse.
🔄 Los que falles serán repasados después de varias preguntas.

¿Cuál es el sonido que hace el/la perro? ladra
¡Correcto! ✅

¿Cuál es el sonido que hace el/la gato? maullar
¡Correcto! ✅

¿Cuál es el sonido que hace el/la vaca? mugir
Incorrecto – las respuestas correctas son 'mugido' o 'mugir' o 'muge'
📝 vaca agregado a la lista de repaso.

¿Cuál es el sonido que hace el/la caballo? relincho
¡Correcto! ✅

¿Cuál es el sonido que hace el/la rana? croa
¡Correcto! ✅

¿Cuál es el sonido que hace el/la oveja? bala
¡Correcto! ✅

🔄 Repasando: vaca
¿Cuál es el sonido que hace el/la vaca? muge
¡Correcto! ✅

quit

¡Gracias por jugar!
Puntuación final: 6/7 correctas

📊 Estadísticas de aprendizaje:
• Animales preguntados: 6
• Animales dominados: 6
• Animales en lista de repaso: 0
• Nivel de dominio: 100.0%
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

### Error de entrada (EOFError)
Si ves un error como "EOF when reading a line":

- ✅ **Solución automática**: La aplicación maneja este error automáticamente
- 🔄 **Causa**: Suele ocurrir cuando se ejecuta sin terminal interactiva
- 💡 **Recomendación**: Ejecuta en una terminal real: `python3 animal_sounds.py`

### Interrupción del programa (Ctrl+C)
- ✅ **Manejo seguro**: La aplicación se cierra ordenadamente
- 📊 **Estadísticas**: Muestra las estadísticas finales antes de salir
- 🔄 **Continuación**: Puedes reanudar en cualquier momento
