"""
Specialized Agents for the Routing Pattern

This module contains various specialized agents that handle specific types of requests
in the routing pattern implementation.
"""

import openai
from typing import Dict, Any, Optional
import re
import math
import os


class BaseSpecializedAgent:
    """Base class for all specialized agents."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize the specialized agent."""
        self.api_key = api_key
        self.client = None
        if api_key or os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.agent_type = "base"
    
    def _check_api_client(self) -> Optional[Dict[str, Any]]:
        """Check if API client is available, return error dict if not."""
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI API key not provided. Set OPENAI_API_KEY environment variable.",
                "agent_type": self.agent_type
            }
        return None

    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a request - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement process_request")


class MathAgent(BaseSpecializedAgent):
    """Specialized agent for mathematical calculations and problems."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "math"
        
        self.system_prompt = """
        You are a specialized mathematics assistant. You excel at:
        - Arithmetic calculations and algebraic equations
        - Geometry problems (area, volume, angles, etc.)
        - Statistics and probability
        - Calculus concepts and basic derivatives/integrals
        - Mathematical proofs and explanations
        
        Always show your work step-by-step and explain the mathematical concepts involved.
        When possible, verify your calculations and provide alternative solution methods.
        """
    
    def _try_simple_calculation(self, user_input: str) -> Optional[str]:
        """Try to solve simple arithmetic expressions directly."""
        # Extract simple mathematical expressions
        patterns = [
            r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',  # Addition
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)',   # Subtraction
            r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',  # Multiplication
            r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)',   # Division
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                a, b = float(match.group(1)), float(match.group(2))
                if '+' in match.group(0):
                    return f"Direct calculation: {a} + {b} = {a + b}"
                elif '-' in match.group(0):
                    return f"Direct calculation: {a} - {b} = {a - b}"
                elif '*' in match.group(0):
                    return f"Direct calculation: {a} * {b} = {a * b}"
                elif '/' in match.group(0) and b != 0:
                    return f"Direct calculation: {a} / {b} = {a / b}"
        
        # Circle area calculation
        circle_match = re.search(r'area.*circle.*radius\s*(\d+(?:\.\d+)?)', user_input.lower())
        if circle_match:
            radius = float(circle_match.group(1))
            area = math.pi * radius ** 2
            return f"Circle area calculation: π × {radius}² = {area:.2f} square units"
        
        return None
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a mathematical request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            # Try direct calculation first for simple expressions
            direct_result = self._try_simple_calculation(user_input)
            
            if direct_result:
                # Still use LLM for detailed explanation
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{user_input}\n\nI got: {direct_result}\nPlease provide a detailed mathematical explanation."}
                ]
            else:
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for mathematical precision
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "direct_calculation": direct_result,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "mathematical calculations"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }


class CodeAgent(BaseSpecializedAgent):
    """Specialized agent for programming and software development tasks."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "code"
        
        self.system_prompt = """
        You are a specialized programming assistant. You excel at:
        - Writing clean, efficient code in various programming languages
        - Debugging and troubleshooting code issues
        - Explaining programming concepts and best practices
        - Code optimization and refactoring suggestions
        - Algorithm design and data structure selection
        
        Always provide well-commented code examples and explain the logic behind your solutions.
        Consider edge cases and follow industry best practices.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a programming-related request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Slightly higher for creative solutions
                max_tokens=1500
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "programming and software development"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }


class CreativeAgent(BaseSpecializedAgent):
    """Specialized agent for creative writing and artistic tasks."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "creative"
        
        self.system_prompt = """
        You are a specialized creative writing assistant. You excel at:
        - Poetry, stories, and creative writing in various styles
        - Brainstorming unique ideas and concepts
        - Character development and world-building
        - Creative problem-solving and innovative thinking
        - Artistic descriptions and vivid imagery
        
        Focus on originality, creativity, and engaging content.
        Use rich, descriptive language and consider different artistic perspectives.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a creative request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,  # Higher temperature for creativity
                max_tokens=1200
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "creative writing and artistic tasks"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }


class FactualAgent(BaseSpecializedAgent):
    """Specialized agent for factual questions and information retrieval."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "factual"
        
        self.system_prompt = """
        You are a specialized factual information assistant. You excel at:
        - Providing accurate, well-sourced information
        - Historical facts, geographical data, and scientific information
        - Definitions and explanations of concepts
        - Current events and general knowledge (up to your training cutoff)
        - Fact-checking and verification of claims
        
        Always strive for accuracy and cite sources when possible.
        If you're uncertain about information, clearly state your confidence level.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a factual information request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,  # Low temperature for factual accuracy
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "factual information and knowledge"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }


class AnalysisAgent(BaseSpecializedAgent):
    """Specialized agent for analytical and comparative tasks."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "analysis"
        
        self.system_prompt = """
        You are a specialized analysis assistant. You excel at:
        - Comparative analysis and contrasting different options
        - Critical thinking and evaluation of pros and cons
        - Trend analysis and pattern recognition
        - Strategic thinking and decision support
        - Research methodology and systematic evaluation
        
        Provide structured, balanced analysis with clear reasoning.
        Consider multiple perspectives and potential implications.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process an analytical request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.4,  # Moderate temperature for balanced analysis
                max_tokens=1300
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "analysis and critical thinking"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }


class GeneralAgent(BaseSpecializedAgent):
    """General-purpose agent for requests that don't fit other categories."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.agent_type = "general"
        
        self.system_prompt = """
        You are a helpful general-purpose assistant. You can handle:
        - General conversation and small talk
        - Mixed requests that don't fit specific categories
        - Coordination between different types of tasks
        - Fallback handling for unclear requests
        
        Be friendly, helpful, and ask clarifying questions when needed.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a general request."""
        try:
            # Check if API client is available
            error_response = self._check_api_client()
            if error_response:
                return error_response
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Moderate temperature for natural conversation
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": assistant_response,
                "agent_type": self.agent_type,
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "specialized_for": "general conversation and mixed tasks"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.agent_type
            }