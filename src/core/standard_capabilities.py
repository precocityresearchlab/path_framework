"""Standard capability implementations for PATH Framework agents."""

import os
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, Any, List

from .capability_interface import (
    FileOperationsInterface,
    CommandExecutionInterface, 
    CodeGenerationInterface,
    AnalysisToolsInterface
)


class StandardFileOperations(FileOperationsInterface):
    """Standard file operations implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        """Validate parameters for file operations."""
        required_params = {
            "read": ["path"],
            "write": ["path", "content"],
            "create_directory": ["path"],
            "delete": ["path"],
            "list": ["path"],
            "move": ["source", "destination"],
            "copy": ["source", "destination"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operation."""
        if method == "read":
            content = Path(params["path"]).read_text()
            return {"content": content}
            
        elif method == "write":
            Path(params["path"]).write_text(params["content"])
            return {"success": True}
            
        elif method == "create_directory":
            Path(params["path"]).mkdir(parents=True, exist_ok=True)
            return {"success": True}
            
        elif method == "delete":
            path = Path(params["path"])
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
            return {"success": True}
            
        elif method == "list":
            items = [str(p) for p in Path(params["path"]).iterdir()]
            return {"items": items}
            
        elif method == "move":
            Path(params["source"]).rename(params["destination"])
            return {"success": True}
            
        elif method == "copy":
            import shutil
            shutil.copy2(params["source"], params["destination"])
            return {"success": True}
            
        else:
            raise ValueError(f"Unsupported method: {method}")


class StandardCommandExecution(CommandExecutionInterface):
    """Standard command execution implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        """Validate parameters for command execution."""
        required_params = {
            "execute": ["command"],
            "execute_async": ["command"],
            "stream_output": ["command"],
            "terminate": ["process_id"],
            "get_exit_code": ["process_id"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command operation."""
        if method == "execute":
            result = subprocess.run(
                params["command"],
                shell=True,
                capture_output=True,
                text=True,
                cwd=params.get("cwd")
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
            
        elif method == "execute_async":
            process = await asyncio.create_subprocess_shell(
                params["command"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=params.get("cwd")
            )
            stdout, stderr = await process.communicate()
            return {
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "exit_code": process.returncode
            }
            
        else:
            raise ValueError(f"Method {method} not implemented yet")


class StandardCodeGeneration(CodeGenerationInterface):
    """Standard code generation implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        """Validate parameters for code generation."""
        required_params = {
            "generate_source": ["language", "content", "path"],
            "generate_config": ["format", "content", "path"],
            "generate_docs": ["format", "content", "path"],
            "apply_templates": ["template", "variables", "output_path"],
            "format_code": ["language", "code"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code generation operation."""
        if method == "generate_source":
            Path(params["path"]).write_text(params["content"])
            return {"success": True, "path": params["path"]}
            
        elif method == "generate_config":
            Path(params["path"]).write_text(params["content"])
            return {"success": True, "path": params["path"]}
            
        elif method == "generate_docs":
            Path(params["path"]).write_text(params["content"])
            return {"success": True, "path": params["path"]}
            
        elif method == "format_code":
            # Basic formatting - could integrate with language-specific formatters
            return {"formatted_code": params["code"]}
            
        else:
            raise ValueError(f"Method {method} not implemented yet")


class StandardAnalysisTools(AnalysisToolsInterface):
    """Standard analysis tools implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        """Validate parameters for analysis tools."""
        required_params = {
            "static_analysis": ["path", "language"],
            "parse_codebase": ["path"],
            "validate_config": ["path", "schema"],
            "assess_metrics": ["path"],
            "dependency_analysis": ["path"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis operation."""
        if method == "static_analysis":
            # Basic static analysis - could integrate with language-specific tools
            return {"issues": [], "metrics": {"lines": 0, "complexity": 0}}
            
        elif method == "parse_codebase":
            # Basic codebase parsing
            files = list(Path(params["path"]).rglob("*.py"))  # Example for Python
            return {"files": [str(f) for f in files], "count": len(files)}
            
        elif method == "assess_metrics":
            # Basic metrics assessment
            return {"metrics": {"files": 0, "lines": 0, "functions": 0}}
            
        else:
            raise ValueError(f"Method {method} not implemented yet")