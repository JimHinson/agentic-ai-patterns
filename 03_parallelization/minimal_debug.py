#!/usr/bin/env python3
"""
Minimal debug test to isolate the NoneType issue
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

def test_minimal():
    """Test the absolute minimum"""
    try:
        from parallelization_agent import ParallelizationAgent, ParallelTask
        
        print("🧪 Creating minimal task...")
        task = ParallelTask(
            id="minimal",
            name="Minimal Task",
            prompt="Hello",
            provider="gemini"
        )
        
        print(f"   Task dependencies: {task.dependencies}")
        print(f"   Task dependencies type: {type(task.dependencies)}")
        
        agent = ParallelizationAgent(max_concurrent_tasks=1)
        
        print("🧪 Checking _can_execute_task...")
        can_execute = agent._can_execute_task(task)
        print(f"   Can execute: {can_execute}")
        
        print("🧪 Testing _execute_single_task directly...")
        result = agent._execute_single_task(task)
        print(f"   Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_minimal()