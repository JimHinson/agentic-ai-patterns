"""
Example usage of the Simple Agent Pattern

This script demonstrates various ways to use the Simple Agent pattern
and shows its strengths and limitations.
"""

from simple_agent import SimpleAgent
import time
import json


def demo_basic_usage():
    """Demonstrate basic usage of the Simple Agent."""
    print("🤖 Basic Simple Agent Usage Demo")
    print("=" * 50)
    
    agent = SimpleAgent()
    
    questions = [
        "What is the capital of France?",
        "How do I bake a chocolate cake?",
        "Explain quantum computing to a 10-year-old",
        "What are the benefits of regular exercise?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        result = agent.process_request(question)
        
        if result["success"]:
            print(f"✅ Response: {result['response'][:200]}...")
            print(f"📊 Tokens: {result['metadata']['tokens_used']}")
        else:
            print(f"❌ Error: {result['error']}")
        
        time.sleep(1)  # Avoid rate limits


def demo_conversation_flow():
    """Demonstrate conversation flow with memory."""
    print("\n\n💬 Conversation Flow Demo")
    print("=" * 50)
    
    agent = SimpleAgent()
    
    conversation = [
        "I'm planning a trip to Japan",
        "What should I visit in Tokyo?",
        "How about food recommendations?",
        "What's the best time of year to visit?"
    ]
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        result = agent.process_request(message)
        
        if result["success"]:
            print(f"🤖 Agent: {result['response']}")
        else:
            print(f"❌ Error: {result['error']}")
        
        time.sleep(1)


def demo_different_task_types():
    """Demonstrate how the simple agent handles different task types."""
    print("\n\n🔄 Different Task Types Demo")
    print("=" * 50)
    
    agent = SimpleAgent()
    
    tasks = [
        ("Factual Question", "What is the population of Brazil?"),
        ("Creative Writing", "Write a haiku about coding"),
        ("Problem Solving", "How can I organize my workspace better?"),
        ("Math Calculation", "What's the area of a circle with radius 5?"),
        ("Code Help", "How do I create a list in Python?"),
        ("Analysis", "Compare the pros and cons of remote work")
    ]
    
    results = {}
    
    for task_type, task in tasks:
        print(f"\n📋 Task Type: {task_type}")
        print(f"📝 Task: {task}")
        
        result = agent.process_request(task)
        
        if result["success"]:
            print(f"✅ Response: {result['response'][:150]}...")
            results[task_type] = {
                "success": True,
                "tokens": result['metadata']['tokens_used']
            }
        else:
            print(f"❌ Error: {result['error']}")
            results[task_type] = {
                "success": False,
                "error": result['error']
            }
        
        time.sleep(1)
    
    # Summary
    print("\n\n📈 Task Performance Summary")
    print("=" * 30)
    successful_tasks = sum(1 for r in results.values() if r["success"])
    total_tasks = len(results)
    
    print(f"Success Rate: {successful_tasks}/{total_tasks} ({successful_tasks/total_tasks*100:.1f}%)")
    
    if successful_tasks > 0:
        avg_tokens = sum(r.get("tokens", 0) for r in results.values() if r["success"]) / successful_tasks
        print(f"Average Tokens Used: {avg_tokens:.1f}")


def demo_limitations():
    """Demonstrate limitations of the Simple Agent pattern."""
    print("\n\n⚠️  Simple Agent Limitations Demo")
    print("=" * 50)
    
    agent = SimpleAgent()
    
    challenging_tasks = [
        "Analyze this CSV data: [no actual data provided]",
        "Connect to my database and run a query",
        "Send an email to john@example.com",
        "Process this image: [no image provided]",
        "Make a reservation at a restaurant"
    ]
    
    print("The Simple Agent will attempt these tasks but will have limitations:")
    
    for task in challenging_tasks:
        print(f"\n🔧 Challenging Task: {task}")
        result = agent.process_request(task)
        
        if result["success"]:
            print(f"🤖 Response: {result['response'][:200]}...")
            print("📝 Note: Agent can explain but cannot execute external actions")
        else:
            print(f"❌ Error: {result['error']}")
        
        time.sleep(1)


if __name__ == "__main__":
    print("Simple Agent Pattern - Comprehensive Examples")
    print("=" * 60)
    
    try:
        demo_basic_usage()
        demo_conversation_flow()
        demo_different_task_types()
        demo_limitations()
        
        print("\n\n🎯 Key Takeaways about Simple Agent Pattern:")
        print("✅ Great for general-purpose conversations")
        print("✅ Maintains conversation context")
        print("✅ Simple to implement and understand")
        print("❌ No specialization for complex tasks")
        print("❌ Cannot execute external actions")
        print("❌ May not be optimal for domain-specific tasks")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure you have set your OPENAI_API_KEY environment variable")