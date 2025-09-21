# agentic-ai-patterns
Examples of the 20 patterns presented by Mark Kashef in his YouTube video "Master ALL 20 Agentic AI Design Patterns [Complete Course]"

## Pattern Examples

This repository contains practical implementations of key agentic AI patterns, starting with foundational patterns and building up to more complex architectures.

### 01. Simple Agent Pattern
**Location:** `01_simple_agent/`

The most basic agentic AI pattern where a single agent handles all types of requests without specialization. This serves as the foundation for understanding more complex patterns.

**Key Features:**
- Single general-purpose agent
- Handles all request types
- Simple conversation memory
- Basic error handling

**Use Cases:**
- Prototyping and early development
- Simple chatbots
- Educational purposes
- Low-complexity applications

### 02. Routing Agent Pattern
**Location:** `02_routing_agent/`

An intelligent routing system that analyzes incoming requests and directs them to specialized agents based on request type and content. This pattern demonstrates how to achieve better performance through specialization while maintaining a unified interface.

**Key Features:**
- Central router with intelligent request classification
- Multiple specialized agents (Math, Code, Creative, Factual, Analysis)
- Agent registry system for managing capabilities
- Performance monitoring and load balancing
- Graceful fallback mechanisms

**Use Cases:**
- Multi-domain chatbots
- Enterprise applications with different functional areas
- Educational platforms with subject-specific tutors
- Content management systems
- API gateways for microservices

## Getting Started

Each pattern example includes:
- Comprehensive implementation with detailed comments
- Usage examples and demonstrations
- README with pattern explanation and use cases
- Requirements file with dependencies

To run any example:

1. Install dependencies:
```bash
cd <pattern_folder>
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the example:
```bash
python example.py
```

## Pattern Comparison

| Pattern | Complexity | Specialization | Performance | Scalability |
|---------|------------|---------------|-------------|-------------|
| Simple Agent | Low | None | General | Limited |
| Routing Agent | Medium | High | Specialized | Good |

## Future Patterns

This repository will be expanded to include additional agentic AI patterns such as:
- Hierarchical agents
- Pipeline patterns
- Collaborative agent patterns
- And more...

## Contributing

Feel free to contribute additional pattern implementations or improvements to existing examples.
