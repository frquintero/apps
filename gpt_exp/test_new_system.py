#!/usr/bin/env python3
"""Script simple para probar el nuevo sistema PAEP-R simplificado"""

import sys
import os
from pathlib import Path

# Add paep to path
sys.path.insert(0, str(Path(__file__).parent))

from paep.engine import PAEPEngine
from paep.llm_client import LLMClient

def test_new_system():
    """Test del nuevo sistema simplificado"""
    
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
    
    print("🧠 NUEVO SISTEMA PAEP-R SIMPLIFICADO")
    print("="*60)
    print(f"📝 Pregunta: {test_question}")
    print("="*60)
    print("🔍 Características del nuevo sistema:")
    print("   • Sin validación JSON rígida")
    print("   • Contenido libre entre tags")
    print("   • Contexto acumulativo con etiquetas semánticas")
    print("   • Debug completo de prompts y respuestas")
    print("="*60)
    print("⚠️  IMPORTANTE: Presiona ESPACIO + ENTER para continuar entre fases")
    print("="*60)
    
    try:
        # Ejecutar solo las primeras 3 fases para prueba
        phases_to_test = ['A', '0', '1']
        
        for i, phase_id in enumerate(phases_to_test):
            phase = next((p for p in template['phases'] if p['id'] == phase_id), None)
            if not phase:
                print(f"❌ No se encontró la fase {phase_id}")
                continue
                
            print(f"\n🎯 PROBANDO FASE {phase_id} ({i+1}/{len(phases_to_test)})")
            result = engine.execute_phase(phase, test_question, template)
            
            if not result:
                print(f"❌ Error en Fase {phase_id}")
                return False
            
            print(f"✅ Fase {phase_id} completada")
            print(f"📄 Contenido almacenado: {len(result['processed_output'])} caracteres")
        
        # Mostrar contexto acumulado
        print("\n" + "="*60)
        print("📚 CONTEXTO ACUMULADO FINAL:")
        print("="*60)
        
        from paep.prompting import build_context_string
        final_context = build_context_string(
            engine.phase_outputs, 
            template.get('phase_tags', {}), 
            '2'  # Up to fase 1 (next would be 2)
        )
        
        print(final_context)
        print("="*60)
        
        print("\n🎉 ¡Test del nuevo sistema completado exitosamente!")
        print(f"✅ Fases ejecutadas: {list(engine.phase_outputs.keys())}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_system()
    if not success:
        sys.exit(1)
