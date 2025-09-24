#!/usr/bin/env python3
"""
Quick test of single provider parallelization
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

def quick_single_provider_test():
    """Quick test with single provider"""
    print("🧪 Quick Single Provider Test - Ollama")
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)
    
    # Create 3 different tasks for Gemini
    tasks = [
        ParallelTask(
            id="math",
            name="Math Problem",
            prompt="What is 15 * 23? Just give me the number.",
            provider="ollama"
        ),
        ParallelTask(
            id="haiku",
            name="Haiku Writing", 
            prompt="Write a haiku about computers.",
            provider="ollama"
        ),
        ParallelTask(
            id="list",
            name="Simple List",
            prompt="List 3 colors in alphabetical order.",
            provider="ollama"
        )
    ]
    
    print("🎯 Running 3 different tasks in parallel with Ollama...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    print("\n📊 Results:")
    for task_id, result in results.items():
        if result.success:
            print(f"✅ {result.task_name} ({result.execution_time:.1f}s): {result.result.strip()[:60]}...")
        else:
            print(f"❌ {result.task_name}: {result.error}")
    
    # Show summary
    summary = agent.get_task_summary()
    print(f"\n🎉 Summary: {summary['successful_tasks']}/{summary['total_tasks']} tasks successful")

if __name__ == "__main__":
    quick_single_provider_test()