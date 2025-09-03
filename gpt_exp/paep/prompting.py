"""Prompt building and content extraction utilities for PAEP-R simplified system"""
import re
from typing import Dict, Any, Optional


def build_prompt(phase: Dict[str, Any], input_data: Dict[str, Any], system_prompt: str, context: str, phase_tags: Dict[str, str]) -> str:
    """Construct the prompt string for a given phase with accumulated context."""
    prompt_parts = []
    
    # For Fase A, include the user question before the task
    if phase.get('id') == 'A':
        user_question = input_data.get('pregunta_usuario', 'N/A')
        prompt_parts.append(f"Pregunta del usuario: {user_question}")
        prompt_parts.append("")
    
    # Add accumulated context if any
    if context:
        prompt_parts.append(context)
        prompt_parts.append("")
    
    # Add task
    prompt_parts.append("<task>")
    prompt_parts.append(phase.get('task', ''))
    prompt_parts.append("</task>")
    prompt_parts.append("")
    
    # Add output instruction
    phase_id = phase.get('id')
    tag_name = phase_tags.get(phase_id, f"fase_{phase_id}")
    
    prompt_parts.extend([
        "IMPORTANTE: Tu respuesta debe ir dentro de las siguientes etiquetas:",
        f"<{tag_name}>",
        "<!-- Aquí debe ir tu respuesta completa en texto libre, NO en JSON -->",
        f"</{tag_name}>",
        "",
        "No agregues texto antes o después de estas etiquetas."
    ])
    
    return "\n".join(prompt_parts)


def extract_content_from_tags(response: str, phase_tags: Dict[str, str], phase_id: str) -> Optional[str]:
    """Extract content from output tags for a specific phase."""
    tag_name = phase_tags.get(phase_id, f"fase_{phase_id}")
    
    # Try to find content between the expected tags
    patterns = [
        f'<{tag_name}>(.*?)</{tag_name}>',  # New format: <tag_name>content</tag_name>
        f'<output json {tag_name}>(.*?)</output>',  # Legacy format
        f'<output json {tag_name}="">(.*?)</output>',  # Legacy format with empty attr
        '<output json[^>]*>(.*?)</output>',  # Fallback for any output json tag
        '<output>(.*?)</output>'  # Fallback for basic output tag
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            # Remove HTML comments
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL).strip()
            if content:
                return content
    
    return None


def build_context_string(phase_outputs: Dict[str, str], phase_tags: Dict[str, str], up_to_phase: str) -> str:
    """Build the accumulated context string up to a specific phase."""
    context_parts = []
    
    # Phase order for PAEP-R
    phase_order = ['A', '0', '1', '2', '3', '4', '5', '6']
    
    for phase_id in phase_order:
        if phase_id in phase_outputs and phase_id != up_to_phase:
            tag_name = phase_tags.get(phase_id, f"fase_{phase_id}")
            content = phase_outputs[phase_id]
            context_parts.append(f"<{tag_name}>\n{content}\n</{tag_name}>")
        
        # Stop when we reach the target phase
        if phase_id == up_to_phase:
            break
    
    return "\n\n".join(context_parts)
