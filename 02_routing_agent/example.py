"""
Comprehensive Example of the Routing Agent Pattern

This script demonstrates the full routing pattern with multiple specialized agents,
showing how requests are classified and routed to the most appropriate agent.
"""

import time
import json
from typing import List, Dict, Any
from routing_agent import RouterAgent, RequestType
from specialized_agents import (
    MathAgent, CodeAgent, CreativeAgent, 
    FactualAgent, AnalysisAgent, GeneralAgent
)
from agent_registry import create_default_registry


class RoutingSystemDemo:
    """Complete demonstration of the routing agent pattern."""
    
    def __init__(self, api_key: str = None):
        """Initialize the routing system demo."""
        self.registry = create_default_registry(api_key)
        self.router = RouterAgent(api_key)
        
        # Register all agents with the router
        for agent_id, agent_info in self.registry.agents.items():
            self.router.register_agent(
                agent_id, 
                agent_info['instance'], 
                agent_info['types']
            )
    
    def demo_routing_decisions(self):
        """Demonstrate how the router makes routing decisions."""
        print("🎯 Routing Decision Analysis")
        print("=" * 50)
        
        test_requests = [
            "What's 25% of 480?",
            "Write a Python function to reverse a string",
            "Create a short poem about artificial intelligence",
            "What is the capital of New Zealand?",
            "Compare the advantages and disadvantages of remote work",
            "Hello, how are you doing today?",
            "Help me solve this algebra problem: 2x + 5 = 15",
            "How do I center a div in CSS?",
            "Write a haiku about programming",
            "Explain quantum computing in simple terms"
        ]
        
        routing_results = []
        
        for request in test_requests:
            routing_decision = self.router.route_request(request)
            routing_results.append({
                'request': request,
                'decision': routing_decision
            })
            
            print(f"\n📝 Request: {request}")
            print(f"🎯 Route Decision:")
            print(f"   Type: {routing_decision.request_type.value}")
            print(f"   Agent: {routing_decision.agent_id}")
            print(f"   Confidence: {routing_decision.confidence:.2f}")
            print(f"   Reasoning: {routing_decision.reasoning}")
            print("-" * 40)
        
        return routing_results
    
    def demo_specialized_responses(self):
        """Demonstrate how different agents handle their specialized requests."""
        print("\n\n🤖 Specialized Agent Responses")
        print("=" * 50)
        
        specialized_examples = [
            ("Math", "Calculate the area of a triangle with base 10 and height 8"),
            ("Code", "Create a function that finds the maximum value in a list"),
            ("Creative", "Write a limerick about debugging code"),
            ("Factual", "What are the main causes of climate change?"),
            ("Analysis", "What are the pros and cons of using microservices architecture?"),
        ]
        
        for category, request in specialized_examples:
            print(f"\n📋 {category} Request: {request}")
            
            start_time = time.time()
            result = self.router.process_request(request)
            end_time = time.time()
            
            if result["success"]:
                print(f"✅ Routed to: {result['routing']['routed_to']}")
                print(f"🎯 Request Type: {result['routing']['request_type']}")
                print(f"⚡ Response: {result['response'][:200]}...")
                print(f"⏱️  Time: {end_time - start_time:.2f}s")
                print(f"🔢 Tokens: {result['metadata']['tokens_used']}")
                
                # Update performance metrics
                self.registry.update_agent_performance(
                    result['routing']['routed_to'],
                    True,
                    end_time - start_time
                )
            else:
                print(f"❌ Error: {result['error']}")
            
            print("-" * 40)
            time.sleep(1)  # Avoid rate limits
    
    def demo_conversation_with_routing(self):
        """Demonstrate a conversation that involves multiple types of requests."""
        print("\n\n💬 Multi-Turn Conversation with Dynamic Routing")
        print("=" * 60)
        
        conversation = [
            "I'm working on a Python project",
            "Can you help me write a function to calculate compound interest?",
            "Now write a creative description of what compound interest is like",
            "What's the mathematical formula for compound interest?",
            "Compare compound interest vs simple interest - which is better for investors?"
        ]
        
        for i, message in enumerate(conversation, 1):
            print(f"\n{i}. 👤 User: {message}")
            
            result = self.router.process_request(message)
            
            if result["success"]:
                routed_to = result['routing']['routed_to']
                request_type = result['routing']['request_type']
                
                print(f"🎯 Routed to {routed_to} ({request_type})")
                print(f"🤖 Response: {result['response'][:300]}...")
                
                # Update performance
                self.registry.update_agent_performance(routed_to, True, 1.0)
            else:
                print(f"❌ Error: {result['error']}")
            
            print("-" * 50)
            time.sleep(1)
    
    def demo_performance_monitoring(self):
        """Show performance metrics and routing statistics."""
        print("\n\n📊 Performance Monitoring & Statistics")
        print("=" * 50)
        
        # Get router stats
        router_stats = self.router.get_routing_stats()
        
        print("Router Statistics:")
        print(f"  Total Agents: {router_stats['total_agents']}")
        print(f"  Total Requests: {router_stats['total_requests']}")
        
        print("\nAgent Usage:")
        for agent_id, usage in router_stats['agent_usage'].items():
            print(f"  {agent_id}: {usage['requests_handled']} requests")
            print(f"    Supports: {', '.join(usage['supported_types'])}")
        
        # Get registry stats
        registry_stats = self.registry.get_registry_stats()
        
        print("\nRegistry Performance:")
        for agent_id, stats in registry_stats['agents'].items():
            if stats['requests_handled'] > 0:
                print(f"  {agent_id}:")
                print(f"    Success Rate: {stats['success_rate']:.1%}")
                print(f"    Avg Response Time: {stats['average_response_time']:.2f}s")
                print(f"    Total Requests: {stats['requests_handled']}")
    
    def demo_error_handling(self):
        """Demonstrate error handling and fallback mechanisms."""
        print("\n\n⚠️  Error Handling & Fallback Mechanisms")
        print("=" * 50)
        
        # Temporarily deactivate a specific agent
        print("Temporarily deactivating the math agent...")
        self.registry.deactivate_agent('math_agent')
        
        # Try a math request
        math_request = "What's the derivative of x^2 + 3x + 2?"
        print(f"\n📝 Math Request: {math_request}")
        
        result = self.router.process_request(math_request)
        
        if result["success"]:
            routed_to = result['routing']['routed_to']
            print(f"✅ Fallback routing to: {routed_to}")
            print(f"📝 Response: {result['response'][:200]}...")
        else:
            print(f"❌ Error: {result['error']}")
        
        # Reactivate the agent
        print("\nReactivating the math agent...")
        self.registry.activate_agent('math_agent')
        
        # Try the same request again
        print(f"\n📝 Same request after reactivation:")
        result = self.router.process_request(math_request)
        
        if result["success"]:
            routed_to = result['routing']['routed_to']
            print(f"✅ Now routed to: {routed_to}")
        
    def run_complete_demo(self):
        """Run the complete routing pattern demonstration."""
        print("🚀 Complete Routing Agent Pattern Demonstration")
        print("=" * 60)
        
        try:
            # 1. Routing decisions
            self.demo_routing_decisions()
            
            # 2. Specialized responses
            self.demo_specialized_responses()
            
            # 3. Multi-turn conversation
            self.demo_conversation_with_routing()
            
            # 4. Performance monitoring
            self.demo_performance_monitoring()
            
            # 5. Error handling
            self.demo_error_handling()
            
            print("\n\n🎯 Key Benefits of Routing Pattern Demonstrated:")
            print("✅ Intelligent request classification and routing")
            print("✅ Specialized agents for better domain-specific performance")
            print("✅ Performance monitoring and load balancing")
            print("✅ Graceful fallback mechanisms")
            print("✅ Scalable architecture for adding new agent types")
            
        except Exception as e:
            print(f"Demo failed: {e}")
            print("Make sure you have set your OPENAI_API_KEY environment variable")


def simple_routing_example():
    """Simple example for quick testing."""
    print("🔄 Simple Routing Example")
    print("=" * 30)
    
    # Create basic routing system
    router = RouterAgent()
    
    # Create specialized agents
    math_agent = MathAgent()
    code_agent = CodeAgent()
    general_agent = GeneralAgent()
    
    # Register agents
    router.register_agent("math_agent", math_agent, [RequestType.MATH])
    router.register_agent("code_agent", code_agent, [RequestType.CODE])
    router.register_agent("general_agent", general_agent, [RequestType.GENERAL])
    
    # Test requests
    requests = [
        "What's 15 * 23?",
        "Write a hello world program in Python",
        "How's the weather today?"
    ]
    
    for request in requests:
        print(f"\n📝 Request: {request}")
        routing = router.route_request(request)
        print(f"🎯 → {routing.agent_id} ({routing.request_type.value})")


if __name__ == "__main__":
    import os
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("Running routing decision demo only (no LLM calls)...")
        simple_routing_example()
    else:
        # Run complete demo
        demo = RoutingSystemDemo()
        demo.run_complete_demo()