#!/usr/bin/env python3
"""
Fast Ollama Configuration Test
Optimized for speed and reliability
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_core import LLMProvider, AgentConfig
import time

def test_fast_ollama():
    """Test optimized Ollama configuration"""
    print("⚡ Fast Ollama Configuration Test")
    print("=" * 40)
    
    # Optimized config for speed
    config = AgentConfig(
        provider="ollama",
        model="phi3:mini",  # Fastest model
        base_url="http://localhost:11434",
        timeout=30,         # Short timeout
        max_tokens=500,     # Limit response length
        temperature=0.3     # Lower temperature for faster generation
    )
    
    llm_provider = LLMProvider(config)
    
    # Simple test prompts
    test_prompts = [
        "What is AI in one sentence?",
        "List 3 benefits of automation.",
        "Define machine learning briefly."
    ]
    
    total_time = 0
    successes = 0
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 Test {i}: {prompt}")
        try:
            start_time = time.time()
            response = llm_provider.generate(prompt)
            end_time = time.time()
            
            duration = end_time - start_time
            total_time += duration
            successes += 1
            
            print(f"✅ Success ({duration:.2f}s): {response[:80]}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print(f"\n📊 Results: {successes}/{len(test_prompts)} successful")
    if successes > 0:
        print(f"⏱️  Average time: {total_time/successes:.2f}s per request")
    
    return successes == len(test_prompts)

if __name__ == "__main__":
    success = test_fast_ollama()
    
    if success:
        print("\n🎉 All tests passed! Your Ollama setup is working well.")
        print("\n💡 Recommended settings for fast Ollama:")
        print("   Model: phi3:mini")
        print("   Timeout: 30-45 seconds")
        print("   Max tokens: 500-1000")
        print("   Temperature: 0.1-0.3")
        
        print("\n🚀 Try running:")
        print("   python agent_runner.py --provider ollama --model 'phi3:mini' --timeout 45 --topic 'your topic'")
    else:
        print("\n⚠️  Some tests failed. Try:")
        print("   1. Restart Ollama: ollama serve")
        print("   2. Check if models are loaded: ollama list") 
        print("   3. Try a different model: ollama run orca-mini:3b")