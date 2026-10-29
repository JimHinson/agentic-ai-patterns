#!/usr/bin/env python3
"""
Debug script to check if basic agent works
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

def check_environment():
    """Check if environment variables are set"""
    print("🔍 Checking Environment Variables:")
    
    env_vars = [
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY", 
        "ANTHROPIC_API_KEY"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * 10}...{value[-4:] if len(value) > 10 else '***'}")
        else:
            print(f"  ❌ {var}: Not set")
    
    return os.getenv("GOOGLE_API_KEY") is not None

def test_agent_directly():
    """Test the agent core directly"""
    try:
        from agent_core import LLMProvider, AgentConfig
        
        print("\n🧪 Testing Agent Core Directly:")
        
        config = AgentConfig(
            provider="gemini",
            model="gemini-1.5-flash",
            timeout=30
        )
        
        provider = LLMProvider(config)
        result = provider.generate("What is 2+2? Just give me the number.")
        
        print(f"✅ Direct test successful: {result.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run debug checks"""
    print("🔧 Parallelization Debug Script")
    print("=" * 40)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n⚠️  GOOGLE_API_KEY not found. Set it in your .env file:")
        print("   GOOGLE_API_KEY=your_key_here")
        return
    
    # Test agent directly
    test_agent_directly()

if __name__ == "__main__":
    main()