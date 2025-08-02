"""
PATH Framework Phases Module.

This module contains the four main development phases:
- Software Engineering Phase
- TDD Phase  
- DevOps Phase
- Operations Phase
"""

from .base import BasePhase

# Import phases as they are implemented
__all__ = [
    "BasePhase",
]

# Phase implementations will be added as they are created
try:
    from .software_engineering import SoftwareEngineeringPhase
    __all__.append("SoftwareEngineeringPhase")
except ImportError:
    pass

try:
    from .tdd import TDDPhase
    __all__.append("TDDPhase")
except ImportError:
    pass

try:
    from .devops import DevOpsPhase
    __all__.append("DevOpsPhase")
except ImportError:
    pass

try:
    from .operations import OperationsPhase
    __all__.append("OperationsPhase")
except ImportError:
    pass
