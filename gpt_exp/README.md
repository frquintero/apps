# GPT Experiments - PAEP-R Engine

This folder contains experiments with GPT models and the PAEP-R (Protocolo de Análisis Epistemológico Profundo Revisado) system, a sophisticated multi-phase epistemological analysis tool.

## Overview

PAEP-R is a structured protocol for deep epistemological analysis that uses Large Language Models (LLMs) to perform comprehensive analysis of complex questions through multiple interconnected phases. The system is designed to generate original insights, challenge assumptions, and explore conceptual connections across disciplines.

**Recent Updates (September 2025):**
- ✅ **Simplified Architecture**: Complete removal of XML tag parsing for improved reliability
- ✅ **Enhanced Stability**: Direct response handling eliminates parsing errors and inconsistencies
- ✅ **Streamlined Processing**: Faster execution with reduced complexity
- ✅ **Maintained Functionality**: All core features preserved while improving robustness

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

### Key Improvements (September 2025)

- **Simplified Content Extraction**: Removed XML tag dependencies for more reliable parsing
- **Direct Response Processing**: LLM responses are processed directly without complex parsing
- **Enhanced Error Handling**: Better handling of edge cases and malformed responses
- **Faster Execution**: Reduced processing overhead from XML parsing elimination

## PAEP-R Analysis Phases

The system performs analysis through 8 sequential phases with **mandatory interactive reformulation validation**:

1. **A: Re-encuadre Contextual** - Reformulate the question eliminating biases and ambiguities
   - **Interactive Validation**: After reformulation, the user is prompted to approve, modify, or refine
   - **Bias Elimination**: System actively removes inductive, presumption, social desirability, emotional, and framing biases
   - **Refinement Loop**: User can provide specific feedback for iterative improvement
   - **Mandatory Approval**: Analysis cannot proceed without explicit user approval of the reformulation
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

### Required: Python Virtual Environment

**Always activate the virtual environment before running any commands:**

```bash
# Navigate to the project directory
cd gpt_exp

# Activate virtual environment (REQUIRED)
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
```

### Basic Usage

```bash
# Run full analysis with interactive reformulation validation
python paep_engine.py --question "What is the nature of consciousness?"

# Run interactively (will prompt for question)
python paep_engine.py
```

### Command Line Flags

#### Required Environment
- **Virtual Environment**: Must be activated with `source venv/bin/activate`
- **API Key**: Set `GROQ_API_KEY` environment variable

#### Available Flags

- **`--question, -q`** - Question to analyze (required unless running interactively)
  ```bash
  python paep_engine.py --question "Your question here"
  ```

- **`--template, -t`** - Path to custom template JSON file (default: paep_template.json)
  ```bash
  python paep_engine.py --question "Your question" --template custom_template.json
  ```

- **`--auto-approve`** - Skip interactive reformulation validation (for batch processing)
  ```bash
  python paep_engine.py --question "Your question" --auto-approve
  ```

- **`--verbose-llm`** - Show complete prompts and LLM responses (recommended for testing)
  ```bash
  python paep_engine.py --question "Your question" --verbose-llm
  ```

- **`--save-only`** - Save results without displaying summary
  ```bash
  python paep_engine.py --question "Your question" --save-only
  ```

### Testing Specific Phases

For testing the interactive reformulation feature with only Phase A and Phase 0:

```bash
# Activate environment first
source venv/bin/activate

# Run test with limited phases
python paep_engine.py \
    --question "¿Cómo puede la humanidad reducir efectivamente las emisiones de CO2 sin comprometer el desarrollo económico?" \
    --template paep_template_test.json \
    --verbose-llm
```

### Global Command (paep-cli)

Make the CLI globally accessible:

```bash
# Make executable
chmod +x paep-cli

# Run from anywhere (still requires API key)
paep-cli --question "Your question here"
```

**Note**: Even when using the global command, ensure your GROQ_API_KEY is set in your environment.

### Options

**Core Flags:**
- `--question, -q`: Question to analyze (required for non-interactive mode)
- `--template, -t`: Path to custom template JSON file (default: paep_template.json)

**Behavior Modifiers:**
- `--auto-approve`: Skip interactive reformulation validation (for batch processing)
- `--verbose-llm`: Show complete prompts and LLM responses (essential for debugging and testing)
- `--save-only`: Save results without displaying summary

**Important Notes:**
- Always activate virtual environment with `source venv/bin/activate` before running
- Set `GROQ_API_KEY` environment variable before use
- Interactive reformulation validation is enabled by default (use `--auto-approve` to skip)
- Use `--verbose-llm` for testing, debugging, or understanding LLM interactions

## Interactive Reformulation Feature

The system now includes **mandatory interactive validation** for question reformulation:

### How It Works

1. **Phase A Execution**: System reformulates your question, eliminating biases and ambiguities
2. **User Validation**: You review the reformulation and choose:
   - **Approve**: Continue with the reformulated question
   - **Modify**: Provide specific feedback for improvement
   - **Exit**: Stop the analysis
3. **Refinement Loop**: If you request modifications, the system refines based on your feedback
4. **Continuation**: Only user-approved reformulations proceed to subsequent phases

### Validation Options

During reformulation validation, you can:
- **Type "yes", "y", "approve", "ok"** - Accept the reformulation
- **Type "no", "n", "reject"** - Request a complete rethinking
- **Provide specific feedback** - Give detailed suggestions for improvement
- **Type "exit", "quit"** - Stop the analysis

### Testing Mode

Use the test template to focus only on reformulation and foundational knowledge:

```bash
# Activate environment
source venv/bin/activate

# Run focused test (Phase A + Phase 0 only)
python paep_engine.py \
    --question "Your test question" \
    --template paep_template_test.json \
    --verbose-llm
```

### Batch Processing

To skip interactive validation for automated processing:

```bash
python paep_engine.py \
    --question "Your question" \
    --auto-approve
```

## Template Customization

The analysis phases are defined in template JSON files:

### Available Templates

- **`paep_template.json`** - Full 8-phase analysis (default)
- **`paep_template_test.json`** - Limited testing template (Phase A + Phase 0 only)

### Creating Custom Templates

1. Copy an existing template to a new file
2. Modify the `phases` array with custom tasks
3. Update `phase_tags` for content extraction
4. Adjust `model_config` for different LLM parameters

### Template Structure

```json
{
  "template_name": "your_template_name",
  "description": "Template description",
  "system_prompt": "System instructions for the LLM",
  "phases": [
    {
      "id": "A",
      "name": "Phase Name",
      "task": "Detailed task description"
    }
  ],
  "model_config": {
    "model": "openai/gpt-oss-120b",
    "temperature": 0.8,
    "max_tokens": 4096,
    "top_p": 0.9
  }
}
```

**Note**: The `phase_tags` field is no longer required as the system processes responses directly without XML parsing.

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

- **Interactive Reformulation** - Mandatory user validation of question reformulation with bias elimination
- **Modular Architecture** - Clean separation of concerns with dedicated packages
- **Verbose Mode** - Complete transparency of LLM interactions with `--verbose-llm`
- **Template System** - Customizable analysis protocols for different use cases
- **Simplified Content Processing** - Direct response handling without XML parsing complexity
- **Context Accumulation** - Each phase builds on previous outputs for coherent analysis
- **Enhanced Error Handling** - Improved reliability and failure recovery
- **Flexible Execution** - Full analysis or targeted testing modes
- **Batch Processing** - Automated mode with `--auto-approve` for unattended execution
- **Global CLI** - Run from any directory with `paep-cli`

## Development

The system is designed for extensibility:

- Add new LLM providers by extending `LLMClient`
- Create new analysis protocols by modifying templates
- Customize prompting strategies in `prompting.py`
- Extend phase logic in `engine.py`

## Troubleshooting

### Common Issues

- **API Key Issues:** Ensure `GROQ_API_KEY` is set correctly in your environment
- **Virtual Environment:** Always activate venv with `source venv/bin/activate` before running
- **Template Errors:** Validate JSON syntax in template files using `python -m json.tool filename.json`
- **Permission Issues:** Make scripts executable with `chmod +x paep-cli`
- **Interactive Mode:** If validation prompts don't appear, ensure you're not using `--auto-approve`

### Recent Fixes (September 2025)

- ✅ **XML Parsing Issues**: Completely eliminated - no more tag parsing errors
- ✅ **Response Processing**: Direct handling of LLM responses for improved reliability
- ✅ **Phase Execution**: More stable phase transitions without parsing dependencies

### Debugging

Use `--verbose-llm` flag to see complete LLM interactions:

```bash
python paep_engine.py --question "test" --verbose-llm
```

This shows:
- Complete system and user prompts
- Model configuration details
- Full LLM responses before content extraction
- Processing steps between phases

### Environment Verification

```bash
# Check virtual environment is active
which python  # Should show path with 'venv'

# Verify API key is set
echo $GROQ_API_KEY  # Should display your key

# Test basic functionality
python paep_engine.py --question "test question" --template paep_template_test.json --auto-approve
```

## License

[Add license information if applicable]

## Contributing

[Add contribution guidelines if applicable]
