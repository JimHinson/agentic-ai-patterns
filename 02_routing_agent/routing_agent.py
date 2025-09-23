"""
Routing Agent Pattern Implementation

This module implements the routing pattern where a central router analyzes
incoming requests and directs them to specialized agents based on the request type.
"""

import openai
from typing import Dict, Any, Optional, List
import json
import re
import os
from dataclasses import dataclass
from enum import Enum


class RequestType(Enum):
    """Enumeration of different request types for routing."""
    MATH = "math"
    CODE = "code"
    CREATIVE = "creative"
    FACTUAL = "factual"
    ANALYSIS = "analysis"
    GENERAL = "general"


@dataclass
class RoutingDecision:
    """Represents a routing decision made by the router."""
    request_type: RequestType
    confidence: float
    agent_id: str
    reasoning: str


class RouterAgent:
    """
    Central router that analyzes requests and routes them to appropriate agents.
    
    The router uses pattern matching and LLM-based classification to determine
    the best agent for handling each request.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the Router Agent.
        
        Args:
            api_key: OpenAI API key (if None, expects OPENAI_API_KEY env var)
            model: The OpenAI model to use for classification
        """
        self.api_key = api_key
        self.client = None
        if api_key or os.getenv("OPENAI_API_KEY"):
            self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.agent_registry = {}
        
        # Routing patterns for quick classification
        self.routing_patterns = {
            RequestType.MATH: [
                r'\b(?:calculate|compute|solve|equation|formula|math|algebra|geometry|statistics|probability)\b',
                r'\b(?:\d+\s*[+\-*/]\s*\d+|\d+%|square root|derivative|integral)\b',
                r'\b(?:area|volume|circumference|diameter|radius|angle|triangle|circle)\b'
            ],
            RequestType.CODE: [
                r'\b(?:python|javascript|java|c\+\+|html|css|sql|function|class|variable|loop|if|else)\b',
                r'\b(?:debug|code|programming|software|algorithm|data structure|api|database)\b',
                r'\b(?:compile|syntax|error|bug|script|library|framework|repository)\b',
                r'\b(?:def |function |class |import |from |return |print\()\b'
            ],
            RequestType.CREATIVE: [
                r'\b(?:write|create|poem|story|song|lyrics|creative|artistic|design|brainstorm)\b',
                r'\b(?:imagine|invent|compose|craft|generate|original|unique|innovative)\b',
                r'\b(?:haiku|novel|script|dialogue|character|plot|theme|metaphor)\b'
            ],
            RequestType.FACTUAL: [
                r'\b(?:what is|who is|when did|where is|how many|fact|definition|explain|describe)\b',
                r'\b(?:history|geography|science|biology|physics|chemistry|capital|population|date)\b',
                r'\b(?:information|knowledge|truth|accurate|correct|precise)\b'
            ],
            RequestType.ANALYSIS: [
                r'\b(?:analyze|compare|contrast|evaluate|assess|critique|review|examine)\b',
                r'\b(?:pros and cons|advantages|disadvantages|strengths|weaknesses|trade-off)\b',
                r'\b(?:trend|pattern|correlation|relationship|impact|effect|influence)\b'
            ]
        }
    
    def register_agent(self, agent_id: str, agent_instance, request_types: List[RequestType]):
        """
        Register a specialized agent with the router.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_instance: The agent instance to register
            request_types: List of request types this agent can handle
        """
        self.agent_registry[agent_id] = {
            'instance': agent_instance,
            'types': request_types,
            'requests_handled': 0
        }
    
    def _pattern_classify(self, user_input: str) -> Optional[RequestType]:
        """
        Quick pattern-based classification using regex patterns.
        
        Args:
            user_input: User input to classify
            
        Returns:
            Classified request type or None if no pattern matches
        """
        input_lower = user_input.lower()
        
        for request_type, patterns in self.routing_patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower):
                    return request_type
        
        return None
    
    def _llm_classify(self, user_input: str) -> RoutingDecision:
        """
        Use LLM for more sophisticated request classification.
        
        Args:
            user_input: User input to classify
            
        Returns:
            RoutingDecision with classification results
        """
        classification_prompt = f"""
        Analyze the following user request and classify it into one of these categories:
        
        1. MATH - Mathematical calculations, equations, geometry, statistics
        2. CODE - Programming, software development, debugging, technical implementation
        3. CREATIVE - Writing, brainstorming, artistic tasks, content creation
        4. FACTUAL - Questions seeking specific facts, definitions, explanations
        5. ANALYSIS - Comparative analysis, evaluation, critical thinking tasks
        6. GENERAL - General conversation, unclear requests, or mixed topics
        
        User request: "{user_input}"
        
        Respond with ONLY a JSON object in this format:
        {{
            "category": "CATEGORY_NAME",
            "confidence": 0.85,
            "reasoning": "Brief explanation of why this category was chosen"
        }}
        """
        
        try:
            if not self.client:
                # Fallback to general category when no API client available
                return RoutingDecision(
                    request_type=RequestType.GENERAL,
                    confidence=0.5,
                    agent_id="general_agent",
                    reasoning="No LLM available for classification"
                )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            request_type = RequestType(result["category"].lower())
            confidence = float(result["confidence"])
            reasoning = result["reasoning"]
            
            # Find the best agent for this request type
            agent_id = self._find_best_agent(request_type)
            
            return RoutingDecision(
                request_type=request_type,
                confidence=confidence,
                agent_id=agent_id,
                reasoning=reasoning
            )
            
        except Exception as e:
            # Fallback to general category
            return RoutingDecision(
                request_type=RequestType.GENERAL,
                confidence=0.1,
                agent_id="general_agent",
                reasoning=f"Classification failed: {str(e)}"
            )
    
    def _find_best_agent(self, request_type: RequestType) -> str:
        """
        Find the best agent for a given request type.
        
        Args:
            request_type: The classified request type
            
        Returns:
            Agent ID of the best agent for this request type
        """
        # Find agents that can handle this request type
        suitable_agents = []
        for agent_id, agent_info in self.agent_registry.items():
            if request_type in agent_info['types']:
                suitable_agents.append((agent_id, agent_info['requests_handled']))
        
        if suitable_agents:
            # Return agent with least requests handled (load balancing)
            return min(suitable_agents, key=lambda x: x[1])[0]
        else:
            # Fallback to general agent
            return "general_agent"
    
    def route_request(self, user_input: str) -> RoutingDecision:
        """
        Route a user request to the appropriate agent.
        
        Args:
            user_input: The user's request
            
        Returns:
            RoutingDecision with routing information
        """
        # First try quick pattern classification
        pattern_result = self._pattern_classify(user_input)
        
        if pattern_result:
            agent_id = self._find_best_agent(pattern_result)
            return RoutingDecision(
                request_type=pattern_result,
                confidence=0.8,  # Pattern matching is fairly reliable
                agent_id=agent_id,
                reasoning="Matched routing pattern"
            )
        
        # Fall back to LLM classification
        return self._llm_classify(user_input)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a request by routing it to the appropriate agent.
        
        Args:
            user_input: The user's request
            
        Returns:
            Response from the selected agent including routing metadata
        """
        # Route the request
        routing_decision = self.route_request(user_input)
        
        # Get the appropriate agent
        if routing_decision.agent_id in self.agent_registry:
            agent_info = self.agent_registry[routing_decision.agent_id]
            agent_instance = agent_info['instance']
            
            # Process with the specialized agent
            response = agent_instance.process_request(user_input)
            
            # Update request counter
            agent_info['requests_handled'] += 1
            
            # Add routing metadata
            if response.get("success", False):
                response["routing"] = {
                    "routed_to": routing_decision.agent_id,
                    "request_type": routing_decision.request_type.value,
                    "confidence": routing_decision.confidence,
                    "reasoning": routing_decision.reasoning,
                    "pattern": "routing_agent"
                }
            
            return response
        else:
            # Agent not found - this shouldn't happen with proper setup
            return {
                "success": False,
                "error": f"Agent '{routing_decision.agent_id}' not found",
                "pattern": "routing_agent",
                "routing": {
                    "attempted_route": routing_decision.agent_id,
                    "request_type": routing_decision.request_type.value
                }
            }
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions and agent usage."""
        stats = {
            "total_agents": len(self.agent_registry),
            "agent_usage": {},
            "total_requests": 0
        }
        
        for agent_id, agent_info in self.agent_registry.items():
            requests_handled = agent_info['requests_handled']
            stats["agent_usage"][agent_id] = {
                "requests_handled": requests_handled,
                "supported_types": [t.value for t in agent_info['types']]
            }
            stats["total_requests"] += requests_handled
        
        return stats


def main():
    """Example usage of the Routing Agent."""
    print("Routing Agent Pattern Demo")
    print("=" * 40)
    
    # This would normally import and use the specialized agents
    # For demo purposes, we'll show the routing decisions
    router = RouterAgent()
    
    examples = [
        "What's the area of a circle with radius 5?",
        "Write a Python function to sort a list",
        "Create a haiku about coding",
        "What is the capital of Australia?",
        "Compare the advantages of Python vs JavaScript",
        "How are you doing today?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. User: {example}")
        routing_decision = router.route_request(example)
        print(f"Router Decision:")
        print(f"  - Type: {routing_decision.request_type.value}")
        print(f"  - Agent: {routing_decision.agent_id}")
        print(f"  - Confidence: {routing_decision.confidence}")
        print(f"  - Reasoning: {routing_decision.reasoning}")
        print("-" * 40)


if __name__ == "__main__":
    main()