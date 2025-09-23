"""
Core Agent Framework for Agentic AI Patterns

This module provides a unified interface for running different agentic AI patterns
with real LLM providers (OpenAI, Anthropic, etc.)
"""

import os
import json
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from dataclasses import dataclass
import logging

# Import LLM clients
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for the agent"""
    provider: str = "openai"  # openai, anthropic, gemini, litellm
    model: str = "gpt-4o-mini"  # Default model
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 120  # Increased default timeout to 2 minutes for local LLMs


class LLMProvider:
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on provider"""
        if self.config.provider == "openai" and OPENAI_AVAILABLE:
            api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key in config.")
            
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=self.config.base_url,
                timeout=self.config.timeout
            )
            
        elif self.config.provider == "anthropic" and ANTHROPIC_AVAILABLE:
            api_key = self.config.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or pass api_key in config.")
            
            self.client = anthropic.Anthropic(
                api_key=api_key,
                timeout=self.config.timeout
            )
            
        elif self.config.provider == "gemini" and GEMINI_AVAILABLE:
            api_key = self.config.api_key or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable or pass api_key in config.")
            
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(self.config.model)
            
        elif self.config.provider == "ollama" and OLLAMA_AVAILABLE:
            # Ollama doesn't need API key, just base URL (default: http://localhost:11434)
            self.base_url = self.config.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            # No client initialization needed for Ollama - we'll use requests directly
            self.client = "ollama_client"
            
        else:
            raise ValueError(f"Provider '{self.config.provider}' not available or not installed")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response using the configured LLM"""
        try:
            if self.config.provider == "openai":
                return self._openai_generate(prompt, system_prompt)
            elif self.config.provider == "anthropic":
                return self._anthropic_generate(prompt, system_prompt)
            elif self.config.provider == "gemini":
                return self._gemini_generate(prompt, system_prompt)
            elif self.config.provider == "ollama":
                return self._ollama_generate(prompt, system_prompt)
            else:
                raise ValueError(f"Generation not implemented for provider: {self.config.provider}")
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def _openai_generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using OpenAI API"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    def _anthropic_generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Anthropic API"""
        system = system_prompt or "You are a helpful AI assistant."
        
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system=system,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    def _gemini_generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Google Gemini API"""
        # Combine system prompt with user prompt if provided
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        # Configure generation settings
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens,
        )
        
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def _ollama_generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Ollama local LLM"""
        # Combine system prompt and user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Prepare Ollama API request
        payload = {
            "model": self.config.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {e}")
            raise ValueError(f"Failed to connect to Ollama at {self.base_url}: {e}")
        except Exception as e:
            logger.error(f"Ollama response parsing failed: {e}")
            raise ValueError(f"Failed to parse Ollama response: {e}")


class AgentStep:
    """Represents a single step in an agentic pattern"""
    
    def __init__(self, name: str, prompt_template: str, system_prompt: str = "", description: str = ""):
        self.name = name
        self.prompt_template = prompt_template
        self.system_prompt = system_prompt
        self.description = description
        self.execution_time = None
        self.input_data = None
        self.output_data = None
    
    def format_prompt(self, **kwargs) -> str:
        """Format the prompt template with provided variables"""
        return self.prompt_template.format(**kwargs)
    
    def execute(self, llm_provider: LLMProvider, previous_output: str = "", **kwargs) -> str:
        """Execute this step using the LLM provider"""
        start_time = datetime.now()
        
        # Store input for logging
        self.input_data = {"previous_output": previous_output, **kwargs}
        
        # Format the prompt
        formatted_prompt = self.format_prompt(previous_output=previous_output, **kwargs)
        
        # Generate response
        response = llm_provider.generate(formatted_prompt, self.system_prompt)
        
        # Store output and timing
        self.output_data = response
        self.execution_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Step '{self.name}' completed in {self.execution_time:.2f} seconds")
        
        return response


class AgentChain:
    """Manages a chain of agent steps"""
    
    def __init__(self, name: str, config: AgentConfig = None):
        self.name = name
        self.config = config or AgentConfig()
        self.llm_provider = LLMProvider(self.config)
        self.steps: List[AgentStep] = []
        self.execution_log = []
    
    def add_step(self, step: AgentStep):
        """Add a step to the chain"""
        self.steps.append(step)
    
    def execute(self, initial_input: str = "", **kwargs) -> str:
        """Execute the entire chain"""
        logger.info(f"Starting execution of chain: {self.name}")
        
        current_output = initial_input
        
        for step in self.steps:
            logger.info(f"Executing step: {step.name}")
            
            try:
                current_output = step.execute(
                    self.llm_provider,
                    previous_output=current_output,
                    **kwargs
                )
                
                # Log the execution
                self.execution_log.append({
                    "step": step.name,
                    "timestamp": datetime.now().isoformat(),
                    "execution_time": step.execution_time,
                    "input_length": len(str(step.input_data)),
                    "output_length": len(current_output),
                    "success": True
                })
                
            except Exception as e:
                logger.error(f"Error in step '{step.name}': {e}")
                self.execution_log.append({
                    "step": step.name,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "success": False
                })
                raise
        
        logger.info(f"Chain '{self.name}' completed successfully")
        return current_output
    
    def save_execution_log(self, filename: str):
        """Save execution log to file"""
        with open(filename, 'w') as f:
            json.dump(self.execution_log, f, indent=2)


# Utility functions
def create_openai_agent(model: str = "gpt-4o-mini", api_key: Optional[str] = None) -> AgentChain:
    """Create an agent with OpenAI configuration"""
    config = AgentConfig(provider="openai", model=model, api_key=api_key)
    return AgentChain("OpenAI Agent", config)


def create_anthropic_agent(model: str = "claude-3-haiku-20240307", api_key: Optional[str] = None) -> AgentChain:
    """Create an agent with Anthropic configuration"""
    config = AgentConfig(provider="anthropic", model=model, api_key=api_key)
    return AgentChain("Anthropic Agent", config)


def create_gemini_agent(model: str = "gemini-1.5-flash", api_key: Optional[str] = None) -> AgentChain:
    """Create an agent with Google Gemini configuration"""
    config = AgentConfig(provider="gemini", model=model, api_key=api_key)
    return AgentChain("Gemini Agent", config)


def list_available_providers() -> Dict[str, bool]:
    """List available LLM providers"""
    return {
        "openai": OPENAI_AVAILABLE and bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": ANTHROPIC_AVAILABLE and bool(os.getenv("ANTHROPIC_API_KEY")),
        "gemini": GEMINI_AVAILABLE and bool(os.getenv("GOOGLE_API_KEY")),
        "ollama": OLLAMA_AVAILABLE  # Ollama doesn't require API key
    }