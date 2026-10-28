# agentic-ai-patterns
Examples of patterns presented by Mark Kashef in his YouTube video "Master ALL 20 Agentic AI Design Patterns [Complete Course]"

## 🚀 Quick Start with Real AI Agents

Want to run these patterns with actual LLMs? See **[AGENT_SETUP.md](AGENT_SETUP.md)** for a complete setup guide.

**Quick setup:**
```bash
# 1. Install dependencies
pip install -r 01_prompt_chaining/requirements.txt

# 2. Set up API keys
copy .env.example .env
# Edit .env with your OpenAI/Anthropic API keys

# 3. Run your first agent
python agent_runner.py --interactive
```

## Patterns Implemented

### 1. Prompt Chaining Pattern
Overview
Prompt chaining is an agentic AI pattern where the output of one AI prompt becomes the input to the next prompt in a sequence. This creates a pipeline of interconnected AI interactions that can solve complex problems by breaking them down into smaller, manageable steps.

Key Concepts
Sequential Processing: Each step in the chain builds upon the previous step's output
Context Preservation: Information flows from one prompt to the next
Modularity: Each step can be optimized independently
Error Propagation: Issues in early steps can affect later steps
Pattern Structure
Input → Prompt 1 → Output 1 → Prompt 2 → Output 2 → ... → Final Output


### 2. Simple Agent Pattern
This is the most basic agentic AI pattern where a single agent handles all types of requests.

Overview
The Simple Agent pattern involves a single AI agent that processes all incoming requests without any specialization or routing logic. This is the foundation pattern that other more complex patterns build upon.

Key Characteristics
Single Point of Entry: All requests go to one agent
General Purpose: The agent tries to handle all types of queries
No Specialization: No domain-specific optimization
Simple Architecture: Minimal complexity in design
Use Cases
Prototyping and early development
Simple chatbots with general knowledge
Applications where request volume and complexity are low
Educational purposes to understand basic agent behavior
Implementation
The implementation demonstrates a basic agent that can handle various types of questions using a general-purpose approach.

### 3. Routing Agent Pattern
The Routing pattern directs different types of queries or tasks to specialized agents or components based on the nature of the request.

Overview
The Routing Agent pattern implements intelligent request distribution where a central router analyzes incoming requests and directs them to the most appropriate specialized agent. This pattern enables better performance through specialization while maintaining a unified interface.

Key Characteristics
Central Router: A main component that analyzes and routes requests
Specialized Agents: Multiple agents, each optimized for specific domains or task types
Intent Classification: Automatic determination of request type and appropriate handler
Scalable Architecture: Easy to add new specialized agents
Load Distribution: Requests are distributed based on capability rather than load
Pattern Components
Router Agent: Analyzes requests and determines routing
Specialized Agents: Domain-specific agents (e.g., Math, Creative Writing, Code, etc.)
Registry: Maintains mapping between request types and available agents
Fallback Handler: Handles requests that don't match any specialized agent

### 4. Parallelization Pattern
Overview
The Parallelization pattern enables running multiple AI tasks simultaneously across different LLM providers to achieve faster overall completion times and leverage the strengths of different models.

Key Concepts
1. Concurrent Execution
Run multiple AI tasks simultaneously instead of sequentially
Utilize different providers (OpenAI, Gemini, Ollama) in parallel
Maximize throughput and minimize total execution time
2. Task Dependencies
Support task dependencies where some tasks must complete before others can start
Automatic dependency resolution and execution ordering
Enable complex workflows with parallel and sequential components
3. Provider Diversity
Leverage different AI providers for different strengths:
OpenAI: High quality, reliable responses
Gemini: Fast responses, good for analysis
Ollama: Local/private processing, cost-effective
Compare outputs from multiple providers
Fallback options if one provider fails
4. Resource Management
Configurable concurrency limits to prevent resource exhaustion
Task prioritization (HIGH, NORMAL, LOW, CRITICAL)
Timeout management per task and provider


## License

MIT License - feel free to use these patterns in your own projects!
