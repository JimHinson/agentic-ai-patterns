#!/usr/bin/env python3
"""
Agent Runner - Main script for running agentic AI patterns

This script provides a command-line interface for running different agentic AI patterns
with real LLM providers.

Usage:
    python agent_runner.py --pattern prompt_chaining --topic "AI Safety"
    python agent_runner.py --pattern prompt_chaining --provider anthropic --model claude-3-haiku-20240307
    python agent_runner.py --list-providers
    python agent_runner.py --interactive
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, Optional
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_core import AgentChain, AgentStep, AgentConfig, list_available_providers

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AgentRunner:
    """Main class for running agentic AI patterns"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config_data = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "providers": {
                "openai": {
                    "models": ["gpt-4o-mini", "gpt-4o"],
                    "default_model": "gpt-4o-mini"
                },
                "anthropic": {
                    "models": ["claude-3-haiku-20240307"],
                    "default_model": "claude-3-haiku-20240307"
                }
            },
            "generation_settings": {
                "temperature": 0.7,
                "max_tokens": 4000,
                "timeout": 30
            }
        }
    
    def create_agent_config(self, provider: str, model: str = None, **kwargs) -> AgentConfig:
        """Create agent configuration"""
        provider_config = self.config_data.get("providers", {}).get(provider, {})
        gen_settings = self.config_data.get("generation_settings", {})
        
        return AgentConfig(
            provider=provider,
            model=model or provider_config.get("default_model", "gpt-4o-mini"),
            temperature=kwargs.get("temperature", gen_settings.get("temperature", 0.7)),
            max_tokens=kwargs.get("max_tokens", gen_settings.get("max_tokens", 4000)),
            timeout=kwargs.get("timeout", gen_settings.get("timeout", 30))
        )
    
    def create_prompt_chaining_example(self, agent_config: AgentConfig) -> AgentChain:
        """Create a prompt chaining example for article creation"""
        chain = AgentChain("Article Creation Chain", agent_config)
        
        # Step 1: Research
        research_step = AgentStep(
            name="research",
            prompt_template="""Research the topic: {topic}
            
Please provide comprehensive research on this topic including:
- Key concepts and definitions
- Current state and recent developments  
- Important statistics or data points
- Notable experts or organizations in the field
- Main challenges or controversies
- Future outlook or trends

Format your response as structured research notes.""",
            system_prompt="You are an expert researcher. Provide accurate, well-structured research on any given topic.",
            description="Research the topic and gather comprehensive information"
        )
        
        # Step 2: Structure
        structure_step = AgentStep(
            name="structure",
            prompt_template="""Based on the following research, create a detailed article outline:

RESEARCH:
{previous_output}

Please create a comprehensive article outline with:
- An engaging title
- Clear section headings
- Key points for each section
- Suggested word count for each section
- Overall flow and narrative structure

Make sure the outline tells a compelling story and is well-organized.""",
            system_prompt="You are an expert content strategist. Create logical, engaging article structures.",
            description="Create a structured outline based on research"
        )
        
        # Step 3: Draft
        draft_step = AgentStep(
            name="draft",
            prompt_template="""Write a full article based on this outline:

OUTLINE:
{previous_output}

Please write a complete, engaging article that:
- Follows the outline structure
- Has a compelling introduction and conclusion
- Uses clear, accessible language
- Includes transitions between sections
- Is informative and well-researched
- Maintains reader engagement throughout

Aim for approximately 1000-1500 words.""",
            system_prompt="You are an expert writer. Create engaging, well-written articles that inform and engage readers.",
            description="Write the full article based on the outline"
        )
        
        # Step 4: Review and polish
        review_step = AgentStep(
            name="review",
            prompt_template="""Review and improve this article:

ARTICLE:
{previous_output}

Please review the article and provide an improved version that:
- Fixes any grammatical or stylistic issues
- Improves clarity and flow
- Enhances engagement and readability
- Ensures accuracy and consistency
- Adds any missing elements that would improve the article
- Maintains the original message and structure

Provide the final, polished version of the article.""",
            system_prompt="You are an expert editor. Polish and improve articles while maintaining their core message.",
            description="Review and polish the final article"
        )
        
        chain.add_step(research_step)
        chain.add_step(structure_step)
        chain.add_step(draft_step)
        chain.add_step(review_step)
        
        return chain
    
    def run_prompt_chaining(self, provider: str = "openai", model: str = None, topic: str = "Artificial Intelligence", output_file: str = None, timeout: int = None):
        """Run the prompt chaining pattern"""
        logger.info(f"Running prompt chaining with {provider} ({model or 'default model'})")
        logger.info(f"Topic: {topic}")
        
        try:
            # Create agent configuration with custom timeout if provided
            kwargs = {}
            if timeout is not None:
                kwargs['timeout'] = timeout
            config = self.create_agent_config(provider, model, **kwargs)
            
            # Create and run the chain
            chain = self.create_prompt_chaining_example(config)
            result = chain.execute(topic=topic)
            
            # Save result
            output_file = output_file or f"generated_article_{provider}_{topic.replace(' ', '_').lower()}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            # Save execution log
            log_file = output_file.replace('.md', '_log.json')
            chain.save_execution_log(log_file)
            
            logger.info(f"Article generated successfully!")
            logger.info(f"Output saved to: {output_file}")
            logger.info(f"Execution log saved to: {log_file}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error running prompt chaining: {e}")
            raise
    
    def list_providers(self):
        """List available providers and their status"""
        providers = list_available_providers()
        
        print("\n=== Available Providers ===")
        for provider, available in providers.items():
            status = "✓ Available" if available else "✗ Not available (missing API key)"
            print(f"{provider}: {status}")
            
            if provider in self.config_data.get("providers", {}):
                models = self.config_data["providers"][provider].get("models", [])
                default_model = self.config_data["providers"][provider].get("default_model", "")
                print(f"  Models: {', '.join(models)}")
                print(f"  Default: {default_model}")
        
        print("\nTo set up API keys, create a .env file from .env.example")
        print()
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n=== Agentic AI Patterns - Interactive Mode ===\n")
        
        # Show available providers
        self.list_providers()
        
        # Get user preferences
        providers = list_available_providers()
        available_providers = [p for p, available in providers.items() if available]
        
        if not available_providers:
            print("No providers available. Please set up your API keys in a .env file.")
            return
        
        print("Available providers:", ", ".join(available_providers))
        provider = input(f"Choose provider ({'/'.join(available_providers)}) [default: {available_providers[0]}]: ").strip()
        if not provider:
            provider = available_providers[0]
        
        if provider not in available_providers:
            print(f"Invalid provider: {provider}")
            return
        
        # Get model (optional)
        available_models = self.config_data.get("providers", {}).get(provider, {}).get("models", [])
        if available_models:
            print(f"Available models for {provider}: {', '.join(available_models)}")
            model = input(f"Choose model [default: auto]: ").strip() or None
        else:
            model = None
        
        # Get topic
        topic = input("Enter topic for article generation [default: Artificial Intelligence]: ").strip()
        if not topic:
            topic = "Artificial Intelligence"
        
        # Run the pattern
        try:
            self.run_prompt_chaining(provider=provider, model=model, topic=topic)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"\nError: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run agentic AI patterns with real LLMs")
    parser.add_argument("--pattern", choices=["prompt_chaining"], default="prompt_chaining",
                        help="Which pattern to run")
    parser.add_argument("--provider", choices=["openai", "anthropic", "gemini", "ollama"], default="openai",
                        help="LLM provider to use")
    parser.add_argument("--model", help="Specific model to use (optional)")
    parser.add_argument("--topic", default="Artificial Intelligence",
                        help="Topic for article generation")
    parser.add_argument("--output", help="Output file name (optional)")
    parser.add_argument("--list-providers", action="store_true",
                        help="List available providers and exit")
    parser.add_argument("--interactive", action="store_true",
                        help="Run in interactive mode")
    parser.add_argument("--config", default="config.json",
                        help="Configuration file path")
    parser.add_argument("--timeout", type=int, default=None,
                        help="Timeout in seconds (default: 120 for ollama, 30 for others)")
    
    args = parser.parse_args()
    
    runner = AgentRunner(args.config)
    
    if args.list_providers:
        runner.list_providers()
        return
    
    if args.interactive:
        runner.interactive_mode()
        return
    
    if args.pattern == "prompt_chaining":
        runner.run_prompt_chaining(
            provider=args.provider,
            model=args.model,
            topic=args.topic,
            output_file=args.output,
            timeout=args.timeout
        )
    else:
        print(f"Pattern '{args.pattern}' not implemented yet")


if __name__ == "__main__":
    main()