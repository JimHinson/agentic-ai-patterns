"""
Agent Registry for the Routing Pattern

This module provides a registry system for managing specialized agents
and their capabilities in the routing pattern.
"""

from typing import Dict, List, Any, Optional
from routing_agent import RequestType
from specialized_agents import (
    MathAgent, CodeAgent, CreativeAgent, 
    FactualAgent, AnalysisAgent, GeneralAgent
)


class AgentRegistry:
    """
    Registry system for managing specialized agents and their capabilities.
    
    The registry maintains information about available agents, their specializations,
    and performance metrics for routing decisions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent registry.
        
        Args:
            api_key: OpenAI API key to pass to specialized agents
        """
        self.api_key = api_key
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.type_mappings: Dict[RequestType, List[str]] = {
            request_type: [] for request_type in RequestType
        }
        
    def register_agent(self, agent_id: str, agent_class, request_types: List[RequestType], 
                      priority: int = 5, metadata: Optional[Dict] = None):
        """
        Register a new specialized agent.
        
        Args:
            agent_id: Unique identifier for the agent
            agent_class: Class of the agent to instantiate
            request_types: List of request types this agent can handle
            priority: Priority level (1-10, higher is better)
            metadata: Additional metadata about the agent
        """
        # Create agent instance
        agent_instance = agent_class(api_key=self.api_key)
        
        # Store agent information
        self.agents[agent_id] = {
            'instance': agent_instance,
            'class': agent_class,
            'types': request_types,
            'priority': priority,
            'requests_handled': 0,
            'success_rate': 1.0,
            'average_response_time': 0.0,
            'metadata': metadata or {},
            'active': True
        }
        
        # Update type mappings
        for request_type in request_types:
            if agent_id not in self.type_mappings[request_type]:
                self.type_mappings[request_type].append(agent_id)
                # Sort by priority (descending)
                self.type_mappings[request_type].sort(
                    key=lambda aid: self.agents[aid]['priority'], 
                    reverse=True
                )
    
    def get_agent(self, agent_id: str) -> Optional[Any]:
        """Get an agent instance by ID."""
        if agent_id in self.agents and self.agents[agent_id]['active']:
            return self.agents[agent_id]['instance']
        return None
    
    def get_agents_for_type(self, request_type: RequestType) -> List[str]:
        """Get list of agent IDs that can handle a specific request type."""
        return [aid for aid in self.type_mappings[request_type] 
                if self.agents[aid]['active']]
    
    def get_best_agent(self, request_type: RequestType) -> Optional[str]:
        """
        Get the best agent for a specific request type based on priority and performance.
        
        Args:
            request_type: The type of request to route
            
        Returns:
            Agent ID of the best available agent, or None if no suitable agent
        """
        suitable_agents = self.get_agents_for_type(request_type)
        
        if not suitable_agents:
            # Fallback to general agent
            return "general_agent" if "general_agent" in self.agents else None
        
        # Score agents based on priority, success rate, and load
        scored_agents = []
        for agent_id in suitable_agents:
            agent_info = self.agents[agent_id]
            # Score = priority * success_rate / (1 + requests_handled/100)
            load_factor = 1 + (agent_info['requests_handled'] / 100)
            score = (agent_info['priority'] * agent_info['success_rate']) / load_factor
            scored_agents.append((agent_id, score))
        
        # Return agent with highest score
        return max(scored_agents, key=lambda x: x[1])[0]
    
    def update_agent_performance(self, agent_id: str, success: bool, response_time: float):
        """
        Update performance metrics for an agent.
        
        Args:
            agent_id: ID of the agent to update
            success: Whether the request was successful
            response_time: Time taken to process the request
        """
        if agent_id not in self.agents:
            return
        
        agent_info = self.agents[agent_id]
        
        # Update request counter
        agent_info['requests_handled'] += 1
        
        # Update success rate (moving average)
        current_rate = agent_info['success_rate']
        total_requests = agent_info['requests_handled']
        if success:
            agent_info['success_rate'] = ((current_rate * (total_requests - 1)) + 1.0) / total_requests
        else:
            agent_info['success_rate'] = (current_rate * (total_requests - 1)) / total_requests
        
        # Update average response time (moving average)
        current_time = agent_info['average_response_time']
        agent_info['average_response_time'] = ((current_time * (total_requests - 1)) + response_time) / total_requests
    
    def deactivate_agent(self, agent_id: str):
        """Deactivate an agent (temporarily remove from routing)."""
        if agent_id in self.agents:
            self.agents[agent_id]['active'] = False
    
    def activate_agent(self, agent_id: str):
        """Activate a previously deactivated agent."""
        if agent_id in self.agents:
            self.agents[agent_id]['active'] = True
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the registry."""
        total_agents = len(self.agents)
        active_agents = sum(1 for a in self.agents.values() if a['active'])
        total_requests = sum(a['requests_handled'] for a in self.agents.values())
        
        agent_stats = {}
        for agent_id, agent_info in self.agents.items():
            agent_stats[agent_id] = {
                'type': agent_info['instance'].agent_type,
                'active': agent_info['active'],
                'priority': agent_info['priority'],
                'requests_handled': agent_info['requests_handled'],
                'success_rate': round(agent_info['success_rate'], 3),
                'average_response_time': round(agent_info['average_response_time'], 3),
                'supported_types': [t.value for t in agent_info['types']]
            }
        
        type_coverage = {}
        for request_type, agent_ids in self.type_mappings.items():
            active_agents_for_type = [aid for aid in agent_ids if self.agents[aid]['active']]
            type_coverage[request_type.value] = {
                'agent_count': len(active_agents_for_type),
                'agents': active_agents_for_type
            }
        
        return {
            'summary': {
                'total_agents': total_agents,
                'active_agents': active_agents,
                'total_requests_handled': total_requests
            },
            'agents': agent_stats,
            'type_coverage': type_coverage
        }
    
    def setup_default_agents(self):
        """Set up the default set of specialized agents."""
        # Math Agent
        self.register_agent(
            'math_agent',
            MathAgent,
            [RequestType.MATH],
            priority=9,
            metadata={'description': 'Specialized in mathematical calculations and problems'}
        )
        
        # Code Agent
        self.register_agent(
            'code_agent',
            CodeAgent,
            [RequestType.CODE],
            priority=9,
            metadata={'description': 'Specialized in programming and software development'}
        )
        
        # Creative Agent
        self.register_agent(
            'creative_agent',
            CreativeAgent,
            [RequestType.CREATIVE],
            priority=8,
            metadata={'description': 'Specialized in creative writing and artistic tasks'}
        )
        
        # Factual Agent
        self.register_agent(
            'factual_agent',
            FactualAgent,
            [RequestType.FACTUAL],
            priority=8,
            metadata={'description': 'Specialized in factual information and knowledge'}
        )
        
        # Analysis Agent
        self.register_agent(
            'analysis_agent',
            AnalysisAgent,
            [RequestType.ANALYSIS],
            priority=8,
            metadata={'description': 'Specialized in analysis and critical thinking'}
        )
        
        # General Agent (fallback)
        self.register_agent(
            'general_agent',
            GeneralAgent,
            [RequestType.GENERAL, RequestType.MATH, RequestType.CODE, 
             RequestType.CREATIVE, RequestType.FACTUAL, RequestType.ANALYSIS],
            priority=3,  # Lower priority, used as fallback
            metadata={'description': 'General purpose agent for mixed or unclear requests'}
        )


def create_default_registry(api_key: Optional[str] = None) -> AgentRegistry:
    """
    Create and configure a default agent registry with standard specialized agents.
    
    Args:
        api_key: OpenAI API key to pass to agents
        
    Returns:
        Configured AgentRegistry instance
    """
    registry = AgentRegistry(api_key=api_key)
    registry.setup_default_agents()
    return registry


if __name__ == "__main__":
    # Demo the registry system
    print("Agent Registry Demo")
    print("=" * 40)
    
    registry = create_default_registry()
    
    print("Registry Statistics:")
    stats = registry.get_registry_stats()
    
    print(f"Total Agents: {stats['summary']['total_agents']}")
    print(f"Active Agents: {stats['summary']['active_agents']}")
    
    print("\nAgent Details:")
    for agent_id, agent_info in stats['agents'].items():
        print(f"  {agent_id}:")
        print(f"    Type: {agent_info['type']}")
        print(f"    Priority: {agent_info['priority']}")
        print(f"    Supported Types: {', '.join(agent_info['supported_types'])}")
    
    print("\nType Coverage:")
    for request_type, coverage in stats['type_coverage'].items():
        print(f"  {request_type}: {coverage['agent_count']} agents ({', '.join(coverage['agents'])})")
    
    print("\nRouting Examples:")
    routing_examples = [
        (RequestType.MATH, "Mathematical calculation"),
        (RequestType.CODE, "Programming task"),
        (RequestType.CREATIVE, "Creative writing"),
        (RequestType.FACTUAL, "Factual question"),
        (RequestType.ANALYSIS, "Analysis task"),
        (RequestType.GENERAL, "General conversation")
    ]
    
    for request_type, description in routing_examples:
        best_agent = registry.get_best_agent(request_type)
        print(f"  {description} → {best_agent}")