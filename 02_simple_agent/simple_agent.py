"""
Simple Agent Pattern Implementation

This module demonstrates the most basic agentic AI pattern where a single agent
handles all types of requests without any specialization or routing.
"""

import openai
from typing import Dict, Any, Optional
import json
import os


class SimpleAgent:
    """
    A simple, general-purpose AI agent that handles all types of requests.
    
    This agent represents the foundational pattern in agentic AI where a single
    agent attempts to handle all incoming requests without specialization.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the Simple Agent.
        
        Args:
            api_key: OpenAI API key (if None, expects OPENAI_API_KEY env var)
            model: The OpenAI model to use for completions
        """
        self.api_key = api_key
        self.client = None
        if api_key or os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history = []
        
        # General system prompt for the agent
        self.system_prompt = """
        You are a helpful AI assistant. You can help with a wide variety of tasks including:
        - Answering questions on various topics
        - Writing and editing text
        - Providing explanations and tutorials
        - Helping with problem-solving
        - Creative tasks like brainstorming
        - Basic data analysis and calculations
        
        Always strive to be helpful, accurate, and clear in your responses.
        If you're unsure about something, acknowledge the uncertainty.
        """
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request and return a response.
        
        Args:
            user_input: The user's input/question
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            if not self.client:
                return {
                    "success": False,
                    "error": "OpenAI API key not provided. Set OPENAI_API_KEY environment variable.",
                    "pattern": "simple_agent"
                }
            
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user", 
                "content": user_input
            })
            
            # Prepare messages for API call
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            # Extract response content
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return {
                "success": True,
                "response": assistant_response,
                "pattern": "simple_agent",
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "conversation_length": len(self.conversation_history)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pattern": "simple_agent"
            }
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
    
    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history.copy()


def main():
    """Example usage of the Simple Agent."""
    import os
    
    # Initialize the agent
    agent = SimpleAgent()
    
    print("Simple Agent Pattern Demo")
    print("=" * 40)
    
    # Example interactions
    examples = [
        "What is artificial intelligence?",
        "Help me write a short poem about nature",
        "Explain the concept of machine learning in simple terms",
        "What's 15% of 240?",
        "Give me 3 tips for better time management"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. User: {example}")
        result = agent.process_request(example)
        
        if result["success"]:
            print(f"Agent: {result['response']}")
            print(f"Tokens used: {result['metadata']['tokens_used']}")
        else:
            print(f"Error: {result['error']}")
        
        print("-" * 40)


if __name__ == "__main__":
    main()