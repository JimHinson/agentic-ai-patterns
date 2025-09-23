# Ollama Setup Guide

This guide shows you how to use Ollama (local LLM) with the agentic AI patterns.

## Prerequisites

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Start Ollama**: It should start automatically, or run `ollama serve`
3. **Pull a Model**: Download a model to use

## Quick Start

### 1. Install and Pull a Model
```bash
# Pull Llama 3.1 8B (recommended for most use cases)
ollama pull llama3.1:8b

# Or pull other models:
ollama pull mistral:7b        # Good for general tasks
ollama pull codellama:7b      # Good for coding tasks
ollama pull llama2:7b         # Alternative option
```

### 2. Test Ollama is Working
```bash
# Check available models
curl http://localhost:11434/api/tags

# Test generation
ollama run llama3.1:8b "Hello, how are you?"
```

### 3. Use with Agent Framework

#### Main Agent Framework (Recommended)
```bash
# Use Ollama with the main framework
python agent_runner.py --provider ollama --model "llama3.1:8b" --topic "your topic here"

# Interactive mode
python agent_runner.py --provider ollama --interactive
```

#### Routing Agent with Ollama
```bash
# Run the Ollama routing demo
cd 02_routing_agent
python ollama_routing_example.py

# Interactive routing demo
python ollama_routing_example.py --interactive
```

## Available Models

Popular models you can use:

| Model | Size | Best For |
|-------|------|----------|
| `llama3.1:8b` | ~4.7GB | General tasks, balanced performance |
| `llama3.1:70b` | ~40GB | High-quality results (needs lots of RAM) |
| `mistral:7b` | ~4.1GB | Fast responses, good reasoning |
| `codellama:7b` | ~3.8GB | Programming and code generation |
| `codellama:13b` | ~7.3GB | Better programming, more RAM needed |
| `neural-chat:7b` | ~4.1GB | Conversational AI |
| `vicuna:7b` | ~3.8GB | Instruction following |

## Configuration

### Environment Variables
Add to your `.env` file:
```bash
# Ollama Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434  # Default Ollama server
DEFAULT_OLLAMA_MODEL=llama3.1:8b       # Your preferred model
```

### Custom Ollama Server
If running Ollama on a different host/port:
```bash
python agent_runner.py --provider ollama --model "llama3.1:8b" --config '{"base_url": "http://your-server:11434"}'
```

## Benefits of Using Ollama

✅ **Privacy**: Everything runs locally, no data sent to external APIs
✅ **Cost**: No API costs after initial setup
✅ **Speed**: Fast responses once model is loaded
✅ **Offline**: Works without internet connection
✅ **Control**: Full control over model behavior and parameters

## Troubleshooting

### Common Issues

**"Cannot connect to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is available: `curl http://localhost:11434/api/tags`

**"Model not found"**
- Pull the model first: `ollama pull llama3.1:8b`
- Check available models: `ollama list`

**Slow responses**
- Use smaller models like `llama3.1:8b` instead of `llama3.1:70b`
- Ensure you have enough RAM (8GB+ recommended)

**Out of memory errors**
- Try smaller models
- Close other applications to free RAM
- Use models like `orca-mini:3b` for low-resource systems

## Performance Tips

1. **Model Selection**: Start with `llama3.1:8b` - good balance of quality and speed
2. **Hardware**: 16GB+ RAM recommended for smooth operation
3. **GPU**: Ollama can use GPU acceleration if available
4. **Concurrent Requests**: Ollama handles multiple requests efficiently

## Next Steps

- Try the interactive demo to see routing in action
- Experiment with different models for different tasks
- Check out the main agent framework for prompt chaining patterns
- Build your own specialized agents using the examples