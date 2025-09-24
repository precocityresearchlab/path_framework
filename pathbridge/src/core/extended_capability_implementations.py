"""Extended capability implementations."""

import httpx
import subprocess
from typing import Dict, Any
from .extended_capabilities import NetworkOperationsInterface, VersionControlInterface


class StandardNetworkOperations(NetworkOperationsInterface):
    """Standard network operations implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        required_params = {
            "http_request": ["url"],
            "api_call": ["endpoint"],
            "webhook_trigger": ["url", "payload"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if method == "http_request":
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=params.get("method", "GET"),
                    url=params["url"],
                    json=params.get("data"),
                    headers=params.get("headers", {})
                )
                return {
                    "status_code": response.status_code,
                    "content": response.text,
                    "headers": dict(response.headers)
                }
                
        elif method == "api_call":
            async with httpx.AsyncClient() as client:
                response = await client.get(params["endpoint"])
                return {"data": response.json()}
                
        else:
            raise ValueError(f"Method {method} not implemented")


class StandardVersionControl(VersionControlInterface):
    """Standard version control implementation."""
    
    def __init__(self, system_adapter):
        self.system = system_adapter
        
    def validate_params(self, method: str, params: Dict[str, Any]) -> bool:
        required_params = {
            "git_commit": ["message"],
            "git_branch": ["branch_name"],
            "git_tag": ["tag_name"]
        }
        
        if method not in required_params:
            return False
            
        return all(param in params for param in required_params[method])
        
    async def execute_capability(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if method == "git_commit":
            result = subprocess.run(
                ["git", "commit", "-m", params["message"]],
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
            
        elif method == "git_branch":
            result = subprocess.run(
                ["git", "checkout", "-b", params["branch_name"]],
                capture_output=True,
                text=True
            )
            return {
                "success": result.returncode == 0,
                "branch": params["branch_name"]
            }
            
        else:
            raise ValueError(f"Method {method} not implemented")