# Parallelization Pattern

## Overview

The Parallelization pattern enables running multiple AI tasks simultaneously across different LLM providers to achieve faster overall completion times and leverage the strengths of different models.

## Key Concepts

### 1. **Concurrent Execution**
- Run multiple AI tasks simultaneously instead of sequentially
- Utilize different providers (OpenAI, Gemini, Ollama) in parallel
- Maximize throughput and minimize total execution time

### 2. **Task Dependencies**
- Support task dependencies where some tasks must complete before others can start
- Automatic dependency resolution and execution ordering
- Enable complex workflows with parallel and sequential components

### 3. **Provider Diversity**
- Leverage different AI providers for different strengths:
  - **OpenAI**: High quality, reliable responses
  - **Gemini**: Fast responses, good for analysis
  - **Ollama**: Local/private processing, cost-effective
- Compare outputs from multiple providers
- Fallback options if one provider fails

### 4. **Resource Management**
- Configurable concurrency limits to prevent resource exhaustion
- Task prioritization (HIGH, NORMAL, LOW, CRITICAL)
- Timeout management per task and provider

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Task Queue    │    │ Parallelization  │    │   Results       │
│                 │────│     Agent        │────│                 │
│ • Task A        │    │                  │    │ • Success/Fail  │
│ • Task B        │    │ • Dependency     │    │ • Execution Time│
│ • Task C        │    │   Management     │    │ • Provider Used │
│ • Dependencies  │    │ • Resource Mgmt  │    │ • Output Data   │
└─────────────────┘    │ • Thread Pool    │    └─────────────────┘
                       └──────────────────┘
                               │
                    ┌──────────┼──────────┐
                    │          │          │
            ┌───────▼────┐ ┌───▼────┐ ┌───▼────┐
            │   OpenAI   │ │ Gemini │ │ Ollama │
            │  Provider  │ │Provider│ │Provider│
            └────────────┘ └────────┘ └────────┘
```

## Usage Examples

### Basic Parallelization

```python
from parallelization_agent import ParallelizationAgent, ParallelTask

# Create agent with max 3 concurrent tasks
agent = ParallelizationAgent(max_concurrent_tasks=3)

# Add tasks for different providers
tasks = [
    ParallelTask(
        id="summary_openai",
        name="Summary (OpenAI)",
        prompt="Summarize the benefits of AI in healthcare.",
        provider="openai"
    ),
    ParallelTask(
        id="summary_gemini",
        name="Summary (Gemini)", 
        prompt="Summarize the benefits of AI in healthcare.",
        provider="gemini"
    ),
    ParallelTask(
        id="summary_ollama",
        name="Summary (Ollama)",
        prompt="Summarize the benefits of AI in healthcare.",
        provider="ollama",
        model="phi3:mini"
    )
]

# Execute all tasks in parallel
agent.add_tasks(tasks)
results = agent.execute_parallel()
```

### Tasks with Dependencies

```python
# Task that depends on other tasks completing first
analysis_task = ParallelTask(
    id="analysis",
    name="Comparison Analysis",
    prompt="Compare the summaries from different AI providers.",
    dependencies=["summary_openai", "summary_gemini", "summary_ollama"],
    provider="gemini"
)

agent.add_task(analysis_task)
```

### Research Pipeline Example

```python
# Parallel research with synthesis
research_tasks = [
    ParallelTask(
        id="tech_trends",
        name="Technology Trends",
        prompt="Research major tech trends for 2024.",
        provider="gemini"
    ),
    ParallelTask(
        id="ai_ethics", 
        name="AI Ethics",
        prompt="Outline key AI ethical considerations.",
        provider="openai"
    ),
    ParallelTask(
        id="synthesis",
        name="Research Synthesis",
        prompt="Synthesize the research findings.",
        dependencies=["tech_trends", "ai_ethics"],
        provider="gemini"
    )
]
```

## Performance Benefits

### Sequential vs Parallel Execution

**Sequential Execution:**
```
Task A (OpenAI)  ████████████ 12s
Task B (Gemini)           ████████ 8s  
Task C (Ollama)                    ██████████ 10s
Total Time: 30s
```

**Parallel Execution:**
```
Task A (OpenAI)  ████████████ 12s
Task B (Gemini)  ████████ 8s
Task C (Ollama)  ██████████ 10s
Total Time: 12s (2.5x faster!)
```

### Typical Speedup Results
- **3 providers, simple tasks**: 2-3x speedup
- **Mixed task complexity**: 1.5-2.5x speedup  
- **With dependencies**: 1.2-2x speedup
- **Network-bound tasks**: 3-5x speedup

## Advanced Features

### Task Prioritization

```python
high_priority_task = ParallelTask(
    id="urgent_analysis",
    name="Urgent Analysis",
    prompt="Analyze critical system issue.",
    provider="openai",
    priority=TaskPriority.CRITICAL
)
```

### Provider-Specific Configuration

```python
ollama_task = ParallelTask(
    id="local_processing",
    name="Local AI Processing",
    prompt="Process sensitive data locally.",
    provider="ollama",
    model="llama3.1:8b",
    timeout=120,  # Longer timeout for larger model
    temperature=0.3
)
```

### Error Handling and Fallbacks

The agent automatically handles:
- Provider failures (timeouts, API errors)
- Dependency failures (dependent tasks won't execute)
- Resource exhaustion (respects concurrency limits)
- Network issues (per-task timeout handling)

## Best Practices

### 1. **Choose Appropriate Concurrency**
- Start with 3-5 concurrent tasks
- Monitor resource usage (CPU, memory, network)
- Adjust based on provider rate limits

### 2. **Optimize Task Distribution**
- Use faster providers (Gemini) for quick tasks
- Use high-quality providers (OpenAI) for complex analysis
- Use local providers (Ollama) for private/cost-sensitive tasks

### 3. **Design Efficient Dependencies**
- Minimize dependency chains for better parallelization
- Group independent tasks together
- Use synthesis tasks to combine parallel results

### 4. **Handle Provider Differences**
- Set appropriate timeouts per provider
- Use different models for different task types
- Plan for provider-specific failures

### 5. **Monitor and Debug**
- Use task result analysis to optimize provider selection
- Track execution times to identify bottlenecks
- Monitor success rates per provider

## Common Use Cases

### 1. **Content Generation**
- Generate multiple versions of content simultaneously
- Compare outputs from different AI models
- Parallel research and synthesis

### 2. **Data Analysis**
- Analyze different aspects of data in parallel
- Multi-perspective analysis with different AI models
- Parallel processing of data subsets

### 3. **Research and Synthesis**
- Parallel information gathering
- Multi-source research with final synthesis
- Competitive analysis across different domains

### 4. **Code Generation**
- Generate code in different languages simultaneously
- Multiple implementation approaches in parallel
- Code review and optimization suggestions

### 5. **Decision Support**
- Parallel analysis of different options
- Multi-criteria evaluation
- Risk assessment from different perspectives

## Running the Examples

### Interactive Demo
```bash
python example.py --interactive
```

### All Demonstrations
```bash
python example.py
```

### Using with Agent Runner
```bash
# Run basic parallelization with custom timeout
python ../agent_runner.py --timeout 60

# Then in the agent:
from parallelization_agent import ParallelizationAgent, ParallelTask
# ... create and run tasks
```

## Performance Tuning

### Ollama Optimization
- Use smaller, faster models: `phi3:mini`, `orca-mini:3b`
- Increase timeout for complex tasks: `timeout=60-120`
- Monitor system resources during parallel execution

### Provider Selection Strategy
```python
# Fast tasks: Use Gemini
fast_task = ParallelTask(provider="gemini", model="gemini-1.5-flash")

# Complex analysis: Use OpenAI  
complex_task = ParallelTask(provider="openai", model="gpt-4o-mini")

# Private/local: Use Ollama
private_task = ParallelTask(provider="ollama", model="phi3:mini")
```

### Monitoring Execution
```python
# Get execution statistics
summary = agent.get_task_summary()
print(f"Provider performance: {summary['provider_statistics']}")
print(f"Average speedup: {summary.get('speedup', 'N/A')}x")
```

This pattern significantly improves AI application performance by leveraging the parallel processing capabilities and diverse strengths of multiple LLM providers.