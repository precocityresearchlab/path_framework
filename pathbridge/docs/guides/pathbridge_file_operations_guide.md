# PathBridge File Operations Integration Guide

## Overview

PathBridge file operations system provides intelligent file system management for AI coding assistants, supporting safe file operations, content analysis, and automated code generation.

**Core Capabilities:**
- **File System Operations**: Read, write, create, delete files and directories
- **Content Search**: Intelligent file and content search with fuzzy matching
- **Command Execution**: Safe system command execution with output capture
- **Content Replacement**: Advanced find and replace operations
- **Backup Management**: Automatic backups before destructive operations

## Quick Start

### 1. Basic File Operations

```python
from pathbridge.file_ops.file_manager import FileSystemManager

async def basic_file_operations():
    fs_manager = FileSystemManager()
    
    # Write file with content
    await fs_manager.write_file(
        path="src/user_service.py",
        content="""
class UserService:
    def __init__(self):
        self.users = {}
    
    def create_user(self, username: str, email: str) -> dict:
        user = {"username": username, "email": email}
        self.users[username] = user
        return user
""",
        create_directories=True
    )
    
    # Read file content
    content = await fs_manager.read_file("src/user_service.py")
    print(f"File content: {content[:100]}...")
    
    # Check if file exists
    exists = await fs_manager.file_exists("src/user_service.py")
    print(f"File exists: {exists}")
```

### 2. Integration with PATH Agents

```python
from pathbridge.agents.base_agent import CoreAgent
from pathbridge.file_ops.file_manager import FileSystemManager

class FileOperationAgent(CoreAgent):
    def __init__(self):
        super().__init__("file_ops_agent", phase=2, ["write_code", "analyze_files"])
        self.fs_manager = FileSystemManager()
    
    async def execute_capability(self, request: CapabilityRequest) -> CapabilityResponse:
        if request.capability_name == "write_code":
            return await self._write_generated_code(request.parameters)
        elif request.capability_name == "analyze_files":
            return await self._analyze_project_files(request.parameters)
    
    async def _write_generated_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Generate code using LLM
        generated_code = await self.llm_client.generate_code(
            prompt=params["requirements"],
            language=params["language"]
        )
        
        # Write to file system
        file_path = params["output_path"]
        await self.fs_manager.write_file(
            path=file_path,
            content=generated_code,
            backup=True  # Create backup before writing
        )
        
        return {
            "file_path": file_path,
            "lines_written": len(generated_code.split('\n')),
            "backup_created": True
        }
```

## File System Operations

### Advanced File Writing

```python
from pathbridge.file_ops.file_writer import FileWriter

async def advanced_file_writing():
    writer = FileWriter()
    
    # Write with template
    await writer.write_with_template(
        template_path="templates/fastapi_controller.py.j2",
        output_path="src/controllers/user_controller.py",
        context={
            "model_name": "User",
            "endpoints": ["create", "read", "update", "delete"],
            "authentication": True
        }
    )
    
    # Append content to existing file
    await writer.append_content(
        path="src/main.py",
        content="\n# Auto-generated route imports\nfrom controllers.user_controller import router as user_router\napp.include_router(user_router)\n"
    )
    
    # Write with metadata
    await writer.create_with_metadata(
        path="src/models/user.py",
        content="class User(BaseModel): pass",
        metadata={
            "generated_by": "pathbridge",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": "domain_analyst"
        }
    )
```

### File Search Operations

```python
from pathbridge.file_ops.search_engine import FileSearchEngine

async def intelligent_file_search():
    search_engine = FileSearchEngine()
    
    # Search by filename
    python_files = await search_engine.search_by_name(
        directory="src/",
        pattern="*.py",
        recursive=True
    )
    
    # Fuzzy search for files
    similar_files = await search_engine.fuzzy_search(
        directory="src/",
        query="user_service",
        threshold=0.7
    )
    
    # Search file contents
    content_matches = await search_engine.search_by_content(
        directory="src/",
        query="class.*Service",
        regex=True,
        include_line_numbers=True
    )
    
    # Advanced search with filters
    filtered_results = await search_engine.advanced_search(
        directory="src/",
        filename_pattern="*.py",
        content_pattern="async def",
        file_size_range=(1000, 50000),  # bytes
        modified_after=datetime.now() - timedelta(days=7)
    )
    
    return {
        "python_files": len(python_files),
        "similar_files": similar_files,
        "content_matches": content_matches,
        "filtered_results": filtered_results
    }
```

### Content Replacement Operations

```python
from pathbridge.file_ops.content_replacer import ContentReplacer

async def content_replacement():
    replacer = ContentReplacer()
    
    # Simple find and replace
    await replacer.replace_in_file(
        file_path="src/user_service.py",
        old_text="def create_user(self, username, email):",
        new_text="def create_user(self, username: str, email: str) -> User:",
        backup=True
    )
    
    # Regex replacement
    await replacer.regex_replace(
        file_path="src/user_service.py",
        pattern=r"def (\w+)\(self, ([^)]+)\):",
        replacement=r"async def \1(self, \2) -> dict:",
        backup=True
    )
    
    # Bulk replacement across multiple files
    replacement_results = await replacer.bulk_replace(
        directory="src/",
        file_pattern="*.py",
        replacements=[
            {"old": "print(", "new": "logger.info("},
            {"old": "import os", "new": "import os\nimport logging"}
        ],
        backup=True
    )
    
    return replacement_results
```

## Command Execution

### Safe Command Execution

```python
from pathbridge.file_ops.command_executor import CommandExecutor

async def safe_command_execution():
    executor = CommandExecutor()
    
    # Execute with output capture
    result = await executor.execute_bash(
        command="python -m pytest tests/ -v",
        cwd="/path/to/project",
        timeout=300,
        capture_output=True
    )
    
    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    # Execute with validation
    git_result = await executor.run_command(
        command=["git", "status", "--porcelain"],
        validate_command=True,  # Check if git is available
        allowed_commands=["git", "python", "npm"]  # Whitelist
    )
    
    return {
        "test_result": result,
        "git_status": git_result
    }
```

### Command Validation and Security

```python
class SecureCommandExecutor(CommandExecutor):
    ALLOWED_COMMANDS = {
        "git": ["status", "add", "commit", "push", "pull"],
        "python": ["-m", "-c"],
        "npm": ["install", "test", "build"],
        "docker": ["build", "run", "ps"]
    }
    
    async def validate_command(self, command: List[str]) -> bool:
        """Validate command against whitelist"""
        if not command:
            return False
        
        base_command = command[0]
        if base_command not in self.ALLOWED_COMMANDS:
            return False
        
        # Additional validation for command arguments
        allowed_args = self.ALLOWED_COMMANDS[base_command]
        if len(command) > 1 and command[1] not in allowed_args:
            return False
        
        return True
    
    async def execute_validated_command(self, command: List[str]) -> CommandResult:
        if not await self.validate_command(command):
            raise SecurityError(f"Command not allowed: {' '.join(command)}")
        
        return await self.run_command(command)
```

## Directory Management

### Directory Operations

```python
from pathbridge.file_ops.directory_manager import DirectoryManager

async def directory_operations():
    dir_manager = DirectoryManager()
    
    # Create directory structure
    await dir_manager.create_tree(
        base_path="new_project/",
        structure={
            "src": {
                "controllers": {},
                "models": {},
                "services": {},
                "utils": {}
            },
            "tests": {
                "unit": {},
                "integration": {}
            },
            "docs": {},
            "config": {}
        }
    )
    
    # List directory contents
    contents = await dir_manager.list_directory(
        path="src/",
        recursive=True,
        include_hidden=False,
        file_types=[".py", ".js", ".ts"]
    )
    
    # Filter files by criteria
    filtered_files = await dir_manager.filter_files(
        directory="src/",
        criteria={
            "min_size": 100,  # bytes
            "max_size": 10000,
            "extensions": [".py"],
            "modified_after": datetime.now() - timedelta(days=1)
        }
    )
    
    return {
        "directory_created": True,
        "total_files": len(contents),
        "filtered_files": len(filtered_files)
    }
```

### Project Structure Analysis

```python
async def analyze_project_structure():
    dir_manager = DirectoryManager()
    
    # Analyze project structure
    analysis = await dir_manager.analyze_project_structure("./")
    
    structure_report = {
        "total_files": analysis.total_files,
        "file_types": analysis.file_type_distribution,
        "directory_depth": analysis.max_depth,
        "largest_files": analysis.largest_files[:5],
        "code_files": analysis.code_files,
        "test_files": analysis.test_files,
        "config_files": analysis.config_files
    }
    
    return structure_report
```

## Backup and Version Management

### Automatic Backup System

```python
from pathbridge.file_ops.backup_manager import FileBackupManager

async def backup_operations():
    backup_manager = FileBackupManager()
    
    # Create backup before modification
    backup_path = await backup_manager.create_backup(
        file_path="src/important_service.py",
        backup_dir=".pathbridge/backups/"
    )
    
    # Restore from backup
    await backup_manager.restore_backup(
        backup_path=backup_path,
        restore_path="src/important_service.py"
    )
    
    # Manage backup versions
    await backup_manager.manage_versions(
        file_path="src/important_service.py",
        max_versions=5,  # Keep only 5 most recent backups
        cleanup_older_than=timedelta(days=30)
    )
    
    # List available backups
    backups = await backup_manager.list_backups("src/important_service.py")
    
    return {
        "backup_created": backup_path,
        "available_backups": len(backups)
    }
```

## Integration with AI Agents

### Code Generation with File Operations

```python
class CodeGenerationAgent(CoreAgent):
    def __init__(self):
        super().__init__("code_gen_agent", phase=2, ["generate_implementation"])
        self.fs_manager = FileSystemManager()
        self.search_engine = FileSearchEngine()
    
    async def generate_implementation(self, user_story: Dict[str, Any]) -> Dict[str, Any]:
        # Analyze existing codebase
        existing_files = await self.search_engine.search_by_content(
            directory="src/",
            query=user_story["domain_entities"],
            regex=False
        )
        
        # Generate new implementation
        implementation = await self.llm_client.generate_code(
            prompt=f"Implement {user_story['title']}",
            context={"existing_files": existing_files},
            language="python"
        )
        
        # Write implementation to file system
        output_path = f"src/{user_story['title'].lower().replace(' ', '_')}.py"
        await self.fs_manager.write_file(
            path=output_path,
            content=implementation,
            backup=True
        )
        
        # Generate corresponding tests
        test_content = await self.llm_client.generate_tests(
            source_code=implementation,
            test_framework="pytest"
        )
        
        test_path = f"tests/test_{user_story['title'].lower().replace(' ', '_')}.py"
        await self.fs_manager.write_file(
            path=test_path,
            content=test_content
        )
        
        return {
            "implementation_file": output_path,
            "test_file": test_path,
            "lines_of_code": len(implementation.split('\n')),
            "backup_created": True
        }
```

## Error Handling and Recovery

```python
from pathbridge.exceptions import FileOperationError, PermissionError

async def robust_file_operations():
    try:
        fs_manager = FileSystemManager()
        
        # Attempt file operation with error handling
        await fs_manager.write_file(
            path="protected/file.py",
            content="# Generated code",
            create_directories=True
        )
        
    except PermissionError as e:
        print(f"Permission denied: {e}")
        # Try alternative location or request elevated permissions
        
    except FileOperationError as e:
        print(f"File operation failed: {e}")
        # Implement retry logic or fallback strategy
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Log error and continue with degraded functionality
```

## Configuration

### File Operations Settings

```bash
# File System Settings
PATH_FILE_BACKUP_ENABLED=true
PATH_FILE_BACKUP_DIR=.pathbridge/backups
PATH_FILE_MAX_SIZE=10MB
PATH_FILE_ALLOWED_EXTENSIONS=.py,.js,.ts,.java,.go,.rs

# Command Execution Settings
PATH_COMMAND_TIMEOUT=300
PATH_COMMAND_WHITELIST=git,python,npm,docker
PATH_COMMAND_VALIDATION=strict

# Search Settings
PATH_SEARCH_MAX_RESULTS=100
PATH_SEARCH_FUZZY_THRESHOLD=0.7
PATH_SEARCH_INCLUDE_BINARY=false
```

## Testing File Operations

```python
import pytest
import tempfile
from pathbridge.file_ops.file_manager import FileSystemManager

@pytest.mark.asyncio
async def test_file_operations():
    """Test basic file operations"""
    with tempfile.TemporaryDirectory() as temp_dir:
        fs_manager = FileSystemManager()
        
        test_file = f"{temp_dir}/test.py"
        test_content = "print('Hello, World!')"
        
        # Test write
        await fs_manager.write_file(test_file, test_content)
        
        # Test read
        content = await fs_manager.read_file(test_file)
        assert content == test_content
        
        # Test exists
        exists = await fs_manager.file_exists(test_file)
        assert exists is True
        
        # Test delete
        await fs_manager.delete_file(test_file)
        exists = await fs_manager.file_exists(test_file)
        assert exists is False
```

## Best Practices

### File Operation Guidelines

1. **Always Create Backups**: Before destructive operations, create backups
2. **Validate Paths**: Ensure file paths are within allowed directories
3. **Handle Permissions**: Check and handle file permission errors gracefully
4. **Atomic Operations**: Use atomic file operations to prevent corruption
5. **Resource Cleanup**: Always close file handles and clean up resources
6. **Security Validation**: Validate all file paths and command inputs

### Performance Optimization

```python
# Batch file operations for better performance
async def batch_file_operations():
    fs_manager = FileSystemManager()
    
    # Process multiple files concurrently
    files_to_process = ["file1.py", "file2.py", "file3.py"]
    
    tasks = [
        fs_manager.process_file(file_path)
        for file_path in files_to_process
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle results and exceptions
    successful = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    return {
        "successful": len(successful),
        "failed": len(failed)
    }
```