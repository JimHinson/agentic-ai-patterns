#!/usr/bin/env python3
"""
Debug the exact LLMProvider issue
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def test_llm_provider():
    """Test LLMProvider directly with same config as parallelization"""
    try:
        from agent_core import LLMProvider, AgentConfig
        
        print("🧪 Creating AgentConfig...")
        config = AgentConfig(
            provider="gemini",
            model=None,  # This is what parallelization_agent passes when task.model is None
            timeout=60,
            max_tokens=1000,
            temperature=0.7
        )
        
        print(f"   Config: provider={config.provider}, model={config.model}")
        
        print("🧪 Creating LLMProvider...")
        provider = LLMProvider(config)
        
        print("🧪 Generating response...")
        result = provider.generate("Hello")
        
        print(f"✅ Success: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_llm_provider()