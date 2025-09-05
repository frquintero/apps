"""Light wrapper around Groq client for sending prompts to the LLM."""
from typing import Optional, Dict, Any
from groq import Groq


class LLMError(Exception):
    pass


class LLMClient:
    def __init__(self, api_key: str, default_model: str = "openai/gpt-oss-120b", verbose: bool = False):
        self.client = Groq(api_key=api_key)
        self.default_model = default_model
        self.verbose = verbose

    def send(self, prompt: str, system_prompt: str = "", model_config: Optional[Dict[str, Any]] = None, phase_name: str = "") -> Optional[str]:
        """Send prompt to the LLM and return raw content string (or None on failure)."""
        
        # Verbose: mostrar prompt completo antes de enviar
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"🚀 ENVIANDO AL LLM - {phase_name}")
            print(f"{'='*80}")
            if system_prompt:
                print("📋 SYSTEM PROMPT:")
                print("-" * 40)
                print(system_prompt)
                print("-" * 40)
            print("📝 USER PROMPT:")
            print("-" * 40)
            print(prompt)
            print("-" * 40)
            
            # Show model config
            config = model_config or {}
            print("🤖 CONFIGURACIÓN DEL MODELO:")
            print(f"   Model: {config.get('model', self.default_model)}")
            print(f"   Temperature: {config.get('temperature', 0.8)}")
            print(f"   Max tokens: {config.get('max_tokens', 4096)}")
            print(f"   Top-p: {config.get('top_p', 0.9)}")
            print()
        
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

            # Verbose: mostrar respuesta recibida del LLM
            if self.verbose:
                print("⏳ Procesando respuesta del LLM...")
                print("📥 RESPUESTA COMPLETA DEL LLM:")
                print("-" * 40)
                if content:
                    print(content)
                else:
                    print("❌ RESPUESTA VACÍA")
                print("-" * 40)
                print()

            return content

        except Exception as e:
            if self.verbose:
                print(f"\n❌ ERROR EN FASE {phase_name}: {str(e)}")
            raise LLMError(str(e))
