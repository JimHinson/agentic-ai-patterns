#!/usr/bin/env python3
"""
Quick test script for the Parallelization Pattern

Tests basic functionality with minimal tasks to verify the pattern works correctly.
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parallelization_agent import ParallelizationAgent, ParallelTask, TaskPriority


def test_basic_functionality():
    """Test basic parallelization functionality"""
    print("🧪 Testing Basic Parallelization Functionality")
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=2)
    
    # Create simple, fast tasks
    tasks = [
        ParallelTask(
            id="test1",
            name="Simple Math (Gemini)",
            prompt="What is 25 + 17? Just give me the number.",
            provider="gemini",
            model="gemini-1.5-flash"
        ),
        ParallelTask(
            id="test2",
            name="Simple Math (Ollama)",
            prompt="What is 25 + 17? Just give me the number.",
            provider="ollama", 
            model="phi3:mini",
            timeout=30
        )
    ]
    
    print(f"📝 Running {len(tasks)} simple tasks in parallel...")
    
    start_time = time.time()
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    total_time = time.time() - start_time
    
    print(f"\n⏱️  Total execution time: {total_time:.2f}s")
    
    # Check results
    success_count = sum(1 for r in results.values() if r.success)
    print(f"✅ Successful tasks: {success_count}/{len(tasks)}")
    
    for task_id, result in results.items():
        if result.success:
            print(f"✅ {result.task_name}: {result.result.strip()[:50]}")
        else:
            print(f"❌ {result.task_name}: {result.error}")
    
    return success_count > 0


def test_dependencies():
    """Test task dependencies"""
    print("\n🧪 Testing Task Dependencies")
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)
    
    tasks = [
        ParallelTask(
            id="base1",
            name="Base Task 1",
            prompt="Say 'Task 1 complete'",
            provider="gemini"
        ),
        ParallelTask(
            id="base2", 
            name="Base Task 2",
            prompt="Say 'Task 2 complete'",
            provider="gemini"
        ),
        ParallelTask(
            id="dependent",
            name="Dependent Task",
            prompt="Say 'All base tasks finished'",
            dependencies=["base1", "base2"],
            provider="gemini"
        )
    ]
    
    print(f"📝 Running {len(tasks)} tasks with dependencies...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    # Verify dependency execution order
    if all(tid in results for tid in ["base1", "base2", "dependent"]):
        base1_end = results["base1"].end_time
        base2_end = results["base2"].end_time
        dependent_start = results["dependent"].start_time
        
        latest_base_end = max(base1_end, base2_end)
        dependency_respected = dependent_start >= latest_base_end
        
        print(f"🔗 Dependency order respected: {'✅' if dependency_respected else '❌'}")
        
        return dependency_respected
    
    return False


def test_error_handling():
    """Test error handling with invalid configurations"""
    print("\n🧪 Testing Error Handling")  
    print("=" * 50)
    
    agent = ParallelizationAgent(max_concurrent_tasks=2)
    
    tasks = [
        ParallelTask(
            id="good_task",
            name="Good Task",
            prompt="Say 'Hello World'",
            provider="gemini"
        ),
        ParallelTask(
            id="bad_task",
            name="Bad Task (Invalid Provider)",
            prompt="This should fail",
            provider="invalid_provider"  # This will cause an error
        )
    ]
    
    print(f"📝 Running tasks with intentional error...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    # Check that good task succeeded and bad task failed
    good_success = results.get("good_task", {}).success if "good_task" in results else False
    bad_failed = not results.get("bad_task", {}).success if "bad_task" in results else False
    
    print(f"✅ Good task succeeded: {'✅' if good_success else '❌'}")
    print(f"❌ Bad task failed as expected: {'✅' if bad_failed else '❌'}")
    
    return good_success and bad_failed


def test_performance_comparison():
    """Test performance improvement with parallelization"""
    print("\n🧪 Testing Performance Improvement")
    print("=" * 50)
    
    # Sequential execution
    print("🐌 Running tasks sequentially...")
    sequential_agent = ParallelizationAgent(max_concurrent_tasks=1)
    
    sequential_tasks = [
        ParallelTask(
            id="seq1",
            name="Sequential Task 1", 
            prompt="Count from 1 to 5 slowly: 1, 2, 3, 4, 5",
            provider="gemini"
        ),
        ParallelTask(
            id="seq2",
            name="Sequential Task 2",
            prompt="List 3 colors: red, blue, green",
            provider="gemini"
        )
    ]
    
    seq_start = time.time()
    sequential_agent.add_tasks(sequential_tasks)
    seq_results = sequential_agent.execute_parallel(show_progress=False)
    seq_time = time.time() - seq_start
    
    # Parallel execution
    print("\n🚀 Running tasks in parallel...")
    parallel_agent = ParallelizationAgent(max_concurrent_tasks=2)
    
    parallel_tasks = [
        ParallelTask(
            id="par1",
            name="Parallel Task 1",
            prompt="Count from 1 to 5 slowly: 1, 2, 3, 4, 5", 
            provider="gemini"
        ),
        ParallelTask(
            id="par2",
            name="Parallel Task 2",
            prompt="List 3 colors: red, blue, green",
            provider="gemini"
        )
    ]
    
    par_start = time.time()
    parallel_agent.add_tasks(parallel_tasks)
    par_results = parallel_agent.execute_parallel(show_progress=False)
    par_time = time.time() - par_start
    
    # Calculate improvement
    if par_time > 0:
        speedup = seq_time / par_time
        print(f"\n📊 Performance Results:")
        print(f"   Sequential: {seq_time:.2f}s")
        print(f"   Parallel:   {par_time:.2f}s")
        print(f"   Speedup:    {speedup:.2f}x")
        
        return speedup > 1.0  # Even minimal speedup is good
    
    return False


def main():
    """Run all tests"""
    print("🚀 Parallelization Pattern - Quick Tests")
    print("Testing core functionality with minimal tasks...")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Dependencies", test_dependencies), 
        ("Error Handling", test_error_handling),
        ("Performance", test_performance_comparison)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Parallelization pattern is working correctly.")
        print("💡 Try running 'python example.py --interactive' for full demo")
    else:
        print("⚠️  Some tests failed. Check your configuration:")
        print("   • Ensure Gemini API key is set (GOOGLE_API_KEY)")
        print("   • Ensure Ollama is running with phi3:mini model")
        print("   • Check network connectivity")


if __name__ == "__main__":
    main()