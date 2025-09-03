#!/usr/bin/env python3
"""
PAEP-R Engine - Protocolo de Análisis Epistemológico Profundo Revisado
Motor iterativo para ejecutar análisis filosóficos profundos con 7 fases secuenciales
"""

import json
import argparse
import os
import sys
import re
from datetime import datetime
from groq import Groq


class PAEPEngine:
    def __init__(self, api_key):
        """Initialize the PAEP-R Engine"""
        self.client = Groq(api_key=api_key)
        self.phase_outputs = {}
        self.completed_phases = {}  # Store complete phase outputs for context building
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def load_template(self, template_path):
        """Load PAEP template configuration"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Template file not found: {template_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in template file: {e}")
            return None
    
    def build_phase_input(self, phase, user_question):
        """Build input JSON for a specific phase"""
        input_data = {}
        
        # Add user question for first phase
        if phase["id"] == "A":
            input_data["pregunta_usuario"] = user_question
        else:
            # For all other phases, we just need a contexto field
            # The actual context will be handled in build_prompt via the placeholder
            input_data["contexto"] = "placeholder"  # This will be replaced in build_prompt
        
        return input_data
    
    def build_prompt(self, phase, input_data, system_prompt):
        """Build the complete prompt for a phase"""
        prompt_parts = []
        
        # Prepare context for phases after A
        context_text = ""
        if phase['id'] != 'A' and len(self.completed_phases) > 0:
            context_parts = []
            # Include complete outputs from all completed phases
            for phase_id in ['A', '0', '1', '2', '3', '4', '5']:
                if phase_id in self.completed_phases:
                    context_parts.append(json.dumps(self.completed_phases[phase_id], ensure_ascii=False, indent=2))
            
            if context_parts:
                context_text = "Información del contexto previo:\n" + "\n\n".join(context_parts)
        
        # Handle task with context placeholder
        task_text = phase['task']
        if 'CONTEXTO_PLACEHOLDER' in task_text:
            task_text = task_text.replace('CONTEXTO_PLACEHOLDER', context_text)
        
        # Only include original question for Phase A
        if phase['id'] == 'A':
            prompt_parts.extend([
                input_data.get('pregunta_usuario', 'N/A'),
                ""
            ])
            
        # Add current phase task
        prompt_parts.extend([
            "<task>",
            task_text,
            "</task>",
            "",
            "INSTRUCCIÓN IMPORTANTE:",
            "Tu respuesta debe contener ÚNICAMENTE el JSON especificado en la etiqueta <output json>.",
            "No agregues texto adicional antes o después del JSON.",
            "El JSON debe estar correctamente formateado y ser válido.",
            "DEBES usar exactamente los nombres de campos especificados en el esquema.",
            "",
            "ESQUEMA JSON REQUERIDO para esta fase:",
        ])
        
        # Add the exact JSON schema expected
        schema_example = self.get_expected_schema_example(phase["id"])
        prompt_parts.extend([
            json.dumps(schema_example, ensure_ascii=False, indent=2),
            "",
            "IMPORTANTE: Usa exactamente estos nombres de campos, no traduzcas ni cambies los nombres.",
            "",
            '<output json="">',
            "<!-- Aquí debe ir tu respuesta JSON con los campos exactos del esquema -->",
            "</output>"
        ])
        
        return "\n".join(prompt_parts)
    
    def send_to_llm(self, prompt, model_config=None):
        """Send prompt to LLM"""
        try:
            config = model_config or {}
            
            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Request parameters
            request_params = {
                "messages": messages,
                "model": config.get("model", "openai/gpt-oss-120b"),
                "temperature": config.get("temperature", 0.8),
                "max_tokens": config.get("max_tokens", 4096),
                "top_p": config.get("top_p", 0.9),
            }
            
            # Send request
            response = self.client.chat.completions.create(**request_params)
            
            content = response.choices[0].message.content
            
            # Check if content is empty but reasoning field has content (GPT-OSS behavior)
            if (content is None or len(content) == 0) and hasattr(response.choices[0].message, 'reasoning') and response.choices[0].message.reasoning:
                reasoning_content = response.choices[0].message.reasoning
                
                # Try to extract JSON from reasoning field
                # Look for JSON patterns in reasoning
                import json
                try:
                    # Try to find JSON object patterns
                    json_patterns = [
                        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested JSON
                        r'\{.*\}',  # Any content between braces
                    ]
                    
                    for pattern in json_patterns:
                        matches = re.findall(pattern, reasoning_content, re.DOTALL)
                        for match in matches:
                            try:
                                # Test if it's valid JSON
                                json.loads(match)
                                return match
                            except json.JSONDecodeError:
                                continue
                    
                    # As a last resort, try to use the reasoning content directly
                    # if it looks like it contains the answer
                    if "corrientes_internas" in reasoning_content or "marco_teorico" in reasoning_content:
                        # This could be enhanced to construct JSON from reasoning content
                        return None
                        
                except Exception as e:
                    return None
            
            if content is None or len(content) == 0:
                return None
            else:
                print(f"🔍 DEBUG - Content preview: {content[:100]}...")
            
            return content
            
        except Exception as e:
            print(f"❌ Error communicating with LLM: {type(e).__name__}: {e}")
            print(f"🔍 DEBUG - Request params: {request_params}")
            return None
    
    def get_expected_schema_example(self, phase_id):
        """Get example JSON structure for a specific phase (STRUCTURE ONLY - content must be original)"""
        examples = {
            "A": {
                "pregunta_reformulada": "[Tu pregunta reformulada y específica aquí]"
            },
            "0": {
                "corrientes_internas": [
                    {
                        "marco_teorico": "[Nombre del marco teórico o autor principal]",
                        "insight_disruptivo": "[Insight específico que desafía ideas convencionales]"
                    },
                    {
                        "marco_teorico": "[Otro marco teórico diferente]", 
                        "insight_disruptivo": "[Otro insight disruptivo diferente]"
                    }
                ]
            },
            "1": {
                "pregunta_reformulada": "[La pregunta reformulada de la Fase A]",
                "deconstruccion": [
                    {
                        "supuesto_oculto": "[Supuesto que normalmente se da por sentado]",
                        "bomba_logica": "[Pregunta o idea que destruiría este supuesto]"
                    }
                ]
            },
            "2": {
                "supuesto_elegido": "[El supuesto más frágil de la Fase 1]",
                "inmersión_conceptual": {
                    "perspectiva": "[Disciplina específica y pensador]",
                    "concepto_contraintuitivo": "[Concepto que desafía el sentido común]",
                    "grieta_conceptual": {
                        "ontologica": "[Qué ES según esta perspectiva]",
                        "epistemologica": "[Cómo se CONOCE según esta perspectiva]",
                        "axiologica": "[Qué VALORES implica esta perspectiva]"
                    }
                }
            },
            "3": {
                "conexiones_disruptivas": [
                    {
                        "campo_disruptivo": "[Campo aparentemente no relacionado]",
                        "concepto_prestado": "[Concepto específico de ese campo]",
                        "conexión_forzada_justificada": "[Explicación rigurosa de la conexión]"
                    }
                ]
            },
            "4": {
                "tesis_provocativa": "[Declaración falsable y provocativa]",
                "argumento_nuclear": "[El argumento central en una frase]",
                "filtro_originalidad": "[Cómo evitaste ideas obvias]"
            },
            "5": {
                "auto_crítica": [
                    {
                        "experimento_mental": "[Experimento que podría refutar tu tesis]",
                        "pensador_crítico": "[Nombre del pensador que haría esta crítica]",
                        "iteracion_respuesta": "[Tu defensa ante esta crítica específica]"
                    }
                ]
            },
            "6": {
                "nuevo_estado_del_arte": "[Cómo cambia el panorama después de este análisis]",
                "pregunta_emergente": "[La nueva pregunta que surge]",
                "evaluacion_plausibilidad": {
                    "nivel": "[Alto/Medio/Bajo/Plausible/Especulativo]",
                    "razon": "[Justificación del nivel asignado]"
                },
                "declaración_final": "[Declaración memorable que capture las implicaciones]"
            }
        }
        return examples.get(phase_id, {})

    def validate_phase_output(self, phase_id, json_output):
        """Validate JSON output matches expected schema for each phase"""
        expected_schemas = {
            "A": {"pregunta_reformulada": str},
            "0": {"corrientes_internas": list},
            "1": {"pregunta_reformulada": str, "deconstruccion": list},
            "2": {"supuesto_elegido": str, "inmersión_conceptual": dict},
            "3": {"conexiones_disruptivas": list},
            "4": {"tesis_provocativa": str, "argumento_nuclear": str, "filtro_originalidad": str},
            "5": {"auto_crítica": list},
            "6": {"nuevo_estado_del_arte": str, "pregunta_emergente": str, "evaluacion_plausibilidad": dict, "declaración_final": str}
        }
        
        if phase_id not in expected_schemas:
            print(f"⚠️  No hay esquema definido para Fase {phase_id}")
            return True
        
        schema = expected_schemas[phase_id]
        
        if not isinstance(json_output, dict):
            print(f"❌ Fase {phase_id}: Se esperaba un objeto JSON, recibido {type(json_output)}")
            print(f"💡 Ejemplo esperado:")
            print(json.dumps(self.get_expected_schema_example(phase_id), ensure_ascii=False, indent=2))
            return False
        
        # Check required fields
        missing_fields = []
        wrong_types = []
        
        for field, expected_type in schema.items():
            if field not in json_output:
                missing_fields.append(field)
            elif not isinstance(json_output[field], expected_type):
                wrong_types.append(f"{field} (esperado {expected_type.__name__}, recibido {type(json_output[field]).__name__})")
        
        if missing_fields:
            print(f"❌ Fase {phase_id}: Campos faltantes: {missing_fields}")
            print(f"💡 Ejemplo esperado:")
            print(json.dumps(self.get_expected_schema_example(phase_id), ensure_ascii=False, indent=2))
            return False
        
        if wrong_types:
            print(f"❌ Fase {phase_id}: Tipos incorrectos: {wrong_types}")
            print(f"💡 Ejemplo esperado:")
            print(json.dumps(self.get_expected_schema_example(phase_id), ensure_ascii=False, indent=2))
            return False
        
        print(f"✅ Fase {phase_id}: JSON válido con esquema correcto")
        return True

    def extract_json_from_response(self, response):
        """Extract JSON from LLM response"""
        try:
            # Primary method: Look for JSON between <output json=""> and </output>
            json_match = re.search(r'<output json="">(.*?)</output>', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                # Remove any comments or extra text
                json_str = re.sub(r'<!--.*?-->', '', json_str, flags=re.DOTALL).strip()
                if json_str:
                    return json.loads(json_str)
            
            # Secondary method: Look for JSON block with code fences
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                return json.loads(json_str)
            
            # Tertiary method: Look for any JSON-like structure (object starting with {)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # Last resort: Try to parse entire response as JSON
            response_clean = response.strip()
            if response_clean.startswith('{') and response_clean.endswith('}'):
                return json.loads(response_clean)
            
            # No valid JSON found
            print("⚠️  No se encontró JSON válido en la respuesta")
            return None
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing JSON: {e}")
            print(f"🔍 Contenido que se intentó parsear:")
            print("-" * 40)
            # Show the problematic JSON attempt
            if 'json_str' in locals():
                print(json_str[:300] + "..." if len(json_str) > 300 else json_str)
            else:
                print(response[:300] + "..." if len(response) > 300 else response)
            print("-" * 40)
            return None
    
    def execute_phase(self, phase, user_question, template):
        """Execute a single phase of the PAEP protocol"""
        print(f"\\n🔄 Ejecutando Fase {phase['id']}: {phase['name']}")
        
        # Build input for this phase
        input_data = self.build_phase_input(phase, user_question)
        print(f"📥 Input: {list(input_data.keys())}")
        
        # Build prompt
        prompt = self.build_prompt(phase, input_data, template["system_prompt"])
        
        print("⏳ Enviando a LLM...")
        
        # Send to LLM
        response = self.send_to_llm(
            prompt, 
            model_config=template.get("model_config")
        )
        
        if not response:
            print(f"❌ Error: No se recibió respuesta del LLM para Fase {phase['id']}")
            return None
        
        # Extract JSON output
        json_output = self.extract_json_from_response(response)
        if not json_output:
            print(f"❌ No se pudo extraer JSON válido de la respuesta en Fase {phase['id']}")
            print(f"🔍 Respuesta completa del LLM:")
            print("-" * 40)
            print(response)
            print("-" * 40)
            return None
        
        # Validate JSON schema for this phase
        if not self.validate_phase_output(phase["id"], json_output):
            print(f"❌ JSON no cumple con el esquema esperado para Fase {phase['id']}")
            print(f"JSON recibido: {json.dumps(json_output, ensure_ascii=False, indent=2)}")
            return None
        
        # Store outputs for next phases
        if isinstance(json_output, dict):
            # Store individual fields for build_phase_input() logic
            for key, value in json_output.items():
                self.phase_outputs[key] = value
            # Store complete phase output for context building
            self.completed_phases[phase['id']] = json_output
        
        print(f"✅ Fase {phase['id']} completada")
        print(f"📤 Output keys: {list(json_output.keys()) if isinstance(json_output, dict) else 'N/A'}")
        
        # Return both the processed JSON output and the raw data for logging
        return {
            "processed_output": json_output,
            "full_prompt": prompt,
            "raw_response": response
        }
    
    def run_analysis(self, user_question, template):
        """Run complete PAEP-R analysis"""
        print(f"🚀 Iniciando análisis PAEP-R")
        print(f"📋 Template: {template.get('template_name', 'Unknown')}")
        print(f"❓ Pregunta: {user_question}")
        print(f"🆔 Session ID: {self.session_id}")
        print("=" * 80)
        
        results = {
            "session_id": self.session_id,
            "user_question": user_question,
            "template_name": template.get("template_name"),
            "timestamp": datetime.now().isoformat(),
            "phases": {}
        }
        
        # Execute each phase
        for phase in template["phases"]:
            phase_result = self.execute_phase(phase, user_question, template)
            
            if phase_result is None:
                print(f"❌ Error en Fase {phase['id']}, deteniendo análisis")
                break
            
            # Build input data for this phase to include in results
            input_data = self.build_phase_input(phase, user_question)
            
            # Extract the processed JSON output for next phase processing
            json_output = phase_result["processed_output"]
            
            # Store complete phase information including prompts and raw responses
            results["phases"][phase["id"]] = {
                "name": phase["name"],
                "input": input_data,
                "output": json_output,
                "full_prompt_sent": phase_result["full_prompt"],
                "raw_llm_response": phase_result["raw_response"]
            }
            
            # Update phase_outputs with processed JSON for next phases
            if isinstance(json_output, dict):
                # Store individual fields for build_phase_input() logic
                for key, value in json_output.items():
                    self.phase_outputs[key] = value
                # Store complete phase output for context building
                self.completed_phases[phase["id"]] = json_output
        
        print("\\n" + "=" * 80)
        print("🎉 ¡Análisis PAEP-R completado!")
        
        # Save results
        self.save_results(results)
        
        return results
    
    def save_results(self, results):
        """Save analysis results to file"""
        filename = f"paep_analysis_{self.session_id}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 Resultados guardados en: {filename}")
        except Exception as e:
            print(f"⚠️  Error guardando resultados: {e}")
    
    def print_summary(self, results):
        """Print analysis summary"""
        print(f"\\n📊 Resumen del Análisis:")
        print(f"   • Pregunta original: {results['user_question']}")
        print(f"   • Fases completadas: {len(results['phases'])}/7")
        print(f"   • Session ID: {results['session_id']}")
        
        # Show key insights from final phases
        phases = results.get("phases", {})
        
        if "6" in phases:
            final_phase = phases["6"]["output"]
            if isinstance(final_phase, dict):
                print(f"\\n🎯 Declaración Final:")
                print(f"   {final_phase.get('declaración_final', 'N/A')}")
                
                print(f"\\n🔮 Pregunta Emergente:")
                print(f"   {final_phase.get('pregunta_emergente', 'N/A')}")
        
        print(f"\\n💾 Archivo de salida incluye:")
        print(f"   • Prompts completos enviados al LLM")
        print(f"   • Respuestas completas del LLM")
        print(f"   • JSON procesados de cada fase")
        print(f"   • Datos de entrada de cada fase")


def main():
    parser = argparse.ArgumentParser(description="PAEP-R Engine - Análisis Epistemológico Profundo")
    parser.add_argument(
        "--template",
        "-t",
        default="paep_template.json",
        help="Path to PAEP template JSON file"
    )
    parser.add_argument(
        "--question",
        "-q",
        required=True,
        help="Pregunta para analizar con el protocolo PAEP-R"
    )
    parser.add_argument(
        "--save-only",
        action="store_true",
        help="Solo guardar resultados, no mostrar resumen"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Habilitar modo debug (mostrar prompts y respuestas)"
    )
    
    args = parser.parse_args()
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable not set!")
        print("💡 Set it with: export GROQ_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize engine
    try:
        engine = PAEPEngine(api_key)
        print("✅ PAEP-R Engine inicializado")
    except Exception as e:
        print(f"❌ Error inicializando engine: {e}")
        sys.exit(1)
    
    # Load template
    template = engine.load_template(args.template)
    if not template:
        sys.exit(1)
    
    # Enable debug mode if requested
    if args.debug:
        template["debug_mode"] = True
        print("🔍 Modo debug habilitado")
    
    # Run analysis
    try:
        results = engine.run_analysis(args.question, template)
        
        if not args.save_only:
            engine.print_summary(results)
            
    except KeyboardInterrupt:
        print("\\n⏹️  Análisis interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
