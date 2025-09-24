"""System adapter for PATH Framework agents."""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List


class SystemAdapter:
    """Adapter for system operations."""
    
    def __init__(self):
        self.temp_dir = Path("/tmp")
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return True
        except Exception:
            return False
    
    def read_file(self, file_path: str) -> str:
        """Read content from file."""
        try:
            return Path(file_path).read_text()
        except Exception:
            return ""
    
    def execute_command(self, command: str, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        """Execute system command."""
        try:
            result = subprocess.run(
                [command] + args,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "success": False
            }