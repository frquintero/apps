#!/usr/bin/env python3
"""CLI shim for PAEP-R Engine using the refactored paep package."""

import argparse
import os
import sys
from pathlib import Path

from paep.engine import PAEPEngine
from paep.llm_client import LLMClient


def main():
    parser = argparse.ArgumentParser(description="PAEP-R Engine - Análisis Epistemológico Profundo")
    
    # Get script directory to resolve template path
    script_dir = Path(__file__).parent
    default_template = script_dir / "paep_template.json"
    
    parser.add_argument(
        "--template",
        "-t",
        default=str(default_template),
        help="Path to PAEP template JSON file"
    )
    parser.add_argument(
        "--question",
        "-q",
        required=False,
        help="Pregunta para analizar con el protocolo PAEP-R"
    )
    parser.add_argument(
        "--save-only",
        action="store_true",
        help="Solo guardar resultados, no mostrar resumen"
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Aprobar automáticamente la reformulación de la pregunta sin validación del usuario"
    )
    parser.add_argument(
        "--verbose-llm",
        action="store_true",
        help="Mostrar prompts y respuestas completas del LLM para análisis detallado"
    )

    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable not set!")
        print("💡 Set it with: export GROQ_API_KEY='your-api-key-here'")
        sys.exit(1)

    llm = LLMClient(api_key=api_key, verbose=args.verbose_llm)
    engine = PAEPEngine(llm, auto_approve=args.auto_approve, verbose=args.verbose_llm)

    # Get question from user if not provided
    question = args.question
    if not question:
        try:
            question = input("🤔 Ingresa tu pregunta para análisis PAEP-R: ").strip()
            if not question:
                print("❌ No se proporcionó ninguna pregunta.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n⏹️  Operación cancelada por el usuario")
            sys.exit(0)

    template = engine.load_template(args.template)
    if not template:
        sys.exit(1)

    try:
        results = engine.run_analysis(question, template)

        if not args.save_only:
            total_phases = len(template.get('phases', []))
            print(f"\n📊 Resumen del Análisis:")
            print(f"   • Pregunta original: {results.get('user_question')}")
            print(f"   • Fases completadas: {len(results.get('phases', {}))}/{total_phases}")
            print(f"   • Session ID: {results.get('session_id')}")
    except KeyboardInterrupt:
        print("\n⏹️  Análisis interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
