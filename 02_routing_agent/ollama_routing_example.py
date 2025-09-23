"""
Ollama-Powered Routing Agent Example

This script demonstrates how to use the routing pattern with Ollama (local LLM).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core import LLMProvider, AgentConfig
import requests
import json
from typing import List, Dict, Any
from enum import Enum


class RequestType(Enum):
    """Enumeration of different request types for routing."""
    MATH = "math"
    CODE = "code"
    CREATIVE = "creative"
    FACTUAL = "factual"
    ANALYSIS = "analysis"
    GENERAL = "general"


class OllamaRouter:
    """Simple routing agent powered by Ollama"""
    
    def __init__(self, model: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.config = AgentConfig(
            provider="ollama",
            model=model,
            base_url=base_url,
            temperature=0.1,
            max_tokens=200
        )
        self.llm_provider = LLMProvider(self.config)
    
    def route_request(self, user_input: str) -> Dict[str, Any]:
        """Route a user request to the appropriate category"""
        
        classification_prompt = f"""
Analyze this user request and classify it into ONE of these categories:

1. MATH - Mathematical calculations, equations, geometry, statistics
2. CODE - Programming, software development, debugging, technical implementation  
3. CREATIVE - Writing, brainstorming, artistic tasks, content creation
4. FACTUAL - Questions seeking specific facts, definitions, explanations
5. ANALYSIS - Comparative analysis, evaluation, critical thinking tasks
6. GENERAL - General conversation, unclear requests, or mixed topics

User request: "{user_input}"

Respond with only the category name (MATH, CODE, CREATIVE, FACTUAL, ANALYSIS, or GENERAL).
"""

        try:
            response = self.llm_provider.generate(classification_prompt)
            category = response.strip().upper()
            
            # Validate response
            valid_categories = ["MATH", "CODE", "CREATIVE", "FACTUAL", "ANALYSIS", "GENERAL"]
            if category not in valid_categories:
                category = "GENERAL"
            
            return {
                "category": category,
                "confidence": 0.8,  # Default confidence for Ollama
                "reasoning": f"Classified as {category} based on content analysis"
            }
            
        except Exception as e:
            print(f"Routing failed: {e}")
            return {
                "category": "GENERAL",
                "confidence": 0.1,
                "reasoning": f"Fallback due to error: {str(e)}"
            }


class OllamaSpecializedAgent:
    """Specialized agent powered by Ollama"""
    
    def __init__(self, agent_type: str, model: str = "llama3.1:8b"):
        self.agent_type = agent_type
        self.config = AgentConfig(
            provider="ollama",
            model=model,
            base_url="http://localhost:11434",
            temperature=0.7,
            max_tokens=1000
        )
        self.llm_provider = LLMProvider(self.config)
        
        # Specialized system prompts for each agent type
        self.system_prompts = {
            "MATH": "You are a mathematics expert. Provide clear, step-by-step solutions to mathematical problems. Show your work and explain your reasoning.",
            "CODE": "You are a programming expert. Write clean, well-commented code and explain programming concepts clearly. Focus on best practices and readability.",
            "CREATIVE": "You are a creative writer. Create engaging, original content. Use vivid language and imaginative scenarios.",
            "FACTUAL": "You are a knowledgeable researcher. Provide accurate, well-sourced information. Be precise and informative.",
            "ANALYSIS": "You are an analytical thinker. Provide balanced, thoughtful analysis. Consider multiple perspectives and weigh pros and cons.",
            "GENERAL": "You are a helpful AI assistant. Provide clear, helpful responses tailored to the user's needs."
        }
    
    def process_request(self, user_input: str) -> str:
        """Process a request using the specialized agent"""
        system_prompt = self.system_prompts.get(self.agent_type, self.system_prompts["GENERAL"])
        
        try:
            response = self.llm_provider.generate(user_input, system_prompt)
            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"


def demo_ollama_routing():
    """Demonstrate Ollama-powered routing"""
    print("🦙 Ollama Routing Agent Demo")
    print("=" * 40)
    
    # Check if Ollama is available
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama is not running. Please start Ollama first.")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434")
        return
    
    # Initialize router and agents
    router = OllamaRouter()
    
    agents = {
        "MATH": OllamaSpecializedAgent("MATH"),
        "CODE": OllamaSpecializedAgent("CODE"), 
        "CREATIVE": OllamaSpecializedAgent("CREATIVE"),
        "FACTUAL": OllamaSpecializedAgent("FACTUAL"),
        "ANALYSIS": OllamaSpecializedAgent("ANALYSIS"),
        "GENERAL": OllamaSpecializedAgent("GENERAL")
    }
    
    # Test requests
    test_requests = [
        "What's 25% of 480?",
        "Write a Python function to reverse a string",
        "Create a short poem about AI",
        "What is the capital of France?",
        "Compare the pros and cons of remote work"
    ]
    
    for request in test_requests:
        print(f"\n📝 Request: {request}")
        
        # Route the request
        routing_result = router.route_request(request)
        category = routing_result["category"]
        
        print(f"🎯 Routed to: {category}")
        print(f"💭 Reasoning: {routing_result['reasoning']}")
        
        # Process with specialized agent
        if category in agents:
            print(f"\n🤖 {category} Agent Response:")
            response = agents[category].process_request(request)
            print(f"   {response[:200]}...")
        
        print("-" * 50)


def interactive_ollama_demo():
    """Interactive demo with Ollama"""
    print("🦙 Interactive Ollama Routing Demo")
    print("Type 'quit' to exit")
    print("=" * 40)
    
    router = OllamaRouter()
    agents = {
        "MATH": OllamaSpecializedAgent("MATH"),
        "CODE": OllamaSpecializedAgent("CODE"), 
        "CREATIVE": OllamaSpecializedAgent("CREATIVE"),
        "FACTUAL": OllamaSpecializedAgent("FACTUAL"),
        "ANALYSIS": OllamaSpecializedAgent("ANALYSIS"),
        "GENERAL": OllamaSpecializedAgent("GENERAL")
    }
    
    while True:
        try:
            user_input = input("\n💬 Your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Route and process
            routing_result = router.route_request(user_input)
            category = routing_result["category"]
            
            print(f"🎯 Routing to: {category}")
            
            if category in agents:
                response = agents[category].process_request(user_input)
                print(f"\n🤖 Response:\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_ollama_demo()
    else:
        demo_ollama_routing()