"""
Agent Registry for PATH Framework.

Manages registration, discovery, and lifecycle of all agents.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Type, Any
from uuid import UUID

from .base import BaseAgent, AgentStatus, AgentTask, AgentMessage
from ..exceptions import AgentError


class AgentRegistry:
    """
    Central registry for managing all PATH Framework agents.
    
    Provides functionality for:
    - Agent registration and discovery
    - Message routing between agents
    - Task orchestration
    - Lifecycle management
    """
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._agent_classes: Dict[str, Type[BaseAgent]] = {}
        self._message_queue: List[AgentMessage] = []
        self.logger = logging.getLogger("path.registry")
        
    def register_agent_class(self, agent_class: Type[BaseAgent], agent_type: str):
        """
        Register an agent class for later instantiation.
        
        Args:
            agent_class: The agent class to register
            agent_type: Unique type identifier for the agent
        """
        self._agent_classes[agent_type] = agent_class
        self.logger.info(f"Registered agent class: {agent_type}")
    
    def create_agent(self, agent_type: str, agent_id: str, **kwargs) -> BaseAgent:
        """
        Create an agent instance from registered class.
        
        Args:
            agent_type: Type of agent to create
            agent_id: Unique ID for the agent instance
            **kwargs: Additional arguments for agent constructor
            
        Returns:
            Created agent instance
            
        Raises:
            AgentError: If agent type not registered or creation fails
        """
        if agent_type not in self._agent_classes:
            raise AgentError(f"Unknown agent type: {agent_type}")
            
        if agent_id in self._agents:
            raise AgentError(f"Agent with ID {agent_id} already exists")
            
        try:
            agent_class = self._agent_classes[agent_type]
            agent = agent_class(agent_id=agent_id, **kwargs)
            self._agents[agent_id] = agent
            
            self.logger.info(f"Created agent: {agent_id} ({agent_type})")
            return agent
            
        except Exception as e:
            raise AgentError(f"Failed to create agent {agent_id}: {e}")
    
    def register_agent(self, agent: BaseAgent):
        """
        Register an existing agent instance.
        
        Args:
            agent: The agent instance to register
            
        Raises:
            AgentError: If agent ID already exists
        """
        if agent.agent_id in self._agents:
            raise AgentError(f"Agent with ID {agent.agent_id} already exists")
            
        self._agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.agent_id}")
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: ID of the agent to retrieve
            
        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_id)
    
    def remove_agent(self, agent_id: str) -> bool:
        """
        Remove an agent from the registry.
        
        Args:
            agent_id: ID of the agent to remove
            
        Returns:
            True if agent was removed, False if not found
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
            self.logger.info(f"Removed agent: {agent_id}")
            return True
        return False
    
    def list_agents(self) -> List[BaseAgent]:
        """
        Get all registered agents.
        
        Returns:
            List of all agent instances
        """
        return list(self._agents.values())
    
    def list_agent_ids(self) -> List[str]:
        """
        Get all registered agent IDs.
        
        Returns:
            List of agent IDs
        """
        return list(self._agents.keys())
    
    def list_agent_types(self) -> List[str]:
        """
        Get all registered agent types.
        
        Returns:
            List of agent type names
        """
        return list(self._agent_classes.keys())
    
    def get_agents_by_phase(self, phase: str) -> List[BaseAgent]:
        """
        Get all agents for a specific phase.
        
        Args:
            phase: Phase name to filter by
            
        Returns:
            List of agents in the specified phase
        """
        return [agent for agent in self._agents.values() if agent.phase == phase]
    
    def get_agents_by_status(self, status: AgentStatus) -> List[BaseAgent]:
        """
        Get all agents with a specific status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of agents with the specified status
        """
        return [agent for agent in self._agents.values() if agent.status == status]
    
    def get_agents_by_capability(self, capability: str) -> List[BaseAgent]:
        """
        Get all agents with a specific capability.
        
        Args:
            capability: Capability to filter by
            
        Returns:
            List of agents with the specified capability
        """
        return [agent for agent in self._agents.values() if capability in agent.capabilities]
    
    async def route_message(self, message: AgentMessage) -> bool:
        """
        Route a message to the appropriate agent.
        
        Args:
            message: Message to route
            
        Returns:
            True if message was delivered, False otherwise
        """
        recipient = self.get_agent(message.recipient)
        if not recipient:
            self.logger.warning(f"Cannot route message: recipient {message.recipient} not found")
            return False
            
        await recipient.receive_message(message)
        return True
    
    async def broadcast_message(self, sender_id: str, message_type: str, 
                               content: Dict[str, Any], exclude_sender: bool = True) -> int:
        """
        Broadcast a message to all agents.
        
        Args:
            sender_id: ID of the sending agent
            message_type: Type of message
            content: Message content
            exclude_sender: Whether to exclude the sender from broadcast
            
        Returns:
            Number of agents that received the message
        """
        recipients = []
        for agent_id, agent in self._agents.items():
            if exclude_sender and agent_id == sender_id:
                continue
            recipients.append(agent)
        
        message_count = 0
        for agent in recipients:
            message = AgentMessage(
                sender=sender_id,
                recipient=agent.agent_id,
                message_type=message_type,
                content=content
            )
            await agent.receive_message(message)
            message_count += 1
            
        self.logger.debug(f"Broadcast message from {sender_id} to {message_count} agents")
        return message_count
    
    async def assign_task(self, agent_id: str, task: AgentTask) -> UUID:
        """
        Assign a task to a specific agent.
        
        Args:
            agent_id: ID of the agent to assign the task to
            task: Task to assign
            
        Returns:
            Task ID
            
        Raises:
            AgentError: If agent not found or cannot accept task
        """
        agent = self.get_agent(agent_id)
        if not agent:
            raise AgentError(f"Agent {agent_id} not found")
            
        task.agent_id = agent_id
        return await agent.start_task(task)
    
    async def find_available_agent(self, capabilities: List[str], phase: Optional[str] = None) -> Optional[BaseAgent]:
        """
        Find an available agent with specific capabilities.
        
        Args:
            capabilities: Required capabilities
            phase: Optional phase filter
            
        Returns:
            Available agent or None if not found
        """
        for agent in self._agents.values():
            if agent.status != AgentStatus.IDLE:
                continue
                
            if phase and agent.phase != phase:
                continue
                
            if all(cap in agent.capabilities for cap in capabilities):
                return agent
                
        return None
    
    def get_registry_status(self) -> Dict[str, Any]:
        """
        Get overall registry status.
        
        Returns:
            Dictionary with registry statistics
        """
        status_counts = {}
        phase_counts = {}
        
        for agent in self._agents.values():
            status = agent.status.value
            phase = agent.phase
            
            status_counts[status] = status_counts.get(status, 0) + 1
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        return {
            "total_agents": len(self._agents),
            "registered_types": len(self._agent_classes),
            "status_distribution": status_counts,
            "phase_distribution": phase_counts,
            "message_queue_size": len(self._message_queue)
        }
    
    async def shutdown_all_agents(self):
        """Gracefully shutdown all agents."""
        self.logger.info("Shutting down all agents...")
        
        for agent in self._agents.values():
            if agent.current_task:
                self.logger.warning(f"Agent {agent.agent_id} has active task during shutdown")
        
        self._agents.clear()
        self.logger.info("All agents shut down")
    
    def __len__(self) -> int:
        """Get number of registered agents."""
        return len(self._agents)
    
    def __contains__(self, agent_id: str) -> bool:
        """Check if agent is registered."""
        return agent_id in self._agents
    
    def __iter__(self):
        """Iterate over agents."""
        return iter(self._agents.values())
