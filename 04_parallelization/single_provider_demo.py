#!/usr/bin/env python3
"""
Single Provider Parallelization Demo

Shows how to run multiple tasks in parallel against a single LLM provider
for scaling, batch processing, or consistency needs.
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

from parallelization_agent import ParallelizationAgent, ParallelTask


def demo_single_provider_scaling(provider="gemini", num_tasks=5):
    """Demonstrate scaling with a single provider"""
    print(f"🚀 Single Provider Scaling Demo - {provider.upper()}")
    print("=" * 60)
    
    agent = ParallelizationAgent(max_concurrent_tasks=num_tasks)
    
    # Create multiple different tasks for the same provider
    prompts = [
        "Write a haiku about programming",
        "Explain quantum computing in simple terms",
        "List 3 benefits of renewable energy", 
        "Write a Python function to reverse a string",
        "Describe the water cycle in 2 sentences"
    ]
    
    tasks = []
    for i, prompt in enumerate(prompts):
        task = ParallelTask(
            id=f"task_{i+1}",
            name=f"Task {i+1} ({provider.upper()})",
            prompt=prompt,
            provider=provider,
            timeout=45 if provider == "ollama" else 30
        )
        tasks.append(task)
    
    print(f"📋 Running {len(tasks)} different tasks in parallel with {provider.upper()}:")
    for i, prompt in enumerate(prompts, 1):
        print(f"   {i}. {prompt}")
    
    start_time = time.time()
    agent.add_tasks(tasks)
    results = agent.execute_parallel()
    total_time = time.time() - start_time
    
    # Calculate what sequential time would have been
    successful_results = [r for r in results.values() if r.success]
    if successful_results:
        sequential_time = sum(r.execution_time for r in successful_results)
        speedup = sequential_time / total_time if total_time > 0 else 1
        
        print(f"\n📊 Performance Results:")
        print(f"   Parallel time:   {total_time:.1f}s")
        print(f"   Sequential time: {sequential_time:.1f}s (estimated)")
        print(f"   Speedup:         {speedup:.1f}x faster!")
    
    print(f"\n📝 Sample Results:")
    for i, (task_id, result) in enumerate(results.items(), 1):
        if result.success and i <= 3:  # Show first 3 results
            print(f"   {i}. {result.result[:80]}...")
    
    return results


def demo_batch_content_generation(provider="openai"):
    """Demonstrate batch content generation with one provider"""
    print(f"\n🎨 Batch Content Generation - {provider.upper()}")
    print("=" * 60)
    
    agent = ParallelizationAgent(max_concurrent_tasks=4)
    
    # Generate different types of content in parallel
    content_tasks = [
        ParallelTask(
            id="blog_intro",
            name="Blog Introduction",
            prompt="Write an engaging introduction for a blog about AI in healthcare (100 words).",
            provider=provider,
            system_prompt="You are a professional content writer."
        ),
        ParallelTask(
            id="social_post",
            name="Social Media Post", 
            prompt="Write a Twitter/X post about the benefits of renewable energy (280 chars max).",
            provider=provider,
            system_prompt="You are a social media expert."
        ),
        ParallelTask(
            id="email_subject",
            name="Email Subject Lines",
            prompt="Write 5 compelling email subject lines for a newsletter about productivity tips.",
            provider=provider,
            system_prompt="You are an email marketing specialist."
        ),
        ParallelTask(
            id="product_desc",
            name="Product Description",
            prompt="Write a product description for a smart home thermostat (150 words).",
            provider=provider,
            system_prompt="You are a product marketing expert."
        )
    ]
    
    print(f"📝 Generating different content types simultaneously with {provider.upper()}...")
    
    agent.add_tasks(content_tasks)
    results = agent.execute_parallel()
    
    print(f"\n✅ Generated Content:")
    content_types = {
        "blog_intro": "Blog Introduction",
        "social_post": "Social Media Post",
        "email_subject": "Email Subject Lines", 
        "product_desc": "Product Description"
    }
    
    for task_id, title in content_types.items():
        if task_id in results and results[task_id].success:
            result = results[task_id]
            print(f"\n📄 {title} ({result.execution_time:.1f}s):")
            print(f"   {result.result[:150]}...")
    
    return results


def demo_local_batch_processing():
    """Demonstrate batch processing with local Ollama"""
    print(f"\n🏠 Local Batch Processing - OLLAMA")
    print("=" * 60)
    
    agent = ParallelizationAgent(max_concurrent_tasks=3)  # Lower concurrency for local
    
    # Process multiple documents/tasks locally
    analysis_tasks = [
        ParallelTask(
            id="sentiment_1",
            name="Sentiment Analysis 1",
            prompt="Analyze the sentiment of this text: 'I love using this new software! It makes my work so much easier and faster.'",
            provider="ollama",
            timeout=30
        ),
        ParallelTask(
            id="sentiment_2", 
            name="Sentiment Analysis 2",
            prompt="Analyze the sentiment of this text: 'The service was disappointing and the wait time was too long.'",
            provider="ollama",
            timeout=30
        ),
        ParallelTask(
            id="summarize",
            name="Text Summarization",
            prompt="Summarize this in 2 sentences: Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make predictions or decisions.",
            provider="ollama", 
            timeout=30
        ),
        ParallelTask(
            id="classify",
            name="Text Classification",
            prompt="Classify this email as spam or not spam: 'Congratulations! You've won $1000! Click here immediately to claim your prize!'",
            provider="ollama",
            timeout=30
        )
    ]
    
    print("🔍 Processing multiple text analysis tasks locally with Ollama...")
    
    agent.add_tasks(analysis_tasks)
    results = agent.execute_parallel()
    
    print(f"\n🎯 Analysis Results:")
    for task_id, result in results.items():
        if result.success:
            print(f"✅ {result.task_name}: {result.result[:100]}...")
        else:
            print(f"❌ {result.task_name}: Failed - {result.error}")
    
    return results


def demo_consistency_testing(provider="gemini"):
    """Test consistency by running same prompt multiple times"""
    print(f"\n🎯 Consistency Testing - {provider.upper()}")
    print("=" * 60)
    
    agent = ParallelizationAgent(max_concurrent_tasks=5)
    
    # Same prompt, multiple executions to test consistency
    prompt = "Rate the importance of cybersecurity for small businesses on a scale of 1-10 and explain in one sentence."
    
    consistency_tasks = []
    for i in range(5):
        task = ParallelTask(
            id=f"consistency_{i+1}",
            name=f"Consistency Test {i+1}",
            prompt=prompt,
            provider=provider,
            temperature=0.7  # Some variation expected
        )
        consistency_tasks.append(task)
    
    print(f"🔄 Running same prompt 5 times in parallel to test consistency...")
    print(f"📝 Prompt: {prompt}")
    
    agent.add_tasks(consistency_tasks)
    results = agent.execute_parallel()
    
    print(f"\n📊 Consistency Results:")
    successful_results = [r for r in results.values() if r.success]
    
    for i, result in enumerate(successful_results, 1):
        print(f"   {i}. {result.result[:120]}...")
    
    if len(successful_results) >= 2:
        # Simple consistency check
        ratings = []
        for result in successful_results:
            # Try to extract rating numbers
            import re
            numbers = re.findall(r'\b([1-9]|10)\b', result.result)
            if numbers:
                ratings.append(int(numbers[0]))
        
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            rating_range = max(ratings) - min(ratings)
            print(f"\n📈 Rating Analysis:")
            print(f"   Ratings found: {ratings}")
            print(f"   Average: {avg_rating:.1f}")
            print(f"   Range: {rating_range} (consistency: {'High' if rating_range <= 2 else 'Medium' if rating_range <= 4 else 'Low'})")
    
    return results


def main():
    """Run all single-provider demonstrations"""
    print("🚀 Single Provider Parallelization Demonstrations")
    print("=" * 80)
    
    demos = [
        ("Scaling with Gemini", lambda: demo_single_provider_scaling("gemini", 5)),
        ("Batch Content (OpenAI)", lambda: demo_batch_content_generation("openai")),
        ("Local Processing (Ollama)", demo_local_batch_processing),
        ("Consistency Testing (Gemini)", lambda: demo_consistency_testing("gemini"))
    ]
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n{'='*20} {demo_name} {'='*20}")
            demo_func()
            print("✅ Demo completed successfully!")
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("🎉 All single-provider demonstrations completed!")
    print("\n💡 Key Benefits of Single-Provider Parallelization:")
    print("   🚀 Scale processing with your preferred LLM")
    print("   💰 Cost-effective batch processing with local models")
    print("   🔒 Consistent results within one provider's ecosystem")
    print("   ⚡ Significant speedup over sequential processing")


if __name__ == "__main__":
    main()