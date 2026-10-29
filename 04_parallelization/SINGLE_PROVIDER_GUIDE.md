# Single Provider Parallelization Examples

## ✅ Yes! You can run all tasks in parallel against one LLM

The parallelization pattern supports running multiple tasks against a single provider. This is great for:

### 🎯 **Use Cases**

1. **Scaling with High-Quality Provider**
   ```python
   # All tasks use OpenAI for consistency and quality
   tasks = [
       ParallelTask(id="task1", provider="openai", prompt="Analyze market trends"),
       ParallelTask(id="task2", provider="openai", prompt="Write product copy"),  
       ParallelTask(id="task3", provider="openai", prompt="Generate code"),
   ]
   ```

2. **Cost-Effective Local Processing**
   ```python
   # All tasks use Ollama for privacy and cost savings
   tasks = [
       ParallelTask(id="task1", provider="ollama", prompt="Classify documents"),
       ParallelTask(id="task2", provider="ollama", prompt="Extract entities"),
       ParallelTask(id="task3", provider="ollama", prompt="Summarize content"),
   ]
   ```

3. **Batch Content Generation**
   ```python
   # Generate multiple pieces of content with Gemini
   tasks = [
       ParallelTask(id="blog", provider="gemini", prompt="Write blog intro"),
       ParallelTask(id="social", provider="gemini", prompt="Create social post"),
       ParallelTask(id="email", provider="gemini", prompt="Write newsletter"),
   ]
   ```

### 🚀 **Performance Benefits**

**Sequential Execution (Traditional):**
```
Task 1 → Task 2 → Task 3 → Task 4 → Task 5
  3s      2s      4s      3s      2s    = 14 seconds total
```

**Parallel Execution (Same Provider):**
```
Task 1 ┐
Task 2 ├─ All execute simultaneously  
Task 3 ├─ Max time = 4s (slowest task)
Task 4 ├─ Speedup = 3.5x faster!
Task 5 ┘
```

### 📋 **Practical Example**

```python
from parallelization_agent import ParallelizationAgent, ParallelTask

# Create agent with higher concurrency for single provider
agent = ParallelizationAgent(max_concurrent_tasks=8)

# All tasks use OpenAI for consistent, high-quality results
openai_tasks = [
    ParallelTask(
        id="analysis_1",
        name="Market Analysis",
        prompt="Analyze Q3 sales trends for tech sector",
        provider="openai",
        model="gpt-4o-mini"
    ),
    ParallelTask(
        id="analysis_2", 
        name="Competitor Research",
        prompt="Research top 5 competitors in cloud computing",
        provider="openai",
        model="gpt-4o-mini"
    ),
    ParallelTask(
        id="content_1",
        name="Blog Post",
        prompt="Write intro for blog about AI trends", 
        provider="openai",
        model="gpt-4o-mini"
    ),
    ParallelTask(
        id="content_2",
        name="Product Description", 
        prompt="Write description for new SaaS product",
        provider="openai", 
        model="gpt-4o-mini"
    ),
    ParallelTask(
        id="synthesis",
        name="Executive Summary",
        prompt="Synthesize market analysis and competitor research into executive summary",
        provider="openai",
        model="gpt-4o-mini",
        dependencies=["analysis_1", "analysis_2"]  # Wait for analysis to complete
    )
]

# Execute all tasks - will run 4 in parallel, then synthesis
agent.add_tasks(openai_tasks)
results = agent.execute_parallel()

# Results: ~5-8 seconds instead of 15-20 seconds sequentially
```

### 🏠 **Local Processing Example (Ollama)**

```python
# High-throughput local processing for privacy-sensitive tasks
agent = ParallelizationAgent(max_concurrent_tasks=4)  # Adjust based on your hardware

local_tasks = [
    ParallelTask(id="classify_1", provider="ollama", model="phi3:mini",
                prompt="Classify this customer email as urgent/normal/low priority"),
    ParallelTask(id="classify_2", provider="ollama", model="phi3:mini", 
                prompt="Extract key entities from this contract text"),
    ParallelTask(id="classify_3", provider="ollama", model="phi3:mini",
                prompt="Summarize this internal document"),
    ParallelTask(id="classify_4", provider="ollama", model="phi3:mini",
                prompt="Generate response to customer inquiry"),
]

# Process locally without sending data to external APIs
results = agent.execute_parallel()
```

### ⚡ **Speed Optimization Tips**

1. **Adjust Concurrency Based on Provider:**
   ```python
   # OpenAI: Higher concurrency (respects rate limits)  
   agent = ParallelizationAgent(max_concurrent_tasks=8)
   
   # Ollama: Lower concurrency (limited by local hardware)
   agent = ParallelizationAgent(max_concurrent_tasks=3)
   
   # Gemini: Medium concurrency (balance speed and limits)
   agent = ParallelizationAgent(max_concurrent_tasks=5)
   ```

2. **Use Appropriate Models:**
   ```python
   # For speed: Use faster models
   ParallelTask(provider="openai", model="gpt-4o-mini")    # Fast
   ParallelTask(provider="gemini", model="gemini-1.5-flash") # Very fast
   ParallelTask(provider="ollama", model="phi3:mini")      # Local fast
   
   # For quality: Use larger models  
   ParallelTask(provider="openai", model="gpt-4o")        # High quality
   ParallelTask(provider="ollama", model="llama3.1:8b")   # Local quality
   ```

3. **Optimize Timeouts:**
   ```python
   # Shorter timeouts for simple tasks
   ParallelTask(timeout=15, prompt="Extract phone number from text")
   
   # Longer timeouts for complex tasks  
   ParallelTask(timeout=60, prompt="Write detailed technical analysis")
   ```

### 🔧 **Ready-to-Use Examples**

Try these files to see single-provider parallelization in action:

- `single_provider_demo.py` - Comprehensive demonstrations
- `quick_single_provider.py` - Simple test with 3 Gemini tasks
- Modify existing examples by changing all `provider` fields to the same value

### 🎉 **Key Benefits**

✅ **Consistency** - All results from same LLM model/style  
✅ **Simplicity** - Single API key and configuration  
✅ **Cost Control** - Use local models or budget-friendly options  
✅ **Speed** - 2-4x faster than sequential processing  
✅ **Scalability** - Handle batch processing efficiently  

The parallelization pattern works excellently with single providers and can significantly speed up your AI workflows while maintaining consistency!