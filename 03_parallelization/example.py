#!/usr/bin/env python3
"""
Parallelization Pattern Example

This example demonstrates running multiple AI tasks simultaneously across different
providers to achieve faster completion times and compare outputs.
"""

import sys
import os
import time
import json
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parallelization_agent import (
    ParallelizationAgent, 
    ParallelTask, 
    TaskPriority,
    create_content_generation_tasks,
    create_research_tasks
)


def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_task_result(result, show_full_output: bool = False):
    """Print a formatted task result"""
    status = "✅ SUCCESS" if result.success else "❌ FAILED"
    print(f"\n📋 {result.task_name} ({result.task_id})")
    print(f"   {status} | {result.provider_used} | {result.execution_time:.2f}s")
    
    if result.success and result.result:
        if show_full_output:
            print(f"   📝 Output:\n      {result.result[:200]}{'...' if len(result.result) > 200 else ''}")
        else:
            print(f"   📝 Output: {len(result.result)} characters")
    elif result.error:
        print(f"   ❌ Error: {result.error}")


def demonstrate_basic_parallelization():
    """Demonstrate basic parallel execution across multiple providers"""
    print_section("Basic Parallelization Demo")
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)
    
    # Create simple parallel tasks
    tasks = [
        ParallelTask(
            id="joke_openai",
            name="Programming Joke (OpenAI)",
            prompt="Tell me a funny programming joke about Python.",
            provider="openai",
            model="gpt-4o-mini"
        ),
        ParallelTask(
            id="joke_gemini", 
            name="Programming Joke (Gemini)",
            prompt="Tell me a funny programming joke about Python.",
            provider="gemini",
            model="gemini-1.5-flash"
        ),
        ParallelTask(
            id="joke_ollama",
            name="Programming Joke (Ollama)",
            prompt="Tell me a funny programming joke about Python.",
            provider="ollama",
            model="phi3:mini",
            timeout=45
        )
    ]
    
    print(f"🎯 Running {len(tasks)} tasks in parallel...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    print("\n📊 Results:")
    for task_id in ["joke_openai", "joke_gemini", "joke_ollama"]:
        if task_id in results:
            print_task_result(results[task_id], show_full_output=True)
    
    return results


def demonstrate_content_generation():
    """Demonstrate parallel content generation with dependencies"""
    print_section("Content Generation with Dependencies")
    
    agent = ParallelizationAgent(max_concurrent_tasks=4)
    tasks = create_content_generation_tasks()
    
    print(f"🎯 Running {len(tasks)} content generation tasks...")
    print("📋 Tasks include:")
    for task in tasks:
        deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"   • {task.name} [{task.provider}]{deps}")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    # Show results organized by category
    print("\n📊 AI Healthcare Summaries:")
    for task_id in ["summary_openai", "summary_gemini", "summary_ollama"]:
        if task_id in results and results[task_id].success:
            result = results[task_id]
            print(f"\n🔹 {result.provider_used.upper()}:")
            print(f"   {result.result[:150]}...")
    
    print("\n💻 Python Code Examples:")
    for task_id in ["code_openai", "code_gemini"]:
        if task_id in results and results[task_id].success:
            result = results[task_id]
            print(f"\n🔹 {result.provider_used.upper()}:")
            # Show just the function signature
            lines = result.result.split('\n')
            for line in lines[:3]:
                if line.strip():
                    print(f"   {line}")
                    break
    
    return results


def demonstrate_research_pipeline():
    """Demonstrate a research pipeline with synthesis"""
    print_section("Research Pipeline with Synthesis")
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)
    tasks = create_research_tasks()
    
    print(f"🎯 Running {len(tasks)} research tasks...")
    
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    
    # Show synthesis result if available
    if "synthesis" in results and results["synthesis"].success:
        print("\n🧠 Research Synthesis:")
        print(f"   {results['synthesis'].result[:300]}...")
    
    return results


def demonstrate_performance_comparison():
    """Compare sequential vs parallel execution times"""
    print_section("Performance Comparison: Sequential vs Parallel")
    
    # Create identical tasks for comparison
    base_tasks = [
        ParallelTask(
            id=f"perf_test_{i}",
            name=f"Performance Test {i+1}",
            prompt=f"Write a short poem about the number {i+1}.",
            provider=["gemini", "openai", "ollama"][i % 3],
            model="phi3:mini" if (i % 3) == 2 else None,
            timeout=45 if (i % 3) == 2 else 30
        )
        for i in range(6)
    ]
    
    # Sequential execution
    print("🐌 Sequential Execution:")
    sequential_start = time.time()
    
    sequential_agent = ParallelizationAgent(max_concurrent_tasks=1)
    sequential_agent.add_tasks(base_tasks.copy())
    sequential_results = sequential_agent.execute_parallel(show_progress=False)
    
    sequential_time = time.time() - sequential_start
    sequential_success = sum(1 for r in sequential_results.values() if r.success)
    
    # Parallel execution
    print("\n🚀 Parallel Execution:")
    parallel_start = time.time()
    
    parallel_agent = ParallelizationAgent(max_concurrent_tasks=4)
    # Create fresh tasks with new IDs to avoid conflicts
    parallel_tasks = [
        ParallelTask(
            id=f"parallel_test_{i}",
            name=f"Parallel Test {i+1}",
            prompt=task.prompt,
            provider=task.provider,
            model=task.model,
            timeout=task.timeout
        )
        for i, task in enumerate(base_tasks)
    ]
    
    parallel_agent.add_tasks(parallel_tasks)
    parallel_results = parallel_agent.execute_parallel(show_progress=False)
    
    parallel_time = time.time() - parallel_start
    parallel_success = sum(1 for r in parallel_results.values() if r.success)
    
    # Show comparison
    speedup = sequential_time / parallel_time if parallel_time > 0 else 0
    
    print(f"\n📊 Performance Comparison:")
    print(f"   Sequential: {sequential_time:.1f}s ({sequential_success}/{len(base_tasks)} successful)")
    print(f"   Parallel:   {parallel_time:.1f}s ({parallel_success}/{len(parallel_tasks)} successful)")
    print(f"   Speedup:    {speedup:.1f}x faster!")
    
    return {
        'sequential_time': sequential_time,
        'parallel_time': parallel_time,
        'speedup': speedup,
        'sequential_success': sequential_success,
        'parallel_success': parallel_success
    }


def show_agent_summary(agent: ParallelizationAgent):
    """Display a summary of agent execution"""
    summary = agent.get_task_summary()
    
    if "message" in summary:
        print(f"\n📊 {summary['message']}")
        return
    
    print("\n📊 Execution Summary:")
    print(f"   Total Tasks: {summary['total_tasks']}")
    print(f"   Successful: {summary['successful_tasks']}")
    print(f"   Failed: {summary['failed_tasks']}")
    
    if summary['provider_statistics']:
        print(f"\n🔧 Provider Performance:")
        for provider, stats in summary['provider_statistics'].items():
            success_rate = (stats['success'] / stats['count']) * 100 if stats['count'] > 0 else 0
            print(f"   {provider.upper()}: {stats['success']}/{stats['count']} "
                  f"({success_rate:.0f}%) - Avg: {stats['avg_time']:.1f}s")
    
    if summary['fastest_task']:
        fastest = summary['fastest_task']
        print(f"\n⚡ Fastest Task: {fastest.task_name} ({fastest.execution_time:.2f}s)")
    
    if summary['slowest_task']:
        slowest = summary['slowest_task']
        print(f"🐌 Slowest Task: {slowest.task_name} ({slowest.execution_time:.2f}s)")


def interactive_demo():
    """Run an interactive demonstration menu"""
    print_section("Parallelization Pattern - Interactive Demo")
    print("This demo showcases running multiple AI tasks simultaneously")
    print("across different providers (OpenAI, Gemini, Ollama)")
    
    while True:
        print(f"\n🎮 Choose a demonstration:")
        print(f"   1. Basic Parallelization (3 providers, same prompt)")
        print(f"   2. Content Generation (summaries + code with dependencies)")
        print(f"   3. Research Pipeline (parallel research + synthesis)")
        print(f"   4. Performance Comparison (sequential vs parallel)")
        print(f"   5. Exit")
        
        try:
            choice = input(f"\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                results = demonstrate_basic_parallelization()
                agent = ParallelizationAgent()
                agent.completed_tasks = results
                show_agent_summary(agent)
                
            elif choice == "2":
                results = demonstrate_content_generation()
                agent = ParallelizationAgent()
                agent.completed_tasks = results
                show_agent_summary(agent)
                
            elif choice == "3":
                results = demonstrate_research_pipeline()
                agent = ParallelizationAgent()
                agent.completed_tasks = results
                show_agent_summary(agent)
                
            elif choice == "4":
                demonstrate_performance_comparison()
                
            elif choice == "5":
                print("👋 Thanks for trying the Parallelization Pattern demo!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error during demo: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        # Run all demonstrations
        print("🚀 Running all Parallelization Pattern demonstrations...")
        
        try:
            demonstrate_basic_parallelization()
            demonstrate_content_generation()
            demonstrate_research_pipeline()
            demonstrate_performance_comparison()
            
            print_section("Demo Complete!")
            print("✨ All demonstrations completed successfully!")
            print("💡 Try running with --interactive flag for menu-driven demo")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()