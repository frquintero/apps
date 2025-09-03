# Simple Groq LLM Tester & PAEP-R Engine

A command line app suite for testing OpenAI's flagship open-weight MoE model (GPT-OSS-120B) via Groq API, including a sophisticated **PAEP-R (Protocolo de Análisis Epistemológico Profundo Revisado)** engine for deep philosophical analysis.

## Features

### Simple Tester
- Send single prompts to OpenAI's GPT-OSS-120B model via Groq
- Support for both template files and direct prompts
- Simple command line interface
- Uses Groq's ultra-fast inference (~500 tokens/second)

### PAEP-R Engine
- **7-phase iterative analysis** system for deep epistemological exploration
- **Cumulative context building** - each phase uses outputs from previous phases
- **JSON-structured outputs** for each phase
- **Provocative thesis generation** with systematic critique
- **Session tracking** and result persistence

## Setup

1. **Install dependencies:**
   ```bash
   ./setup.sh
   ```

2. **Set your Groq API key:**
   ```bash
   export GROQ_API_KEY='your-api-key-here'
   ```
   Get your API key from: https://console.groq.com/keys

## Usage

### Simple Tester

#### Using a template file:
```bash
python groq_simple_tester.py --template sample_template.json
```

#### Using a direct prompt:
```bash
python groq_simple_tester.py --prompt "Explain quantum computing in simple terms"
```

### PAEP-R Engine

#### Run deep epistemological analysis:
```bash
python paep_engine.py --question "¿Qué es la conciencia?"
```

#### Use custom template:
```bash
python paep_engine.py --question "¿Es real el libre albedrío?" --template custom_paep.json
```

#### Save results only (no summary):
```bash
python paep_engine.py --question "¿Qué es la verdad?" --save-only
```

### Help:
```bash
python groq_simple_tester.py --help
python paep_engine.py --help
```

## Template Format

The template JSON file should have this structure:

```json
{
  "template_name": "simple_prompt_test",
  "description": "Simple template for testing prompts",
  "system_prompt": "You are a helpful AI assistant.",
  "user_prompt": "Your question here",
  "model_config": {
    "model": "openai/gpt-oss-120b",
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9
  }
}
```

## Model Information

- **Model**: `openai/gpt-oss-120b` - OpenAI's flagship open-weight MoE model
- **Parameters**: 120B total parameters (20B active)
- **Context**: 131,072 tokens context window
- **Speed**: ~500 tokens per second via Groq
- **Cost**: $0.59/1M input tokens, $0.79/1M output tokens

## Example

```bash
$ python groq_simple_tester.py --prompt "What is artificial intelligence?"

✅ Groq client initialized successfully
🚀 Sending prompt to LLM...
📝 User prompt: What is artificial intelligence?
⏳ Waiting for response...

🤖 LLM Response:
==================================================
Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans...
==================================================
✅ Done!
```
