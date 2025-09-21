"""
Configuration settings for the Parallelization Agentic AI Pattern examples.
"""
import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"  # You can change to gpt-4 for better results
MAX_TOKENS = 1000

# Parallelization Settings
MAX_CONCURRENT_AGENTS = 5  # Maximum number of parallel agents
TIMEOUT_SECONDS = 60      # Timeout for individual agent tasks

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Output Settings
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"