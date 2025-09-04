# GPT Experiments - PAEP-R Engine

This folder contains experiments with GPT models and the PAEP-R (Protocolo de Análisis Epistemológico Profundo Revisado) system, a sophisticated multi-phase epistemological analysis tool.

## Overview

PAEP-R is a structured protocol for deep epistemological analysis that uses Large Language Models (LLMs) to perform comprehensive analysis of complex questions through multiple interconnected phases. The system is designed to generate original insights, challenge assumptions, and explore conceptual connections across disciplines.

## Architecture

The codebase is organized as follows:

### Core Components

- **`paep/`** - Main package containing the analysis engine
  - `engine.py` - Core orchestration logic for running analysis phases
  - `llm_client.py` - Wrapper for Groq API integration
  - `prompting.py` - Utilities for building prompts and extracting content
  - `__init__.py` - Package initialization

- **`paep_engine.py`** - Main CLI application for running PAEP-R analysis
- **`paep-cli`** - Global command wrapper script for running from anywhere
- **`paep_template.json`** - Default template defining the analysis phases
- **`sample_template.json`** - Placeholder for additional templates
- **`groq_simple_tester.py`** - Simple tester for Groq API (currently empty)

### Configuration Files

- **`requirements.txt`** - Python dependencies (Groq API client)
- **`setup.sh`** - Setup script for creating virtual environment and installing dependencies
- **`.gitignore`** - Git ignore patterns

## PAEP-R Analysis Phases

The system performs analysis through 8 sequential phases:

1. **A: Re-encuadre Contextual** - Reformulate the question to highlight critical aspects
2. **0: Corrientes Internas** - Inject foundational knowledge from relevant theoretical frameworks
3. **1: Deconstrucción Radical** - Challenge hidden assumptions about concept interrelations
4. **2: Inmersión Conceptual** - Deep disciplinary analysis of concept interactions
5. **3: Conexiones Disruptivas** - Force connections with unrelated fields
6. **4: Tesis Provocativa** - Synthesize a falsifiable, uncomfortable thesis
7. **5: Auto-crítica** - Stress-test the thesis with counterarguments
8. **6: Legado de la Ruina** - Evaluate implications and formulate follow-up questions

## Installation & Setup

1. **Clone the repository** (if not already done)
2. **Navigate to this folder:**
   ```bash
   cd gpt_exp
   ```
3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
4. **Set your Groq API key:**
   ```bash
   export GROQ_API_KEY='your_api_key_here'
   ```
   Get your API key from [Groq Console](https://console.groq.com/keys)

## Usage

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run analysis with a question
python paep_engine.py --question "What is the nature of consciousness?"

# Or run interactively
python paep_engine.py
```

### Global Command (paep-cli)

Make the CLI globally accessible:

```bash
# Make executable
chmod +x paep-cli

# Run from anywhere
paep-cli --question "Your question here"
```

### Options

- `--template, -t`: Path to custom template JSON file (default: paep_template.json)
- `--question, -q`: Question to analyze
- `--save-only`: Save results without displaying summary
- `--debug, -d`: Enable debug mode (shows prompts and responses)

## Template Customization

The analysis phases are defined in `paep_template.json`. You can create custom templates by:

1. Copying `paep_template.json` to a new file
2. Modifying the `phases` array with custom tasks
3. Updating `phase_tags` for content extraction
4. Adjusting `model_config` for different LLM parameters

## Output

Results are saved as Markdown files in the current directory (or `PAEP_OUTPUT_DIR` if set):

- **Filename format:** `paep_resultado_YYYYMMDD_HHMMSS.md`
- **Content:** Complete analysis with all phases, prompts, and responses
- **Structure:** Header with metadata, then each phase with extracted content

## Dependencies

- **Python 3.7+**
- **Groq API** - For LLM interactions
- **Virtual Environment** - Recommended for dependency management

## Key Features

- **Modular Architecture** - Clean separation of concerns
- **Debug Mode** - Detailed logging of prompts and responses
- **Template System** - Customizable analysis protocols
- **Content Extraction** - Robust parsing of LLM responses using XML tags
- **Context Accumulation** - Each phase builds on previous outputs
- **Error Handling** - Graceful failure recovery
- **Global CLI** - Run from any directory

## Development

The system is designed for extensibility:

- Add new LLM providers by extending `LLMClient`
- Create new analysis protocols by modifying templates
- Customize prompting strategies in `prompting.py`
- Extend phase logic in `engine.py`

## Troubleshooting

- **API Key Issues:** Ensure `GROQ_API_KEY` is set correctly
- **Virtual Environment:** Always activate venv before running
- **Template Errors:** Validate JSON syntax in template files
- **Permission Issues:** Make scripts executable with `chmod +x`

## License

[Add license information if applicable]

## Contributing

[Add contribution guidelines if applicable]
