"""
PATH Framework Agents Module.

This module contains all the specialized AI agents for the PATH Framework.
"""

from .base import BaseAgent
from .registry import AgentRegistry

# Import agents as they are implemented
try:
    from .software_engineering.domain_analyst import DomainAnalyst
    AVAILABLE_AGENTS = [DomainAnalyst]
except ImportError:
    AVAILABLE_AGENTS = []

__all__ = [
    "BaseAgent",
    "AgentRegistry", 
    "AVAILABLE_AGENTS",
]
