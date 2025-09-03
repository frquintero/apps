#!/usr/bin/env python3
"""
Simple Groq LLM Tester
A command line app to send prompts to OpenAI's GPT-OSS-120B model via Groq API
"""

import json
import argparse
import os
import sys
from groq import Groq


def load_template(template_path):
    """Load template configuration from JSON file"""
    try:
        with open(template_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in template file: {e}")
        return None


def send_prompt(client, template):
    """Send a single prompt to the LLM and return the response"""
    try:
        # Prepare the messages
        messages = [
            {
                "role": "system",
                "content": template.get("system_prompt", "You are a helpful AI assistant.")
            },
            {
                "role": "user", 
                "content": template.get("user_prompt", "Hello!")
            }
        ]
        
        # Get model configuration
        model_config = template.get("model_config", {})
        
        print("🚀 Sending prompt to LLM...")
        print(f"📝 User prompt: {template.get('user_prompt', 'Hello!')}")
        print("⏳ Waiting for response...\n")
        
        # Prepare the request parameters
        request_params = {
            "messages": messages,
            "model": model_config.get("model", "openai/gpt-oss-120b"),
            "temperature": model_config.get("temperature", 0.7),
            "max_tokens": model_config.get("max_tokens", 1000),
            "top_p": model_config.get("top_p", 0.9),
        }
        
        # Send request to Groq
        chat_completion = client.chat.completions.create(**request_params)
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"❌ Error sending prompt: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Simple Groq LLM Tester")
    parser.add_argument(
        "--template", 
        "-t",
        default="sample_template.json",
        help="Path to template JSON file (default: sample_template.json)"
    )
    parser.add_argument(
        "--prompt",
        "-p", 
        help="Direct prompt to send (overrides template)"
    )
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY environment variable not set!")
        print("💡 Set it with: export GROQ_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Initialize Groq client
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("✅ Groq client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        sys.exit(1)
    
    # Handle direct prompt
    if args.prompt:
        template = {
            "system_prompt": "You are a helpful AI assistant.",
            "user_prompt": args.prompt,
            "model_config": {
                "model": "openai/gpt-oss-120b",
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9
            }
        }
    else:
        # Load template
        template = load_template(args.template)
        if not template:
            sys.exit(1)
        
        print(f"📋 Loaded template: {template.get('template_name', 'Unknown')}")
        print(f"📄 Description: {template.get('description', 'No description')}")
    
    # Send the prompt
    response = send_prompt(client, template)
    
    if response:
        print("🤖 LLM Response:")
        print("=" * 50)
        print(response)
        print("=" * 50)
        print("✅ Done!")
    else:
        print("❌ Failed to get response from LLM")
        sys.exit(1)


if __name__ == "__main__":
    main()
