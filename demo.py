#!/usr/bin/env python3
"""
Agentic AI Patterns Demo

This script demonstrates the difference between Simple Agent and Routing Agent patterns.
It works with or without an OpenAI API key - without the key, it shows routing decisions only.
"""

import os
import sys

def demo_without_api():
    """Demo that works without OpenAI API key."""
    print("🤖 Agentic AI Patterns Demo")
    print("=" * 60)
    print("⚠️  No OpenAI API key detected - showing routing logic only")
    print()
    
    # Import the routing system
    sys.path.append('02_routing_agent')
    from routing_agent import RouterAgent, RequestType
    
    print("🔄 Routing Agent Pattern - Request Classification")
    print("-" * 50)
    
    router = RouterAgent()
    
    test_requests = [
        "What's the area of a circle with radius 10?",
        "Write a Python function to sort a list",
        "Create a haiku about artificial intelligence", 
        "What is the capital of Japan?",
        "Compare the pros and cons of remote work",
        "Hello, how are you today?"
    ]
    
    for i, request in enumerate(test_requests, 1):
        decision = router.route_request(request)
        print(f"{i}. Request: {request}")
        print(f"   → Routed to: {decision.agent_id}")
        print(f"   → Type: {decision.request_type.value}")
        print(f"   → Confidence: {decision.confidence}")
        print(f"   → Reasoning: {decision.reasoning}")
        print()
    
    print("✨ Key Benefits of Routing Pattern:")
    print("   • Intelligent request classification")
    print("   • Specialized agents for better performance")
    print("   • Fallback mechanisms for reliability")
    print("   • Scalable architecture")
    print()
    print("💡 To see full functionality with LLM responses:")
    print("   1. Set your OpenAI API key: export OPENAI_API_KEY=your_key")
    print("   2. Run: python 02_routing_agent/example.py")


def demo_with_api():
    """Demo that uses OpenAI API."""
    print("🤖 Agentic AI Patterns Demo - Full Functionality")
    print("=" * 60)
    print("✅ OpenAI API key detected - showing full capabilities")
    print()
    
    # Import both patterns
    sys.path.append('01_simple_agent')
    sys.path.append('02_routing_agent')
    
    from simple_agent import SimpleAgent
    from routing_agent import RouterAgent
    from specialized_agents import MathAgent, CodeAgent, GeneralAgent
    
    print("1️⃣  Simple Agent Pattern Demo")
    print("-" * 30)
    
    simple_agent = SimpleAgent()
    result = simple_agent.process_request("What's 15% of 200?")
    
    if result["success"]:
        print(f"✅ Response: {result['response'][:100]}...")
        print(f"📊 Tokens used: {result['metadata']['tokens_used']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print()
    print("2️⃣  Routing Agent Pattern Demo")
    print("-" * 30)
    
    # Set up routing system
    router = RouterAgent()
    math_agent = MathAgent()
    code_agent = CodeAgent()
    general_agent = GeneralAgent()
    
    router.register_agent("math_agent", math_agent, [RequestType.MATH])
    router.register_agent("code_agent", code_agent, [RequestType.CODE])
    router.register_agent("general_agent", general_agent, [RequestType.GENERAL])
    
    # Process the same request through routing
    result = router.process_request("What's 15% of 200?")
    
    if result["success"]:
        print(f"✅ Routed to: {result['routing']['routed_to']}")
        print(f"🎯 Request type: {result['routing']['request_type']}")
        print(f"💬 Response: {result['response'][:100]}...")
        print(f"📊 Tokens used: {result['metadata']['tokens_used']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print()
    print("✨ Comparison:")
    print("   Simple Agent: One agent handles everything")
    print("   Routing Agent: Specialized agents for better performance")


def main():
    """Main demo function."""
    # Check if OpenAI API key is available
    if os.getenv("OPENAI_API_KEY"):
        try:
            demo_with_api()
        except Exception as e:
            print(f"Error in full demo: {e}")
            print("Falling back to routing-only demo...")
            demo_without_api()
    else:
        demo_without_api()


if __name__ == "__main__":
    main()