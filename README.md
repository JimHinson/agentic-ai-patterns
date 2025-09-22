# agentic-ai-patterns
Examples of the 20 patterns presented by Mark Kashef in his YouTube video "Master ALL 20 Agentic AI Design Patterns [Complete Course]"

## 🚀 Quick Start with Real AI Agents

Want to run these patterns with actual LLMs? See **[AGENT_SETUP.md](AGENT_SETUP.md)** for a complete setup guide.

**Quick setup:**
```bash
# 1. Install dependencies
pip install -r prompt-chaining/requirements.txt

# 2. Set up API keys
copy .env.example .env
# Edit .env with your OpenAI/Anthropic API keys

# 3. Run your first agent
python agent_runner.py --interactive
```

## Patterns Implemented

### 1. Prompt Chaining ✅
**Location:** `prompt-chaining/`

A pattern where the output of one AI prompt becomes the input to the next prompt in a sequence, creating a pipeline of interconnected AI interactions.

**Key Features:**
- Sequential processing with context preservation
- Modular design for complex problem solving
- Comprehensive article creation example
- Multiple usage examples and patterns
- **NEW: Real LLM integration** - Run with OpenAI, Anthropic, or other providers

**Files:**
- `prompt_chaining.py` - Original implementation with mock responses
- `examples.py` - Various usage examples and patterns
- `README.md` - Detailed documentation and explanation

**Agent Framework (NEW):**
- `agent_core.py` - Core agent framework for real LLM integration
- `agent_runner.py` - Command-line interface for running agents
- `config.json` - Configuration for models and providers
- `.env.example` - Template for API keys

**Usage:**
```bash
# Original examples (mock responses)
cd prompt-chaining
python prompt_chaining.py    # Run the main article creation demo
python examples.py          # Run various usage examples

# Real AI agents (requires API keys)
python agent_runner.py --interactive                    # Interactive mode
python agent_runner.py --pattern prompt_chaining        # Command line
python agent_runner.py --provider anthropic --topic "AI Safety"    # Anthropic
python agent_runner.py --provider gemini --topic "Climate Tech"    # Google Gemini
```

## Project Structure

```
agentic-ai-patterns/
├── agent_core.py           # Core agent framework
├── agent_runner.py         # Main script for running agents
├── config.json            # Agent configuration
├── .env.example           # API key template
├── AGENT_SETUP.md         # Complete setup guide
├── README.md              # This file
└── prompt-chaining/       # Pattern 1: Prompt Chaining
    ├── prompt_chaining.py   # Original mock implementation
    ├── examples.py          # Usage examples
    ├── requirements.txt     # Dependencies
    └── README.md           # Pattern documentation
```

## Supported LLM Providers

- ✅ **OpenAI** - GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- ✅ **Anthropic** - Claude 3 Opus, Sonnet, Haiku
- ✅ **Google Gemini** - Gemini 1.5 Pro, Flash, Gemini 1.0 Pro
- 🔄 **More coming soon** - Cohere, local models via Ollama

## Contributing

We're implementing all 20 agentic patterns! Here's our roadmap:

- [x] 1. Prompt Chaining
- [ ] 2. Sequential Processing
- [ ] 3. Conditional Logic
- [ ] 4. Parallel Processing
- [ ] 5. Recursive Prompting
- [ ] 6. State Management
- [ ] 7. Tool Integration
- [ ] 8. Multi-Agent Coordination
- [ ] 9. Hierarchical Planning
- [ ] 10. Memory Integration
- [ ] ... and 10 more!

Want to contribute? Each pattern needs:
1. Core implementation in its own directory
2. Integration with the agent framework
3. Documentation and examples
4. Real LLM testing

## License

MIT License - feel free to use these patterns in your own projects!
