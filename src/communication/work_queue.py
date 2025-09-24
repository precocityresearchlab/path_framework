"""Work queue system for agent coordination."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from collections import deque


class WorkStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkItem:
    """Work item in the queue."""
    id: str
    assigned_agent: str
    work_type: str
    input_data: Dict[str, Any]
    status: WorkStatus
    result: Optional[Dict[str, Any]] = None
    dependencies: List[str] = None


class WorkQueue:
    """Manages work distribution between agents."""
    
    def __init__(self):
        self._work_items: Dict[str, WorkItem] = {}
        self._agent_queues: Dict[str, deque] = {}
    
    async def add_work(self, work_item: WorkItem) -> None:
        """Add work item to queue."""
        self._work_items[work_item.id] = work_item
        
        if work_item.assigned_agent not in self._agent_queues:
            self._agent_queues[work_item.assigned_agent] = deque()
        
        self._agent_queues[work_item.assigned_agent].append(work_item.id)
    
    async def get_next_work(self, agent_id: str) -> Optional[WorkItem]:
        """Get next work item for agent."""
        if agent_id not in self._agent_queues:
            return None
        
        queue = self._agent_queues[agent_id]
        if not queue:
            return None
        
        work_id = queue.popleft()
        work_item = self._work_items[work_id]
        work_item.status = WorkStatus.IN_PROGRESS
        return work_item
    
    async def complete_work(self, work_id: str, result: Dict[str, Any]) -> None:
        """Mark work as completed."""
        if work_id in self._work_items:
            self._work_items[work_id].status = WorkStatus.COMPLETED
            self._work_items[work_id].result = result
    
    async def create_phase_workflow(self, user_story: Dict[str, Any]) -> List[str]:
        """Create workflow across all phases."""
        workflow_id = f"workflow_{user_story['story_id']}"
        
        # Phase 1: Domain Analysis → System Architecture → Component Design → Integration
        phase1_work = [
            WorkItem(f"{workflow_id}_domain", "domain_analyst", "analyze_user_story", user_story, WorkStatus.PENDING),
            WorkItem(f"{workflow_id}_system", "system_architect", "design_architecture", {}, WorkStatus.PENDING, dependencies=[f"{workflow_id}_domain"]),
            WorkItem(f"{workflow_id}_component", "component_designer", "design_components", {}, WorkStatus.PENDING, dependencies=[f"{workflow_id}_system"]),
            WorkItem(f"{workflow_id}_integration", "integration_architect", "design_integrations", {}, WorkStatus.PENDING, dependencies=[f"{workflow_id}_component"])
        ]
        
        for work in phase1_work:
            await self.add_work(work)
        
        return [work.id for work in phase1_work]