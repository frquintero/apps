# PAEP-R: Protocolo de Análisis Epistemológico Profundo Revisado

Sistema de análisis filosófico y epistemológico que genera insights originales y disruptivos a través de un proceso estructurado de 7 fases.

## 🎯 Características Principales

- **Análisis Multi-Conceptual**: Mantiene el foco en todos los conceptos de la pregunta original
- **Sistema de Tags**: Extracción flexible de contenido mediante etiquetas XML semánticas
- **Context Propagation**: Acumulación inteligente de contexto entre fases
- **Debug System**: Visualización completa de prompts y respuestas del LLM
- **Modular Architecture**: Separación clara entre engine, prompting, y LLM client

## 🏗️ Arquitectura

```
paep/
├── engine.py          # Orquestación principal del sistema
├── prompting.py       # Construcción de prompts y extracción de contenido
├── llm_client.py      # Cliente Groq con capacidades de debug
└── __init__.py        # Inicialización del módulo

paep_template.json     # Configuración de fases y system prompt
paep_engine.py         # CLI principal
```

## 🚀 Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar API key de Groq:
```bash
export GROQ_API_KEY="tu_api_key_aqui"
```

4. **(Opcional)** Crear comando global:
```bash
chmod +x paep-cli
ln -sf "$(pwd)/paep-cli" ~/.local/bin/paep
```

## 💻 Uso

### Comando Global (Recomendado)
Si instalaste el comando global, puedes usar `paep` desde cualquier directorio:
```bash
paep                    # Modo básico
paep --debug           # Modo debug
paep --interactive     # Modo interactivo
```

**📁 El archivo de resultados se guardará en el directorio desde donde ejecutes el comando.**

### Comando Local
**Importante**: Siempre activar el entorno virtual antes de usar el sistema:
```bash
source venv/bin/activate
```

### Modo Básico
```bash
python paep_engine.py
```

### Modo Debug (muestra prompts y respuestas completas)
```bash
python paep_engine.py --debug
```

### Modo Interactivo
```bash
python paep_engine.py --interactive
```

## 📋 Las 7 Fases del PAEP-R

| Fase | Nombre | Propósito |
|------|--------|-----------|
| **A** | Re-encuadre Contextual | Reformulación crítica de la pregunta |
| **0** | Corrientes Internas | Identificación de marcos teóricos relevantes |
| **1** | Deconstrucción Radical | Destrucción de supuestos interrelacionales |
| **2** | Inmersión Conceptual | Análisis disciplinar integrado |
| **3** | Conexiones Disruptivas | Enlaces entre campos aparentemente no relacionados |
| **4** | Tesis Provocativa | Síntesis falsable y controversial |
| **5** | Auto-Crítica | Stress-test de la propia tesis |
| **6** | Legado de Ruina | Implicaciones y nueva pregunta emergente |

## 🔧 Configuración

El sistema usa `paep_template.json` para configurar:
- **System prompt**: Instrucciones meta-cognitivas aplicadas a todas las fases
- **Phase tasks**: Tareas específicas de cada fase
- **Phase tags**: Etiquetas XML para extracción de contenido
- **Model config**: Configuración del LLM (temperatura, max_tokens, etc.)

## 📊 Outputs

El sistema genera archivos Markdown con estructura clara:
- Timestamp y metadata de sesión
- Contenido etiquetado por fase
- Análisis integrado y multi-conceptual
- Referencias y justificaciones rigurosas

## 🎭 Principios del Sistema

1. **Foco Multi-Conceptual**: Nunca reduce análisis complejos a un solo concepto
2. **Rigor Argumentativo**: Cita pensadores específicos y teorías contraintuitivas
3. **Provocación Intelectual**: Prioriza novedad sobre corrección política académica
4. **Conexiones Disruptivas**: Busca enlaces inesperados entre campos diversos
5. **Falsabilidad**: Genera tesis verificables y controversiales

## 🧪 Desarrollo y Debug

Para desarrolladores que quieran extender el sistema:

```python
from paep import PAEPEngine, LLMClient

# Inicializar con debug
llm = LLMClient(api_key="tu_key", debug=True)
engine = PAEPEngine(llm)

# Ejecutar análisis
result = engine.run_full_analysis("tu_pregunta", "paep_template.json")
```

## 📈 Estado del Proyecto

- ✅ Sistema modular funcional
- ✅ Extracción por tags XML
- ✅ Context propagation
- ✅ Debug system completo
- ✅ Multi-concept focus
- ✅ System prompt integration

---

*Desarrollado para generar insights epistemológicos profundos y disruptivos*
