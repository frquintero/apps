"""Prompt building and content extraction utilities for PAEP-R simplified system"""
import re
from typing import Dict, Any, Optional


def build_prompt(phase: Dict[str, Any], input_data: Dict[str, Any], system_prompt: str, context: str, phase_tags: Dict[str, str]) -> str:
    """Construct the prompt string for a given phase with accumulated context."""
    prompt_parts = []
    
    # For Fase A, include the user question and modifications (if any)
    if phase.get('id') == 'A':
        user_question = input_data.get('pregunta_usuario', 'N/A')
        prompt_parts.append(f"Pregunta del usuario: {user_question}")
        
        # If there are user modifications/suggestions, add them
        if 'modificaciones_usuario' in input_data:
            modifications = input_data.get('modificaciones_usuario', '')
            prompt_parts.append(f"Modificaciones solicitadas por el usuario: {modifications}")
        
        prompt_parts.append("")
    
    # Add accumulated context if any
    if context:
        prompt_parts.append(context)
        prompt_parts.append("")
    
    # Add task
    prompt_parts.append("<task>")
    prompt_parts.append(phase.get('task', ''))
    prompt_parts.append("</task>")
    
    return "\n".join(prompt_parts)


def extract_content_from_tags(response: str, phase_tags: Dict[str, str], phase_id: str) -> Optional[str]:
    """Extract content from LLM response. Now simply returns the full response since we removed XML tags."""
    if response and response.strip():
        return response.strip()
    return None


def build_context_string(phase_outputs: Dict[str, str], phase_tags: Dict[str, str], up_to_phase: str) -> str:
    """Build the accumulated context string up to a specific phase."""
    context_parts = []
    
    # Phase order for PAEP-R
    phase_order = ['A', '0', '1', '2', '3', '4', '5', '6']
    
    for phase_id in phase_order:
        if phase_id in phase_outputs and phase_id != up_to_phase:
            content = phase_outputs[phase_id]
            # Simply add content with a clear separator, no XML tags needed
            context_parts.append(f"=== FASE {phase_id} ===\n{content}")
        
        # Stop when we reach the target phase
        if phase_id == up_to_phase:
            break
    
    return "\n\n".join(context_parts)
