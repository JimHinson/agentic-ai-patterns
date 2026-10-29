#!/usr/bin/env python3
"""
Simple test for parallelization agent - just check if basic imports work
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def test_imports():
    """Test if we can import everything"""
    try:
        from parallelization_agent import ParallelizationAgent, ParallelTask, TaskPriority
        print("✅ Imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_creation():
    """Test creating agent and tasks"""
    try:
        from parallelization_agent import ParallelizationAgent, ParallelTask
        
        agent = ParallelizationAgent(max_concurrent_tasks=1)
        task = ParallelTask(
            id="test1",
            name="Test Task",
            prompt="Say hello",
            provider="gemini"
        )
        
        agent.add_task(task)
        print("✅ Agent and task creation successful")
        return True
    except Exception as e:
        print(f"❌ Creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_task():
    """Test executing a single task"""
    try:
        from parallelization_agent import ParallelizationAgent, ParallelTask
        
        agent = ParallelizationAgent(max_concurrent_tasks=1)
        task = ParallelTask(
            id="single_test",
            name="Single Test Task",
            prompt="What is 2+2? Just give me the number.",
            provider="gemini",
            timeout=30
        )
        
        print("🧪 Testing single task execution...")
        agent.add_task(task)
        results = agent.execute_parallel(show_progress=False)
        
        if results and "single_test" in results:
            result = results["single_test"]
            if result.success:
                print(f"✅ Single task succeeded: {result.result.strip()[:50]}")
                return True
            else:
                print(f"❌ Single task failed: {result.error}")
                return False
        else:
            print("❌ No results returned")
            return False
            
    except Exception as e:
        print(f"❌ Single task test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run simple tests"""
    print("🚀 Simple Parallelization Tests")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Creation", test_basic_creation), 
        ("Single Task", test_single_task)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        if test_func():
            passed += 1
        else:
            break  # Stop on first failure
    
    print(f"\n🎯 Result: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Basic functionality works! Try the full examples.")
    else:
        print("⚠️  Fix the issues above before running full examples.")

if __name__ == "__main__":
    main()