#!/usr/bin/env python3
"""Script para verificar el reemplazo de CONTEXTO_PLACEHOLDER"""

import sys
import json
from pathlib import Path

# Add paep to path
sys.path.insert(0, str(Path(__file__).parent))

from paep.prompting import build_prompt

def test_placeholder_replacement():
    """Test que verifica el reemplazo literal de CONTEXTO_PLACEHOLDER"""
    
    # Simular una fase con CONTEXTO_PLACEHOLDER
    phase = {
        "id": "1",
        "name": "Test Phase",
        "task": "CONTEXTO_PLACEHOLDER\n\nEsta es la tarea que viene después del contexto."
    }
    
    # Simular fases completadas previas
    completed_phases = {
        "A": {"pregunta_reformulada": "¿Qué es la creatividad reformulada?"},
        "0": {"corrientes_internas": [{"marco_teorico": "Test Theory", "insight_disruptivo": "Test insight"}]}
    }
    
    # Input data para la fase
    input_data = {"contexto": "placeholder"}
    
    # System prompt
    system_prompt = "Test system prompt"
    
    # Construir el prompt
    result = build_prompt(phase, input_data, system_prompt, completed_phases)
    
    print("=== RESULTADO DEL REEMPLAZO ===")
    print(result)
    print("\n=== VERIFICACIÓN ===")
    
    # Verificar que CONTEXTO_PLACEHOLDER fue reemplazado
    if "CONTEXTO_PLACEHOLDER" in result:
        print("❌ ERROR: CONTEXTO_PLACEHOLDER NO fue reemplazado")
        return False
    
    # Verificar que contiene el contexto esperado
    if "Información del contexto previo:" in result:
        print("✅ OK: El contexto fue insertado con el prefijo correcto")
    else:
        print("❌ ERROR: No se encontró el prefijo de contexto")
        return False
    
    # Verificar que contiene los datos de las fases anteriores
    if "pregunta_reformulada" in result and "corrientes_internas" in result:
        print("✅ OK: Los datos de fases anteriores están presentes")
    else:
        print("❌ ERROR: Faltan datos de fases anteriores")
        return False
    
    # Verificar que la tarea viene después del contexto
    if "Esta es la tarea que viene después del contexto." in result:
        print("✅ OK: La tarea fue preservada después del reemplazo")
    else:
        print("❌ ERROR: La tarea no fue preservada correctamente")
        return False
    
    return True

def test_phase_without_placeholder():
    """Test para fase sin CONTEXTO_PLACEHOLDER (Fase A)"""
    
    phase = {
        "id": "A",
        "name": "Phase A",
        "task": "Reformula la pregunta sin contexto previo."
    }
    
    input_data = {"pregunta_usuario": "¿Qué es la creatividad?"}
    completed_phases = {}
    system_prompt = "Test system prompt"
    
    result = build_prompt(phase, input_data, system_prompt, completed_phases)
    
    print("\n=== FASE A (SIN PLACEHOLDER) ===")
    print(result)
    
    # Verificar que incluye la pregunta del usuario
    if "¿Qué es la creatividad?" in result:
        print("✅ OK: Pregunta del usuario incluida en Fase A")
        return True
    else:
        print("❌ ERROR: Pregunta del usuario no encontrada")
        return False

if __name__ == "__main__":
    print("🔍 Verificando reemplazo de CONTEXTO_PLACEHOLDER...\n")
    
    success1 = test_placeholder_replacement()
    success2 = test_phase_without_placeholder()
    
    if success1 and success2:
        print("\n🎉 ¡Todas las verificaciones pasaron!")
    else:
        print("\n❌ Algunas verificaciones fallaron")
        sys.exit(1)
