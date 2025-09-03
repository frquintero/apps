#!/usr/bin/env python3
"""
Test simple para debugging Fase 0
"""

import json
import os
from groq import Groq
from datetime import datetime

def test_fase_0():
    """Test directo de la Fase 0"""
    
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    # Prompt simplificado para Fase 0
    prompt = """
Basándote exclusivamente en tu conocimiento interno, identifica y resume 3-5 corrientes de pensamiento, teorías o marcos conceptuales relevantes al tema: "¿Cómo interactúan la ignorancia y la incertidumbre para generar sorpresas inesperadas?"

Para cada corriente: (1) especifica el marco teórico o autor principal, (2) resume el insight clave que puede informar análisis subsiguientes, (3) marca explícitamente como 'conocimiento interno' sin inventar URLs o referencias específicas no verificables.

Devuelve tu respuesta en el siguiente formato JSON:

<output json="">
{
  "corrientes_internas": [
    {
      "marco_teorico": "Nombre del marco teórico o autor principal",
      "insight_disruptivo": "Insight específico que desafía ideas convencionales"
    }
  ]
}
</output>
"""
    
    print("🔍 Test Fase 0 - Debugging")
    print("=" * 50)
    print("📝 Prompt:")
    print(prompt[:200] + "...")
    print("-" * 50)
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-20b",
            temperature=0.8,
            max_tokens=4096,
            top_p=0.9
        )
        
        content = response.choices[0].message.content
        print("✅ Respuesta recibida:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        # Try to extract JSON
        import re
        json_match = re.search(r'<output json="">(.*?)</output>', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            try:
                json_data = json.loads(json_str)
                print("✅ JSON extraído exitosamente:")
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                print(f"JSON string: {json_str}")
        else:
            print("❌ No se encontró JSON en formato esperado")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_fase_0()
