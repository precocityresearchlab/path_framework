"""Communication protocols for agent interactions."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import asyncio
import json
import logging


@dataclass
class Message:
    """Standard message format for agent communication."""
    message_id: str
    source_agent: str
    target_agent: str
    message_type: str
    payload: Dict[str, Any]
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None


class CommunicationLayer:
    """Handles inter-agent communication."""
    
    def __init__(self):
        self.logger = logging.getLogger("CommunicationLayer")
        self.message_handlers = {}
        self.subscribers = {}
    
    async def send_message(self, message: Message) -> Dict[str, Any]:
        """Send message to target agent."""
        self.logger.info(f"Sending message from {message.source_agent} to {message.target_agent}")
        
        # In real implementation, this would use gRPC, Kafka, or REST
        # For now, simulate message delivery
        response = {
            "status": "delivered",
            "message_id": message.message_id,
            "timestamp": "2025-09-22T12:00:00Z"
        }
        
        return response
    
    async def broadcast_message(self, message: Message, targets: list) -> Dict[str, Any]:
        """Broadcast message to multiple agents."""
        results = {}
        for target in targets:
            message.target_agent = target
            result = await self.send_message(message)
            results[target] = result
        
        return results
    
    def subscribe(self, agent_id: str, message_type: str, handler):
        """Subscribe to specific message types."""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        
        self.subscribers[message_type].append({
            "agent_id": agent_id,
            "handler": handler
        })
    
    async def publish_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish event to subscribers."""
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                try:
                    await subscriber["handler"](payload)
                except Exception as e:
                    self.logger.error(f"Error handling event {event_type}: {e}")
    
    def register_handler(self, message_type: str, handler):
        """Register message handler."""
        self.message_handlers[message_type] = handler
    
    async def handle_message(self, message: Message) -> Dict[str, Any]:
        """Handle incoming message."""
        if message.message_type in self.message_handlers:
            handler = self.message_handlers[message.message_type]
            return await handler(message)
        else:
            self.logger.warning(f"No handler for message type: {message.message_type}")
            return {"status": "no_handler", "message_type": message.message_type}