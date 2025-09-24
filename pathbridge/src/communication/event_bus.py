"""Event-driven communication between agents."""

from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from enum import Enum
import asyncio


class EventType(Enum):
    WORK_COMPLETED = "work_completed"
    QUALITY_GATE_PASSED = "quality_gate_passed"
    PHASE_TRANSITION = "phase_transition"
    ERROR_OCCURRED = "error_occurred"


@dataclass
class AgentEvent:
    """Event published by agents."""
    event_type: EventType
    source_agent: str
    data: Dict[str, Any]
    timestamp: str


class EventBus:
    """Publish-subscribe event system for agents."""
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """Subscribe to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    async def publish(self, event: AgentEvent) -> None:
        """Publish event to subscribers."""
        handlers = self._subscribers.get(event.event_type, [])
        
        # Execute all handlers concurrently
        tasks = [handler(event) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks)
    
    async def publish_work_completed(self, agent_id: str, work_product: Dict[str, Any]) -> None:
        """Publish work completion event."""
        event = AgentEvent(
            event_type=EventType.WORK_COMPLETED,
            source_agent=agent_id,
            data={"work_product": work_product},
            timestamp=""
        )
        await self.publish(event)