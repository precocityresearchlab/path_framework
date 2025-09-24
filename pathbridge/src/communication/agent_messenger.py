"""Agent-to-agent communication system."""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import json


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response" 
    NOTIFICATION = "notification"
    HANDOFF = "handoff"


@dataclass
class AgentMessage:
    """Message between agents."""
    from_agent: str
    to_agent: str
    message_type: MessageType
    payload: Dict[str, Any]
    correlation_id: str
    timestamp: str


class AgentMessenger:
    """Handles inter-agent communication."""
    
    def __init__(self):
        self._message_queue: Dict[str, List[AgentMessage]] = {}
        self._subscribers: Dict[str, List[str]] = {}
    
    async def send_message(self, message: AgentMessage) -> None:
        """Send message to target agent."""
        if message.to_agent not in self._message_queue:
            self._message_queue[message.to_agent] = []
        
        self._message_queue[message.to_agent].append(message)
    
    async def receive_messages(self, agent_id: str) -> List[AgentMessage]:
        """Receive messages for agent."""
        messages = self._message_queue.get(agent_id, [])
        self._message_queue[agent_id] = []
        return messages
    
    async def handoff_to_next_phase(self, from_agent: str, to_agent: str, 
                                   work_product: Dict[str, Any]) -> None:
        """Hand off work to next phase agent."""
        message = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=MessageType.HANDOFF,
            payload={"work_product": work_product, "phase_transition": True},
            correlation_id=f"handoff_{from_agent}_{to_agent}",
            timestamp=""
        )
        await self.send_message(message)