#!/usr/bin/env python3
"""
Parallel Research Agents - Parallelization Agentic AI Pattern Example

This script demonstrates how multiple AI agents can work in parallel to research
different aspects of a topic simultaneously, then combine their results.

Usage:
    python parallel_research_agents.py "artificial intelligence ethics"
"""

import asyncio
import time
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Mock OpenAI client for demonstration (replace with real implementation)
class MockOpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def chat_completions_create(self, model: str, messages: List[Dict], max_tokens: int) -> Dict:
        """Mock OpenAI API call - replace with real openai.chat.completions.create()"""
        # Simulate API delay
        time.sleep(0.5)
        
        # Extract the research aspect from the system message
        system_msg = next((msg['content'] for msg in messages if msg['role'] == 'system'), '')
        user_msg = next((msg['content'] for msg in messages if msg['role'] == 'user'), '')
        
        # Generate mock response based on the research aspect
        mock_responses = {
            "technical": f"Technical analysis of {user_msg}: Advanced algorithms, implementation challenges, computational requirements...",
            "ethical": f"Ethical considerations for {user_msg}: Privacy concerns, bias issues, fairness, transparency requirements...",
            "economic": f"Economic impact of {user_msg}: Market opportunities, cost implications, ROI analysis, industry transformation...",
            "social": f"Social implications of {user_msg}: User adoption, cultural changes, accessibility, digital divide...",
            "regulatory": f"Regulatory landscape for {user_msg}: Current policies, compliance requirements, future regulations..."
        }
        
        # Determine response based on system message
        response_key = "technical"  # default
        for key in mock_responses.keys():
            if key.lower() in system_msg.lower():
                response_key = key
                break
                
        return {
            "choices": [{
                "message": {
                    "content": mock_responses[response_key],
                    "role": "assistant"
                }
            }]
        }

@dataclass
class ResearchTask:
    """Represents a research task for a single agent."""
    aspect: str
    prompt: str
    agent_id: str

@dataclass
class ResearchResult:
    """Represents the result from a research agent."""
    agent_id: str
    aspect: str
    content: str
    timestamp: datetime
    execution_time: float

class ParallelResearchCoordinator:
    """Coordinates multiple research agents working in parallel."""
    
    def __init__(self, api_key: str, max_concurrent_agents: int = 5):
        self.client = MockOpenAIClient(api_key)  # Replace with: openai.OpenAI(api_key=api_key)
        self.max_concurrent_agents = max_concurrent_agents
        
    def create_research_tasks(self, topic: str) -> List[ResearchTask]:
        """Create research tasks for different aspects of a topic."""
        aspects = [
            {
                "name": "technical",
                "prompt": f"You are a technical research specialist. Analyze the technical aspects of '{topic}'. Focus on implementation details, algorithms, architecture, and technological challenges. Provide specific technical insights and considerations."
            },
            {
                "name": "ethical", 
                "prompt": f"You are an ethics research specialist. Analyze the ethical implications of '{topic}'. Focus on moral considerations, potential risks, societal impact, and ethical frameworks. Provide thoughtful ethical analysis."
            },
            {
                "name": "economic",
                "prompt": f"You are an economic research specialist. Analyze the economic aspects of '{topic}'. Focus on market impact, cost-benefit analysis, business models, and economic implications. Provide detailed economic insights."
            },
            {
                "name": "social",
                "prompt": f"You are a social research specialist. Analyze the social implications of '{topic}'. Focus on user behavior, cultural impact, accessibility, and social dynamics. Provide comprehensive social analysis."
            },
            {
                "name": "regulatory",
                "prompt": f"You are a regulatory research specialist. Analyze the regulatory landscape for '{topic}'. Focus on current policies, compliance requirements, and potential future regulations. Provide regulatory insights."
            }
        ]
        
        return [
            ResearchTask(
                aspect=aspect["name"],
                prompt=aspect["prompt"],
                agent_id=f"agent_{i+1}_{aspect['name']}"
            )
            for i, aspect in enumerate(aspects)
        ]
    
    def execute_research_task(self, task: ResearchTask, topic: str) -> ResearchResult:
        """Execute a single research task."""
        start_time = time.time()
        
        try:
            messages = [
                {"role": "system", "content": task.prompt},
                {"role": "user", "content": f"Research topic: {topic}"}
            ]
            
            response = self.client.chat_completions_create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000
            )
            
            content = response["choices"][0]["message"]["content"]
            execution_time = time.time() - start_time
            
            return ResearchResult(
                agent_id=task.agent_id,
                aspect=task.aspect,
                content=content,
                timestamp=datetime.now(),
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ResearchResult(
                agent_id=task.agent_id,
                aspect=task.aspect,
                content=f"Error during research: {str(e)}",
                timestamp=datetime.now(),
                execution_time=execution_time
            )
    
    def run_parallel_research(self, topic: str) -> Dict[str, Any]:
        """Run parallel research on a topic using multiple agents."""
        print(f"🔍 Starting parallel research on: '{topic}'")
        print(f"📊 Using {self.max_concurrent_agents} concurrent agents")
        
        # Create research tasks
        tasks = self.create_research_tasks(topic)
        print(f"✅ Created {len(tasks)} research tasks")
        
        # Execute tasks in parallel
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_concurrent_agents) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self.execute_research_task, task, topic): task 
                for task in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✅ Agent {result.agent_id} completed {result.aspect} research in {result.execution_time:.2f}s")
                except Exception as e:
                    print(f"❌ Agent {task.agent_id} failed: {str(e)}")
        
        total_time = time.time() - start_time
        
        # Compile final report
        report = self.compile_research_report(topic, results, total_time)
        return report
    
    def compile_research_report(self, topic: str, results: List[ResearchResult], total_time: float) -> Dict[str, Any]:
        """Compile all research results into a final report."""
        report = {
            "topic": topic,
            "research_summary": {
                "total_agents": len(results),
                "total_time": total_time,
                "average_agent_time": sum(r.execution_time for r in results) / len(results) if results else 0,
                "timestamp": datetime.now().isoformat()
            },
            "research_results": {},
            "consolidated_insights": self.generate_consolidated_insights(results)
        }
        
        # Organize results by aspect
        for result in results:
            report["research_results"][result.aspect] = {
                "agent_id": result.agent_id,
                "content": result.content,
                "execution_time": result.execution_time,
                "timestamp": result.timestamp.isoformat()
            }
        
        return report
    
    def generate_consolidated_insights(self, results: List[ResearchResult]) -> str:
        """Generate consolidated insights from all research results."""
        # In a real implementation, this could use another AI agent to synthesize results
        insights = [
            "🔗 CONSOLIDATED INSIGHTS:",
            f"📈 Research completed by {len(results)} parallel agents",
            f"⚡ Parallel processing provided comprehensive multi-perspective analysis",
            ""
        ]
        
        for result in results:
            insights.append(f"🎯 {result.aspect.upper()} PERSPECTIVE:")
            insights.append(f"   {result.content[:100]}...")
            insights.append("")
        
        insights.extend([
            "💡 KEY BENEFITS OF PARALLEL RESEARCH:",
            "   • Comprehensive coverage of multiple aspects simultaneously",
            "   • Faster completion through concurrent execution", 
            "   • Diverse perspectives enhance research quality",
            "   • Scalable approach for complex topics"
        ])
        
        return "\n".join(insights)

def print_research_report(report: Dict[str, Any]):
    """Pretty print the research report."""
    print("\n" + "="*80)
    print(f"🔬 PARALLEL RESEARCH REPORT: {report['topic']}")
    print("="*80)
    
    # Summary
    summary = report['research_summary']
    print(f"\n📊 RESEARCH SUMMARY:")
    print(f"   • Total Agents: {summary['total_agents']}")
    print(f"   • Total Time: {summary['total_time']:.2f} seconds")
    print(f"   • Average Agent Time: {summary['average_agent_time']:.2f} seconds")
    print(f"   • Timestamp: {summary['timestamp']}")
    
    # Individual Results
    print(f"\n📋 DETAILED RESULTS:")
    for aspect, result in report['research_results'].items():
        print(f"\n🎯 {aspect.upper()} RESEARCH:")
        print(f"   Agent: {result['agent_id']}")
        print(f"   Time: {result['execution_time']:.2f}s")
        print(f"   Content: {result['content']}")
    
    # Consolidated Insights
    print(f"\n{report['consolidated_insights']}")

def main():
    """Main function to run the parallel research example."""
    if len(sys.argv) < 2:
        print("Usage: python parallel_research_agents.py \"<research topic>\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    # Initialize the coordinator
    coordinator = ParallelResearchCoordinator(
        api_key="mock-api-key",  # Replace with actual API key
        max_concurrent_agents=5
    )
    
    # Run parallel research
    report = coordinator.run_parallel_research(topic)
    
    # Display results
    print_research_report(report)
    
    # Save report to file
    filename = f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Report saved to: {filename}")

if __name__ == "__main__":
    main()