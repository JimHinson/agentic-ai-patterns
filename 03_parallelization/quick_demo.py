#!/usr/bin/env python3
"""
Quick demo of parallelization pattern
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

from parallelization_agent import ParallelizationAgent, ParallelTask

def quick_demo():
    """Run a quick demonstration"""
    print("🚀 Parallelization Pattern - Quick Demo")
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)
    
    # Create tasks for different providers
    tasks = [
        ParallelTask(
            id="joke_gemini",
            name="Programming Joke (Gemini)",
            prompt="Tell me a short programming joke.",
            provider="gemini"
        ),
        ParallelTask(
            id="joke_openai", 
            name="Programming Joke (OpenAI)",
            prompt="Tell me a short programming joke.",
            provider="openai"
        ),
        ParallelTask(
            id="joke_ollama",
            name="Programming Joke (Ollama)",
            prompt="Tell me a short programming joke.",
            provider="ollama",
            timeout=30
        )
    ]
    
    print(f"🎯 Running {len(tasks)} tasks in parallel across different providers...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    print("\n📊 Results from different AI providers:")
    for task_id, result in results.items():
        if result.success:
            print(f"\n✅ {result.provider_used.upper()} ({result.execution_time:.1f}s):")
            print(f"   {result.result[:200]}...")
        else:
            print(f"\n❌ {result.provider_used.upper()}: {result.error}")
    
    # Show summary
    summary = agent.get_task_summary()
    print(f"\n🎉 Demo Complete!")
    print(f"   Total tasks: {summary['total_tasks']}")
    print(f"   Successful: {summary['successful_tasks']}")
    if summary.get('fastest_task'):
        fastest = summary['fastest_task']
        print(f"   Fastest: {fastest.task_name} ({fastest.execution_time:.1f}s)")

if __name__ == "__main__":
    quick_demo()