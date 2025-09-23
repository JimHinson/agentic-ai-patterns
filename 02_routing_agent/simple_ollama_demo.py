#!/usr/bin/env python3
"""
Simple Ollama Routing Demo
Fast and reliable routing with phi3:mini
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core import LLMProvider, AgentConfig
import time

class SimpleOllamaRouter:
    """Simple, fast Ollama router"""
    
    def __init__(self):
        self.config = AgentConfig(
            provider="ollama",
            model="phi3:mini",
            timeout=30,
            max_tokens=300,
            temperature=0.1  # Low temperature for consistent classification
        )
        self.llm = LLMProvider(self.config)
        
    def classify_request(self, request: str) -> str:
        """Classify request into a category"""
        prompt = f"""Classify this request into ONE category:
MATH - calculations, equations
CODE - programming, technical
CREATIVE - writing, stories, poems  
FACTUAL - facts, definitions
GENERAL - everything else

Request: "{request}"

Respond with ONLY the category name (MATH, CODE, CREATIVE, FACTUAL, or GENERAL):"""
        
        try:
            response = self.llm.generate(prompt)
            category = response.strip().upper()
            # Validate response
            valid_categories = ["MATH", "CODE", "CREATIVE", "FACTUAL", "GENERAL"]
            if category in valid_categories:
                return category
            else:
                return "GENERAL"  # Fallback
        except Exception as e:
            print(f"Classification error: {e}")
            return "GENERAL"
    
    def process_request(self, request: str, category: str) -> str:
        """Process request with category-specific prompt"""
        
        system_prompts = {
            "MATH": "You are a math expert. Provide clear, step-by-step solutions.",
            "CODE": "You are a programming expert. Write clean, commented code.",
            "CREATIVE": "You are a creative writer. Be imaginative and engaging.",
            "FACTUAL": "You are a knowledgeable researcher. Be accurate and informative.",
            "GENERAL": "You are a helpful assistant. Be clear and concise."
        }
        
        system_prompt = system_prompts.get(category, system_prompts["GENERAL"])
        
        try:
            # Use slightly longer timeout for content generation
            config = AgentConfig(
                provider="ollama",
                model="phi3:mini",
                timeout=45,
                max_tokens=500,
                temperature=0.7
            )
            llm = LLMProvider(config)
            
            response = llm.generate(request, system_prompt)
            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"

def demo_simple_routing():
    """Demo the simple routing system"""
    print("🦙 Simple Ollama Routing Demo")
    print("Using phi3:mini for fast, reliable responses")
    print("=" * 50)
    
    router = SimpleOllamaRouter()
    
    # Test cases that should work quickly
    test_requests = [
        "What is 15 + 27?",
        "Write hello world in Python",
        "Write a haiku about coding",
        "What is the capital of Japan?",
        "How are you today?"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. 📝 Request: {request}")
        
        # Step 1: Classify
        print("   🎯 Classifying...", end=" ")
        start_time = time.time()
        category = router.classify_request(request)
        classify_time = time.time() - start_time
        print(f"→ {category} ({classify_time:.1f}s)")
        
        # Step 2: Process  
        print("   🤖 Processing...", end=" ")
        start_time = time.time()
        response = router.process_request(request, category)
        process_time = time.time() - start_time
        print(f"({process_time:.1f}s)")
        
        # Show result
        print(f"   ✅ Response: {response[:100]}...")
        print(f"   ⏱️  Total time: {classify_time + process_time:.1f}s")
        print("-" * 50)

if __name__ == "__main__":
    demo_simple_routing()