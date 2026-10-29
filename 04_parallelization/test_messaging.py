#!/usr/bin/env python3
"""
Test the improved messaging
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

def test_success_messaging():
    """Test the improved success messaging"""
    print("🧪 Testing Improved Success Messaging")
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=2)
    
    # Create 2 simple tasks that should succeed
    tasks = [
        ParallelTask(
            id="test1",
            name="Simple Math",
            prompt="What is 5 + 3? Just the number.",
            provider="gemini"
        ),
        ParallelTask(
            id="test2", 
            name="Color Question",
            prompt="Name one primary color.",
            provider="gemini"
        )
    ]
    
    print("🎯 Running 2 simple tasks that should succeed...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    print("\n📋 Expected improvement:")
    print("   ✅ Should show 'All tasks completed successfully!' instead of '❌ Failed: 0/2'")

if __name__ == "__main__":
    test_success_messaging()