#!/usr/bin/env python3
"""
Groq Template Tester - Command Line App
Tests OpenAI's flagship open-weight MoE model (GPT-OSS-120B) via Groq API
Implements iterative task-prompt algorithm for template testing
"""

import os
import sys
import json
import argparse
import time
from typing import List, Dict, Any, Optional
from groq import Groq
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TemplateStep:
    """Represents a step in the template"""
    task: str
    prompt: str
    response: Optional[str] = None
    timestamp: Optional[str] = None
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None


@dataclass
class TemplateSession:
    """Represents a complete template testing session"""
    session_id: str
    template_name: str
    model: str
    steps: List[TemplateStep]
    created_at: str
    completed_at: Optional[str] = None
    total_tokens: int = 0
    total_time: float = 0.0


class GroqTemplateTester:
    """Main class for testing templates with Groq's GPT-OSS-120B model"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-oss-120b"):
        """
        Initialize the Groq Template Tester
        
        Args:
            api_key: Groq API key (if not provided, will use GROQ_API_KEY env var)
            model: Model to use (default: openai/gpt-oss-120b)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required or pass api_key parameter")
        
        self.model = model
        self.client = Groq(api_key=self.api_key)
        self.current_session: Optional[TemplateSession] = None
        
    def create_session(self, template_name: str) -> str:
        """Create a new template testing session"""
        session_id = f"session_{int(time.time())}_{template_name}"
        self.current_session = TemplateSession(
            session_id=session_id,
            template_name=template_name,
            model=self.model,
            steps=[],
            created_at=datetime.now().isoformat()
        )
        return session_id
    
    def send_prompt(self, task: str, prompt: str, system_prompt: Optional[str] = None) -> TemplateStep:
        """
        Send a prompt to the Groq API and return the response
        
        Args:
            task: Description of the current task
            prompt: The prompt to send to the model
            system_prompt: Optional system prompt for context
            
        Returns:
            TemplateStep with the response
        """
        if not self.current_session:
            raise ValueError("No active session. Call create_session() first")
        
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            print(f"🔄 Sending task: {task}")
            print(f"📝 Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
                stream=False
            )
            
            processing_time = time.time() - start_time
            response = completion.choices[0].message.content
            tokens_used = completion.usage.total_tokens if completion.usage else 0
            
            step = TemplateStep(
                task=task,
                prompt=prompt,
                response=response,
                timestamp=datetime.now().isoformat(),
                tokens_used=tokens_used,
                processing_time=processing_time
            )
            
            self.current_session.steps.append(step)
            self.current_session.total_tokens += tokens_used
            self.current_session.total_time += processing_time
            
            print(f"✅ Response received ({tokens_used} tokens, {processing_time:.2f}s)")
            print(f"🤖 Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            print("-" * 80)
            
            return step
            
        except Exception as e:
            print(f"❌ Error sending prompt: {e}")
            step = TemplateStep(
                task=task,
                prompt=prompt,
                response=f"ERROR: {str(e)}",
                timestamp=datetime.now().isoformat(),
                processing_time=time.time() - start_time
            )
            self.current_session.steps.append(step)
            return step
    
    def run_iterative_template(self, template_config: Dict[str, Any]) -> TemplateSession:
        """
        Run an iterative template based on configuration
        
        Args:
            template_config: Configuration dictionary for the template
            
        Returns:
            Completed TemplateSession
        """
        template_name = template_config.get('name', 'unnamed_template')
        self.create_session(template_name)
        
        print(f"🚀 Starting template: {template_name}")
        print(f"📊 Model: {self.model}")
        print("=" * 80)
        
        # Get initial configuration
        system_prompt = template_config.get('system_prompt')
        initial_task = template_config.get('initial_task', 'Initial task')
        initial_prompt = template_config.get('initial_prompt', 'Please provide a response.')
        max_iterations = template_config.get('max_iterations', 5)
        
        # Send initial prompt
        current_step = self.send_prompt(initial_task, initial_prompt, system_prompt)
        iteration = 1
        
        # Iterative process
        while iteration < max_iterations and current_step.response and not current_step.response.startswith("ERROR:"):
            # Check if we have a custom iteration function
            if 'iteration_function' in template_config:
                try:
                    # Custom iteration logic
                    next_task, next_prompt = template_config['iteration_function'](
                        current_step.response, iteration, self.current_session.steps
                    )
                except Exception as e:
                    print(f"❌ Error in iteration function: {e}")
                    break
            else:
                # Default iteration logic - use previous response to build next prompt
                next_task = f"Iteration {iteration + 1}"
                next_prompt = f"Based on your previous response: '{current_step.response}', please continue and elaborate further."
            
            # Check for completion conditions
            if not next_task or not next_prompt:
                print("🏁 Template completed - no more tasks to process")
                break
                
            current_step = self.send_prompt(next_task, next_prompt, system_prompt)
            iteration += 1
        
        # Complete session
        self.current_session.completed_at = datetime.now().isoformat()
        
        print("=" * 80)
        print(f"🎉 Template completed!")
        print(f"📈 Total steps: {len(self.current_session.steps)}")
        print(f"🔢 Total tokens: {self.current_session.total_tokens}")
        print(f"⏱️  Total time: {self.current_session.total_time:.2f}s")
        
        return self.current_session
    
    def save_session(self, filename: Optional[str] = None) -> str:
        """Save the current session to a JSON file"""
        if not self.current_session:
            raise ValueError("No active session to save")
        
        if not filename:
            filename = f"{self.current_session.session_id}.json"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.current_session), f, indent=2, ensure_ascii=False)
        
        print(f"💾 Session saved to: {filepath}")
        return filepath
    
    def load_session(self, filepath: str) -> TemplateSession:
        """Load a session from a JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert steps back to TemplateStep objects
        steps = [TemplateStep(**step) for step in data['steps']]
        data['steps'] = steps
        
        session = TemplateSession(**data)
        self.current_session = session
        return session


def create_sample_template() -> Dict[str, Any]:
    """Create a sample template configuration for testing"""
    
    def sample_iteration_function(previous_response: str, iteration: int, all_steps: List[TemplateStep]) -> tuple:
        """Sample iteration function that analyzes and refines responses"""
        
        if iteration >= 3:  # Limit to 3 iterations for this sample
            return None, None
        
        tasks = [
            "Analyze and critique the previous response",
            "Provide specific improvements and alternatives",
            "Synthesize insights from all previous responses"
        ]
        
        prompts = [
            f"Please analyze this response and identify its strengths and weaknesses: '{previous_response[:500]}...'",
            f"Based on the analysis, provide 3 specific improvements or alternative approaches to: '{previous_response[:200]}...'",
            f"Now synthesize all the insights from our conversation and provide a final, comprehensive response that incorporates the best elements discussed."
        ]
        
        if iteration - 1 < len(tasks):
            return tasks[iteration - 1], prompts[iteration - 1]
        
        return None, None
    
    return {
        'name': 'sample_analysis_template',
        'system_prompt': 'You are an expert analyst and consultant. Provide thoughtful, detailed responses that demonstrate deep understanding and practical insights.',
        'initial_task': 'Initial analysis request',
        'initial_prompt': 'Please explain the key factors that make a successful software development team, focusing on both technical and human aspects.',
        'max_iterations': 4,
        'iteration_function': sample_iteration_function
    }


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Groq Template Tester - Test OpenAI GPT-OSS-120B with iterative templates'
    )
    parser.add_argument(
        '--template', '-t',
        type=str,
        help='Path to template configuration JSON file'
    )
    parser.add_argument(
        '--sample', '-s',
        action='store_true',
        help='Run with sample template'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for session results (default: auto-generated)'
    )
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='openai/gpt-oss-120b',
        help='Model to use (default: openai/gpt-oss-120b)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Groq API key (if not set in GROQ_API_KEY env var)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize tester
        tester = GroqTemplateTester(api_key=args.api_key, model=args.model)
        
        # Get template configuration
        if args.sample:
            print("🔬 Using sample template")
            template_config = create_sample_template()
        elif args.template:
            print(f"📋 Loading template from: {args.template}")
            with open(args.template, 'r', encoding='utf-8') as f:
                template_config = json.load(f)
        else:
            print("❌ Please specify either --sample or --template")
            sys.exit(1)
        
        # Run template
        session = tester.run_iterative_template(template_config)
        
        # Save results
        output_file = tester.save_session(args.output)
        
        print("\n" + "=" * 80)
        print("📋 SESSION SUMMARY")
        print("=" * 80)
        print(f"Session ID: {session.session_id}")
        print(f"Template: {session.template_name}")
        print(f"Model: {session.model}")
        print(f"Steps completed: {len(session.steps)}")
        print(f"Total tokens used: {session.total_tokens}")
        print(f"Total processing time: {session.total_time:.2f}s")
        print(f"Average tokens per second: {session.total_tokens / session.total_time:.2f}")
        print(f"Results saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
