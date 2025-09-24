"""
PATH Framework Phases Module.

This module contains the four main development phases:
- Software Engineering Phase
- TDD Phase
- DevOps Phase
- Operations Phase
"""

import contextlib

from .base import BasePhase

# Import phases as they are implemented
__all__ = [
    "BasePhase",
]

# Phase implementations will be added as they are created
with contextlib.suppress(ImportError):
    __all__.append("SoftwareEngineeringPhase")

with contextlib.suppress(ImportError):
    __all__.append("TDDPhase")

with contextlib.suppress(ImportError):
    __all__.append("DevOpsPhase")

with contextlib.suppress(ImportError):
    __all__.append("OperationsPhase")
