"""Core PAEP engine orchestration: manages phases, state, and persistence."""
from datetime import datetime
import json
from typing import Dict, Any, Optional

from .prompting import build_prompt, extract_content_from_tags, build_context_string
from .llm_client import LLMClient, LLMError


class PAEPEngine:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.phase_outputs: Dict[str, str] = {}  # Changed to store raw content strings
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def load_template(self, template_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Template file not found: {template_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in template file: {e}")
            return None

    def build_phase_input(self, phase: Dict[str, Any], user_question: str) -> Dict[str, Any]:
        input_data = {}
        if phase.get('id') == 'A':
            input_data['pregunta_usuario'] = user_question
        # Para otras fases, no necesitamos input_data específico ya que el contexto se maneja separadamente
        return input_data

    def execute_phase(self, phase: Dict[str, Any], user_question: str, template: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        print(f"\n🔄 Ejecutando Fase {phase['id']}: {phase['name']}")
        
        # Get phase tags from template
        phase_tags = template.get('phase_tags', {})
        
        # Build input data
        input_data = self.build_phase_input(phase, user_question)
        print(f"📥 Input: {list(input_data.keys())}")

        # Build context from previous phases
        context = build_context_string(self.phase_outputs, phase_tags, phase['id'])
        
        # Build prompt with context
        prompt = build_prompt(phase, input_data, "", context, phase_tags)

        phase_name = f"{phase['id']} - {phase.get('name', 'Unnamed Phase')}"
        print(f"⏳ Enviando a LLM - Fase {phase_name}...")
        try:
            system_prompt = template.get('system_prompt', '')
            raw_response = self.llm.send(prompt, system_prompt=system_prompt, model_config=template.get('model_config'), phase_name=phase_name)
        except LLMError as e:
            print(f"❌ Error comunicando con LLM: {e}")
            return None

        if not raw_response:
            print(f"❌ Error: No se recibió respuesta del LLM para Fase {phase['id']}")
            return None

        # Extract content from tags
        if self.llm.debug:
            print(f"\n🔧 EXTRAYENDO CONTENIDO DE TAGS - FASE {phase_name}:")
            print(f"{'='*80}")

        content = extract_content_from_tags(raw_response, phase_tags, phase['id'])
        
        if self.llm.debug:
            print(f"📦 CONTENIDO EXTRAÍDO:")
            print(f"{'='*80}")
            if content:
                print(content)
            else:
                print("❌ NO SE PUDO EXTRAER CONTENIDO DE LAS TAGS")
            print(f"{'='*80}")
        
        if not content:
            print(f"❌ No se pudo extraer contenido de las tags en Fase {phase['id']}")
            print("🔍 Respuesta completa del LLM:")
            print("-" * 40)
            print(raw_response)
            print("-" * 40)
            return None

        # Store the raw content
        self.phase_outputs[phase['id']] = content

        print(f"✅ Fase {phase['id']} completada")
        return {"processed_output": content, "full_prompt": prompt, "raw_response": raw_response}

    def run_analysis(self, user_question: str, template: Dict[str, Any]) -> Dict[str, Any]:
        print(f"🚀 Iniciando análisis PAEP-R")
        print(f"📋 Template: {template.get('template_name', 'Unknown')}")
        print(f"❓ Pregunta: {user_question}")
        print(f"🆔 Session ID: {self.session_id}")
        print("=" * 80)

        results = {"session_id": self.session_id, "user_question": user_question, "template_name": template.get('template_name'), "timestamp": datetime.now().isoformat(), "phases": {}}

        for phase in template.get('phases', []):
            phase_result = self.execute_phase(phase, user_question, template)
            if phase_result is None:
                print(f"❌ Error en Fase {phase['id']}, deteniendo análisis")
                break

            input_data = self.build_phase_input(phase, user_question)
            content_output = phase_result['processed_output']

            results['phases'][phase['id']] = {
                'name': phase['name'],
                'input': input_data,
                'output': content_output,
                'full_prompt_sent': phase_result['full_prompt'],
                'raw_llm_response': phase_result['raw_response']
            }

        print("\n" + "=" * 80)
        print("🎉 ¡Análisis PAEP-R completado!")
        self.save_results(results)
        return results

    def save_results(self, results: Dict[str, Any]) -> None:
        filename = f"paep_resultado_{self.session_id}.md"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"# Análisis PAEP-R: {results.get('user_question', 'N/A')}\n\n")
                f.write(f"**Session ID:** {results.get('session_id', 'N/A')}\n")
                f.write(f"**Timestamp:** {results.get('timestamp', 'N/A')}\n")
                f.write(f"**Template:** {results.get('template_name', 'N/A')}\n\n")
                f.write("---\n\n")
                
                # Phase results
                phase_tags = {
                    'A': 'encuadre_contextual',
                    '0': 'corrientes_internas', 
                    '1': 'deconstruccion_radical',
                    '2': 'inmersion_conceptual',
                    '3': 'conexiones_disruptivas',
                    '4': 'tesis_provocativa',
                    '5': 'auto_critica',
                    '6': 'legado_ruina'
                }
                
                phase_names = {
                    'A': 'Re-encuadre Contextual & Identificación de Umbrales Críticos',
                    '0': 'Inyección de Conocimiento Fundacional (Corrientes Internas)',
                    '1': 'Destrucción de Supuestos (Deconstrucción Radical)',
                    '2': 'Inmersión en Abismos Conceptuales (Profundización Disciplinar)',
                    '3': 'Persecución de Fantasmas Teóricos (Conexiones Forzadas Disruptivas)',
                    '4': 'Síntesis de un Monstruo Lógico (Tesis Provocativa)',
                    '5': 'Autopsia de la Propia Tesis (Stress-Test Incisivo)',
                    '6': 'Legado de la Ruina (Implicaciones y Conclusión)'
                }
                
                phases = results.get('phases', {})
                for phase_id in ['A', '0', '1', '2', '3', '4', '5', '6']:
                    if phase_id in phases:
                        phase_data = phases[phase_id]
                        phase_name = phase_names.get(phase_id, f'Fase {phase_id}')
                        tag_name = phase_tags.get(phase_id, f'fase_{phase_id}')
                        
                        f.write(f"## Fase {phase_id}: {phase_name}\n\n")
                        f.write(f"### {tag_name.replace('_', ' ').title()}\n\n")
                        f.write(f"{phase_data.get('output', 'Sin contenido')}\n\n")
                        f.write("---\n\n")
                
            print(f"💾 Resultados guardados en: {filename}")
        except Exception as e:
            print(f"⚠️  Error guardando resultados: {e}")
