"""Light wrapper around Groq client for sending prompts to the LLM."""
from typing import Optional, Dict, Any
from groq import Groq


class LLMError(Exception):
    pass


class LLMClient:
    def __init__(self, api_key: str, default_model: str = "openai/gpt-oss-120b", debug: bool = False):
        self.client = Groq(api_key=api_key)
        self.default_model = default_model
        self.debug = debug

    def send(self, prompt: str, system_prompt: str = "", model_config: Optional[Dict[str, Any]] = None, phase_name: str = "") -> Optional[str]:
        """Send prompt to the LLM and return raw content string (or None on failure)."""
        
        # Debug: mostrar prompt enviado
        if self.debug:
            print(f"\n{'='*80}")
            print(f"🚀 PROMPT ENVIADO FASE {phase_name}:")
            print(f"{'='*80}")
            if system_prompt:
                print("SYSTEM PROMPT:")
                print(system_prompt)
                print(f"{'-'*40}")
            print("USER PROMPT:")
            print(prompt)
            print(f"{'='*80}")
        
        try:
            config = model_config or {}
            
            # Build messages array
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            request_params = {
                "messages": messages,
                "model": config.get("model", self.default_model),
                "temperature": config.get("temperature", 0.8),
                "max_tokens": config.get("max_tokens", 4096),
                "top_p": config.get("top_p", 0.9),
            }

            response = self.client.chat.completions.create(**request_params)
            content = response.choices[0].message.content

            # Fallback: some Groq responses may have reasoning field
            if (content is None or len(content) == 0) and hasattr(response.choices[0].message, 'reasoning'):
                reasoning_content = response.choices[0].message.reasoning
                content = reasoning_content

            # Debug: mostrar respuesta recibida RAW
            if self.debug:
                print(f"\n📥 RESPUESTA RAW COMPLETA DEL LLM - FASE {phase_name}:")
                print(f"{'='*80}")
                print("🔍 CONTENIDO EXACTO TAL COMO LO ENTREGA EL LLM:")
                print(f"{'='*80}")
                if content:
                    print(repr(content))  # repr() muestra caracteres especiales, comillas, etc.
                    print(f"{'='*80}")
                    print("🔍 CONTENIDO RENDERIZADO:")
                    print(f"{'='*80}")
                    print(content)
                else:
                    print("❌ RESPUESTA VACÍA")
                print(f"{'='*80}")
                input("🔍 Presiona ESPACIO y luego ENTER para continuar con la siguiente fase...")
                print()

            return content

        except Exception as e:
            if self.debug:
                print(f"\n❌ ERROR EN FASE {phase_name}: {str(e)}")
                input("🔍 Presiona ESPACIO y luego ENTER para continuar...")
            raise LLMError(str(e))
            raise LLMError(str(e))
