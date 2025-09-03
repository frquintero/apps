#!/usr/bin/env python3
"""Script para probar el sistema PAEP-R con debug habilitado"""

import sys
import os
from pathlib import Path

# Add paep to path
sys.path.insert(0, str(Path(__file__).parent))

from paep.engine import PAEPEngine
from paep.llm_client import LLMClient

def test_debug_mode():
    """Test del modo debug con una pregunta simple"""
    
    # Verificar API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable not set!")
        print("💡 Set it with: export GROQ_API_KEY='your-api-key-here'")
        return False
    
    # Crear cliente LLM con debug habilitado
    llm = LLMClient(api_key=api_key, debug=True)
    engine = PAEPEngine(llm)
    
    # Cargar template
    script_dir = Path(__file__).parent
    template_path = script_dir / "paep_template.json"
    template = engine.load_template(str(template_path))
    
    if not template:
        print("❌ No se pudo cargar el template")
        return False
    
    # Pregunta de prueba
    test_question = "¿Qué es la creatividad?"
    
    print("🧠 PAEP-R Debug Test")
    print("="*50)
    print(f"📝 Pregunta: {test_question}")
    print("="*50)
    print("🔍 Modo DEBUG activado - se mostrará cada prompt y respuesta")
    print("⚠️  IMPORTANTE: Presiona ESPACIO + ENTER para continuar entre fases")
    print("="*50)
    
    # Ejecutar solo las primeras 2 fases para prueba
    try:
        # Fase A
        phase_a = template['phases'][0]  # Fase A
        result_a = engine.execute_phase(phase_a, test_question, template)
        
        if not result_a:
            print("❌ Error en Fase A")
            return False
        
        # Fase 0
        phase_0 = template['phases'][1]  # Fase 0
        result_0 = engine.execute_phase(phase_0, test_question, template)
        
        if not result_0:
            print("❌ Error en Fase 0")
            return False
        
        print("\n🎉 ¡Test de debug completado exitosamente!")
        print(f"✅ Fase A resultado: {result_a['processed_output']}")
        print(f"✅ Fase 0 resultado: {result_0['processed_output']}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        return False

if __name__ == "__main__":
    success = test_debug_mode()
    if not success:
        sys.exit(1)
