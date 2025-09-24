"""Extended capability interfaces for PATH Framework agents."""

from abc import abstractmethod
from typing import Dict, Any, List
from .capability_interface import AgentCapabilityInterface


class NetworkOperationsInterface(AgentCapabilityInterface):
    """Network and API operations capability."""
    
    def get_capability_name(self) -> str:
        return "network_operations"
    
    def get_supported_methods(self) -> List[str]:
        return ["http_request", "websocket_connect", "api_call", "webhook_trigger"]


class DatabaseOperationsInterface(AgentCapabilityInterface):
    """Database operations capability."""
    
    def get_capability_name(self) -> str:
        return "database_operations"
    
    def get_supported_methods(self) -> List[str]:
        return ["connect", "query", "migrate", "backup", "schema_validate"]


class VersionControlInterface(AgentCapabilityInterface):
    """Version control operations capability."""
    
    def get_capability_name(self) -> str:
        return "version_control"
    
    def get_supported_methods(self) -> List[str]:
        return ["git_commit", "git_branch", "git_merge", "git_tag", "create_pr"]