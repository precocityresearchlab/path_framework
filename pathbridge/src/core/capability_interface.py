"""Standard capability interfaces for PATH Framework agents."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class CapabilityStatus(Enum):
    """Standard capability execution status."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class CapabilityRequest:
    """Standard capability request format."""
    capability: str
    method: str
    params: Dict[str, Any]
    request_id: str
    timeout: int = 30


@dataclass
class CapabilityResponse:
    """Standard capability response format."""
    request_id: str
    status: CapabilityStatus
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    execution_time: float


class AgentCapabilityInterface(ABC):
    """Standard interface that all agent capabilities must implement."""
    
    @abstractmethod
    def get_capability_name(self) -> str:
        """Return the capability name."""
        pass
    
    @abstractmethod
    def get_supported_methods(self) -> List[str]:
        """Return list of supported methods."""
        pass
    
    @abstractmethod
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a capability method with parameters."""
        pass
    
    @abstractmethod
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        """Validate parameters for a method."""
        pass


class FileOperationsInterface(AgentCapabilityInterface):
    """Standard file operations capability."""
    
    def get_capability_name(self) -> str:
        return "file_operations"
    
    def get_supported_methods(self) -> List[str]:
        return ["read", "write", "create_directory", "delete", "list", "move", "copy"]


class CommandExecutionInterface(AgentCapabilityInterface):
    """Standard command execution capability."""
    
    def get_capability_name(self) -> str:
        return "command_execution"
    
    def get_supported_methods(self) -> List[str]:
        return ["execute", "execute_async", "stream_output", "terminate", "get_exit_code"]


class CodeGenerationInterface(AgentCapabilityInterface):
    """Standard code generation capability."""
    
    def get_capability_name(self) -> str:
        return "code_generation"
    
    def get_supported_methods(self) -> List[str]:
        return ["generate_source", "generate_config", "generate_docs", "apply_templates", "format_code"]


class AnalysisToolsInterface(AgentCapabilityInterface):
    """Standard analysis tools capability."""
    
    def get_capability_name(self) -> str:
        return "analysis_tools"
    
    def get_supported_methods(self) -> List[str]:
        return ["static_analysis", "parse_codebase", "validate_config", "assess_metrics", "dependency_analysis"]