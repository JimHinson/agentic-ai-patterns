# Agent Setup Guide

This guide will help you set up and run actual AI agents using the agentic patterns in this repository.

## Quick Start

### 1. Install Dependencies

```bash
cd agentic-ai-patterns
pip install -r 01_prompt_chaining/requirements.txt
```

### 2. Set Up API Keys

Copy the environment template:
```bash
copy .env.example .env
```

Edit `.env` and add your API keys:
```bash
# For OpenAI
OPENAI_API_KEY=sk-your-key-here

# For Anthropic
ANTHROPIC_API_KEY=your-key-here

# For Google Gemini
GOOGLE_API_KEY=your-key-here
```

### 3. Run Your First Agent

Interactive mode (recommended for first time):
```bash
python agent_runner.py --interactive
```

Command line mode:
```bash
python agent_runner.py --pattern prompt_chaining --topic "Machine Learning"
```

## Getting API Keys

### OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file
5. Make sure you have credits in your account

**Recommended models:**
- `gpt-4o-mini` - Fast and cost-effective
- `gpt-4o` - High quality but more expensive

### Anthropic API Key
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

### Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file
5. Note: Gemini has generous free tier limits

**Recommended models:**
- `gemini-1.5-flash` - Fast and cost-effective (recommended)
- `gemini-1.5-pro` - Higher quality, more capable
- `gemini-1.0-pro` - Original Gemini model

## Available Commands

### List Available Providers
```bash
python agent_runner.py --list-providers
```

### Run Specific Patterns

**Prompt Chaining with OpenAI:**
```bash
python agent_runner.py --pattern prompt_chaining --provider openai --topic "Climate Change"
```

**Prompt Chaining with Gemini:**
```bash
python agent_runner.py --pattern prompt_chaining --provider gemini --topic "Renewable Energy"
```

**Specify Gemini Model:**
```bash
python agent_runner.py --provider gemini --model gemini-1.5-pro --topic "Quantum Computing"
```

**Specify Output File:**
```bash
python agent_runner.py --pattern prompt_chaining --topic "AI Ethics" --output my_article.md
```

### Interactive Mode
```bash
python agent_runner.py --interactive
```

Interactive mode will:
1. Show available providers
2. Let you choose provider and model
3. Ask for a topic
4. Generate the article with real-time progress

## Understanding the Output

Each run generates two files:
1. **Article file** (`.md`) - The generated article
2. **Log file** (`_log.json`) - Execution details and timing

Example output structure:
```
generated_article_openai_climate_change.md
generated_article_openai_climate_change_log.json
```

## Configuration

### Model Settings

Edit `config.json` to customize:
- Available models for each provider
- Default generation settings (temperature, max_tokens)
- Pattern-specific configurations

### Custom Prompts

The agent framework is modular. You can create custom patterns by:
1. Creating new `AgentStep` instances
2. Adding them to an `AgentChain`
3. Running with your chosen LLM provider

Example:
```python
from agent_core import AgentChain, AgentStep, AgentConfig

# Create custom chain
config = AgentConfig(provider="openai", model="gpt-4o-mini")
chain = AgentChain("Custom Chain", config)

# Add custom step
step = AgentStep(
    name="custom_step",
    prompt_template="Analyze this topic: {topic}\n\nPrevious context: {previous_output}",
    system_prompt="You are an expert analyst.",
    description="Custom analysis step"
)
chain.add_step(step)

# Execute
result = chain.execute(topic="Your topic here")
```

## Troubleshooting

### Common Issues

**Import errors:**
- Make sure you've installed the requirements: `pip install -r 01_prompt_chaining/requirements.txt`

**API key errors:**
- Check that your `.env` file exists and has valid API keys
- Verify you have credits/access for your chosen provider

**Model not available:**
- Use `--list-providers` to see available models
- Check that your API key has access to the requested model

**Rate limiting:**
- Some providers have rate limits for new accounts
- Try using different models or wait between requests

### Getting Help

1. Use `--list-providers` to check your setup
2. Try interactive mode first to test your configuration
3. Check the execution log files for detailed error information
4. Start with smaller, simpler topics to test your setup

## Next Steps

Once you have the basic setup working:

1. **Explore different topics** - Try various subjects to see how the agent handles different domains
2. **Experiment with models** - Compare outputs from different models and providers
3. **Create custom patterns** - Use the agent framework to implement other agentic patterns
4. **Integrate into applications** - Use the agent framework in your own projects

## Cost Management

**OpenAI Pricing (approximate):**
- GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- GPT-4o: ~$5 per 1M input tokens, ~$15 per 1M output tokens

**Anthropic Pricing (approximate):**
- Claude 3 Haiku: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- Claude 3 Sonnet: ~$3 per 1M input tokens, ~$15 per 1M output tokens

**Gemini Pricing (approximate):**
- Gemini 1.5 Flash: Free tier available, then ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
- Gemini 1.5 Pro: Free tier available, then ~$1.25 per 1M input tokens, ~$5 per 1M output tokens

**Tips for cost control:**
- Start with Gemini 1.5 Flash (often free and very capable)
- Use smaller, cheaper models (gpt-4o-mini, claude-3-haiku, gemini-1.5-flash)
- Use shorter topics and prompts for testing
- Monitor your usage in the provider dashboards
- Set up billing alerts in your provider accounts