"""
Parallelization Agent Pattern Implementation

This module demonstrates running multiple AI tasks simultaneously across different
providers and models to achieve faster overall completion times.
"""

import asyncio
import concurrent.futures
import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
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

from agent_core import LLMProvider, AgentConfig


class TaskPriority(Enum):
    """Priority levels for parallel tasks"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ParallelTask:
    """Represents a task to be executed in parallel"""
    id: str
    name: str
    prompt: str
    system_prompt: Optional[str] = None
    provider: str = "gemini"
    model: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: int = 60
    max_tokens: int = 1000
    temperature: float = 0.7
    dependencies: List[str] = field(default_factory=list)  # Task IDs this task depends on


@dataclass
class TaskResult:
    """Result of a parallel task execution"""
    task_id: str
    task_name: str
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    provider_used: str = ""
    model_used: str = ""
    start_time: float = 0.0
    end_time: float = 0.0


class ParallelizationAgent:
    """Agent that executes multiple tasks in parallel across different LLM providers"""
    
    def __init__(self, max_concurrent_tasks: int = 5):
        """
        Initialize the parallelization agent
        
        Args:
            max_concurrent_tasks: Maximum number of tasks to run simultaneously
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_queue: List[ParallelTask] = []
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.active_tasks: Dict[str, threading.Thread] = {}
        self.task_lock = threading.Lock()
        
    def add_task(self, task: ParallelTask) -> None:
        """Add a task to the execution queue"""
        with self.task_lock:
            self.task_queue.append(task)
            print(f"✅ Added task '{task.name}' (ID: {task.id}) to queue")
    
    def add_tasks(self, tasks: List[ParallelTask]) -> None:
        """Add multiple tasks to the execution queue"""
        for task in tasks:
            self.add_task(task)
    
    def _execute_single_task(self, task: ParallelTask) -> TaskResult:
        """Execute a single task"""
        print(f"🚀 Starting task '{task.name}' with {task.provider}")
        start_time = time.time()
        
        try:
            # Create LLM provider configuration with default model if none specified
            model = task.model
            if not model:
                # Use default models per provider
                default_models = {
                    "openai": "gpt-4o-mini",
                    "anthropic": "claude-3-haiku-20240307",
                    "gemini": "gemini-1.5-flash",
                    "ollama": "phi3:mini"
                }
                model = default_models.get(task.provider, "gpt-4o-mini")
            
            config = AgentConfig(
                provider=task.provider,
                model=model,
                timeout=task.timeout,
                max_tokens=task.max_tokens,
                temperature=task.temperature
            )
            
            # Create provider and execute
            llm_provider = LLMProvider(config)
            result = llm_provider.generate(task.prompt, task.system_prompt)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"✅ Completed task '{task.name}' in {execution_time:.2f}s")
            
            return TaskResult(
                task_id=task.id,
                task_name=task.name,
                success=True,
                result=result,
                execution_time=execution_time,
                provider_used=task.provider,
                model_used=task.model or config.model,
                start_time=start_time,
                end_time=end_time
            )
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"❌ Failed task '{task.name}': {str(e)}")
            
            return TaskResult(
                task_id=task.id,
                task_name=task.name,
                success=False,
                error=str(e),
                execution_time=execution_time,
                provider_used=task.provider,
                model_used=task.model or "unknown",
                start_time=start_time,
                end_time=end_time
            )
    
    def _can_execute_task(self, task: ParallelTask) -> bool:
        """Check if a task's dependencies are satisfied"""
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
            if not self.completed_tasks[dep_id].success:
                return False
        
        return True
    
    def execute_parallel(self, show_progress: bool = True) -> Dict[str, TaskResult]:
        """
        Execute all queued tasks in parallel with dependency management
        
        Args:
            show_progress: Whether to show execution progress
            
        Returns:
            Dictionary of task results keyed by task ID
        """
        if not self.task_queue:
            print("⚠️  No tasks in queue to execute")
            return {}
        
        total_tasks = len(self.task_queue)
        print(f"🎯 Executing {total_tasks} tasks in parallel (max concurrent: {self.max_concurrent_tasks})")
        
        remaining_tasks = self.task_queue.copy()
        overall_start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent_tasks) as executor:
            future_to_task = {}
            
            while remaining_tasks or future_to_task:
                # Submit tasks that can be executed (dependencies satisfied)
                tasks_to_submit = []
                for task in remaining_tasks[:]:
                    if self._can_execute_task(task):
                        tasks_to_submit.append(task)
                        remaining_tasks.remove(task)
                
                # Submit available tasks up to the concurrent limit
                for task in tasks_to_submit:
                    if len(future_to_task) < self.max_concurrent_tasks:
                        try:
                            future = executor.submit(self._execute_single_task, task)
                            future_to_task[future] = task
                        except Exception as e:
                            print(f"❌ Failed to submit task {task.name}: {e}")
                            # Create a failed result
                            failed_result = TaskResult(
                                task_id=task.id,
                                task_name=task.name,
                                success=False,
                                error=f"Failed to submit: {e}",
                                provider_used=task.provider
                            )
                            self.completed_tasks[task.id] = failed_result
                
                # Wait for completed tasks
                if future_to_task:
                    # Use as_completed with a short timeout to avoid hanging
                    try:
                        done_futures, _ = concurrent.futures.wait(
                            future_to_task.keys(), 
                            timeout=1.0,
                            return_when=concurrent.futures.FIRST_COMPLETED
                        )
                        
                        for future in done_futures:
                            task = future_to_task[future]
                            try:
                                result = future.result()
                                self.completed_tasks[result.task_id] = result
                                
                                if show_progress:
                                    completed_count = len(self.completed_tasks)
                                    success_count = sum(1 for r in self.completed_tasks.values() if r.success)
                                    print(f"📊 Progress: {completed_count}/{total_tasks} tasks completed ({success_count} successful)")
                                
                            except Exception as e:
                                # Handle task execution errors
                                error_result = TaskResult(
                                    task_id=task.id,
                                    task_name=task.name,
                                    success=False,
                                    error=str(e),
                                    provider_used=task.provider
                                )
                                self.completed_tasks[task.id] = error_result
                                print(f"❌ Task {task.name} failed: {e}")
                            
                            # Remove completed future
                            del future_to_task[future]
                    
                    except Exception as e:
                        print(f"⚠️  Error waiting for futures: {e}")
                        break
                
                # Safety check to avoid infinite loops
                if not remaining_tasks and not future_to_task:
                    break
        
        overall_time = time.time() - overall_start_time
        
        # Print summary
        successful_tasks = [r for r in self.completed_tasks.values() if r.success]
        failed_tasks = [r for r in self.completed_tasks.values() if not r.success]
        
        print(f"\n🎉 Parallel execution completed in {overall_time:.2f}s")
        print(f"✅ Successful: {len(successful_tasks)}/{total_tasks}")
        
        # Only show failed count if there are actually failures
        if failed_tasks:
            print(f"❌ Failed: {len(failed_tasks)}/{total_tasks}")
        else:
            print("🎯 All tasks completed successfully!")
        
        if successful_tasks:
            avg_time = sum(r.execution_time for r in successful_tasks) / len(successful_tasks)
            print(f"⏱️  Average task time: {avg_time:.2f}s")
            total_sequential_time = sum(r.execution_time for r in successful_tasks)
            if overall_time > 0:
                speedup = total_sequential_time / overall_time
                print(f"🚀 Speedup: ~{speedup:.1f}x faster than sequential")
        
        # Clear the queue
        self.task_queue.clear()
        
        return self.completed_tasks
    
    def get_task_summary(self) -> Dict[str, Any]:
        """Get a summary of all executed tasks"""
        if not self.completed_tasks:
            return {"message": "No tasks executed yet"}
        
        successful_tasks = [r for r in self.completed_tasks.values() if r.success]
        failed_tasks = [r for r in self.completed_tasks.values() if not r.success]
        
        provider_stats = {}
        for result in self.completed_tasks.values():
            provider = result.provider_used
            if provider not in provider_stats:
                provider_stats[provider] = {"count": 0, "success": 0, "avg_time": 0}
            
            provider_stats[provider]["count"] += 1
            if result.success:
                provider_stats[provider]["success"] += 1
                
        # Calculate average times
        for provider, stats in provider_stats.items():
            provider_results = [r for r in self.completed_tasks.values() 
                             if r.provider_used == provider and r.success]
            if provider_results:
                stats["avg_time"] = sum(r.execution_time for r in provider_results) / len(provider_results)
        
        return {
            "total_tasks": len(self.completed_tasks),
            "successful_tasks": len(successful_tasks),
            "failed_tasks": len(failed_tasks),
            "provider_statistics": provider_stats,
            "fastest_task": min(successful_tasks, key=lambda x: x.execution_time) if successful_tasks else None,
            "slowest_task": max(successful_tasks, key=lambda x: x.execution_time) if successful_tasks else None
        }
    
    def clear_results(self):
        """Clear all completed task results"""
        self.completed_tasks.clear()
        print("🧹 Cleared all task results")


def create_content_generation_tasks() -> List[ParallelTask]:
    """Create a set of parallel content generation tasks"""
    return [
        ParallelTask(
            id="summary_openai",
            name="Article Summary (OpenAI)",
            prompt="Write a 100-word summary about the benefits of artificial intelligence in healthcare.",
            provider="openai",
            model="gpt-4o-mini",
            priority=TaskPriority.HIGH
        ),
        ParallelTask(
            id="summary_gemini",
            name="Article Summary (Gemini)",
            prompt="Write a 100-word summary about the benefits of artificial intelligence in healthcare.",
            provider="gemini",
            model="gemini-1.5-flash",
            priority=TaskPriority.HIGH
        ),
        ParallelTask(
            id="summary_ollama",
            name="Article Summary (Ollama)",
            prompt="Write a 100-word summary about the benefits of artificial intelligence in healthcare.",
            provider="ollama",
            model="phi3:mini",
            priority=TaskPriority.NORMAL,
            timeout=45
        ),
        ParallelTask(
            id="code_openai",
            name="Python Code (OpenAI)",
            prompt="Write a Python function to calculate the factorial of a number using recursion. Include docstring and example.",
            provider="openai",
            system_prompt="You are a Python expert. Write clean, well-documented code."
        ),
        ParallelTask(
            id="code_gemini",
            name="Python Code (Gemini)",
            prompt="Write a Python function to calculate the factorial of a number using recursion. Include docstring and example.",
            provider="gemini",
            system_prompt="You are a Python expert. Write clean, well-documented code."
        ),
        ParallelTask(
            id="analysis_comparison",
            name="Comparison Analysis",
            prompt="Compare the summaries and code implementations from different AI providers.",
            dependencies=["summary_openai", "summary_gemini", "code_openai", "code_gemini"],
            provider="gemini",
            priority=TaskPriority.LOW
        )
    ]


def create_research_tasks() -> List[ParallelTask]:
    """Create parallel research tasks"""
    return [
        ParallelTask(
            id="tech_trends",
            name="Technology Trends Research",
            prompt="Research and list 5 major technology trends for 2024-2025. Provide brief explanations.",
            provider="gemini"
        ),
        ParallelTask(
            id="ai_ethics",
            name="AI Ethics Research", 
            prompt="Outline key ethical considerations in AI development and deployment.",
            provider="openai"
        ),
        ParallelTask(
            id="sustainability",
            name="Green Tech Research",
            prompt="Research sustainable technology solutions for reducing carbon footprint.",
            provider="ollama",
            model="phi3:mini",
            timeout=60
        ),
        ParallelTask(
            id="synthesis",
            name="Research Synthesis",
            prompt="Synthesize findings from technology trends, AI ethics, and sustainability research into a cohesive overview.",
            dependencies=["tech_trends", "ai_ethics", "sustainability"],
            provider="gemini"
        )
    ]