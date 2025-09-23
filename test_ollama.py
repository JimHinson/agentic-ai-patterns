#!/usr/bin/env python3
"""
Simple Ollama Test Script
Test basic Ollama functionality with minimal prompts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_core import LLMProvider, AgentConfig
import time

def test_ollama_basic():
    """Test basic Ollama functionality"""
    print("🧪 Testing Ollama Basic Functionality")
    print("=" * 40)
    
    # Test with different models and timeouts
    test_cases = [
        ("phi3:mini", 30, "What is 2+2?"),
        ("orca-mini:3b", 30, "Say hello in one word."),
        ("phi3:mini", 60, "Write one sentence about AI."),
    ]
    
    for model, timeout, prompt in test_cases:
        print(f"\n📝 Testing {model} (timeout: {timeout}s)")
        print(f"Prompt: {prompt}")
        
        try:
            # Create config
            config = AgentConfig(
                provider="ollama",
                model=model,
                base_url="http://localhost:11434",
                timeout=timeout,
                max_tokens=100  # Keep response short
            )
            
            # Create provider
            llm_provider = LLMProvider(config)
            
            # Test generation
            start_time = time.time()
            response = llm_provider.generate(prompt)
            end_time = time.time()
            
            print(f"✅ Success ({end_time - start_time:.2f}s):")
            print(f"   Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print("-" * 40)


def test_ollama_chain_simple():
    """Test a simple 2-step chain"""
    print("\n🔗 Testing Simple 2-Step Chain")
    print("=" * 40)
    
    try:
        # Use fastest model with short timeout
        config = AgentConfig(
            provider="ollama",
            model="phi3:mini",
            base_url="http://localhost:11434",
            timeout=45,
            max_tokens=200
        )
        
        llm_provider = LLMProvider(config)
        
        # Step 1: Simple outline
        print("\n📋 Step 1: Create simple outline")
        outline_prompt = "Create a 3-point outline about cats. Keep it very brief."
        
        start_time = time.time()
        outline = llm_provider.generate(outline_prompt)
        step1_time = time.time() - start_time
        
        print(f"✅ Outline created ({step1_time:.2f}s):")
        print(f"   {outline[:150]}...")
        
        # Step 2: Expand one point
        print(f"\n📝 Step 2: Expand on outline")
        expand_prompt = f"Based on this outline:\n{outline}\n\nWrite 2 sentences about the first point."
        
        start_time = time.time()
        expansion = llm_provider.generate(expand_prompt)
        step2_time = time.time() - start_time
        
        print(f"✅ Expansion created ({step2_time:.2f}s):")
        print(f"   {expansion[:150]}...")
        
        print(f"\n🎉 Total time: {step1_time + step2_time:.2f}s")
        
    except Exception as e:
        print(f"❌ Chain failed: {e}")


if __name__ == "__main__":
    test_ollama_basic()
    test_ollama_chain_simple()