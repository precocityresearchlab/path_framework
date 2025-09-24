"""
Sample Data for PATH Framework BaseAgent Examples

Contains realistic sample data for demonstrating BaseAgent capabilities
following PATH Framework rule compliance requirements.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone


class SampleDataProvider:
    """Provides sample data for PATH Framework examples."""
    
    @staticmethod
    def get_user_stories() -> Dict[str, Dict[str, Any]]:
        """Sample user stories following PATH Framework format."""
        return {
            "file_management": {
                "format": "As a developer, I want to manage configuration files, so that I can store and retrieve application settings efficiently",
                "acceptance_criteria": [
                    "Given a configuration object, When I save it to file, Then it should be stored in valid JSON format",
                    "Given a file path, When I read the configuration, Then it should return the parsed object",
                    "Given invalid file path, When I try to read, Then it should handle the error gracefully"
                ],
                "business_value": "Reduces configuration management time by 40%"
            },
            
            "code_generation": {
                "format": "As a developer, I want to generate data model classes, so that I can maintain consistent data structures across the application",
                "acceptance_criteria": [
                    "Given field specifications, When I generate a class, Then it should include proper type hints",
                    "Given validation rules, When I create the model, Then it should include validation methods",
                    "Given inheritance requirements, When I generate the class, Then it should extend the correct base class"
                ],
                "business_value": "Reduces boilerplate code writing by 60%"
            },
            
            "data_analysis": {
                "format": "As a data analyst, I want to analyze code quality metrics, so that I can identify areas for improvement",
                "acceptance_criteria": [
                    "Given source code, When I run analysis, Then it should return complexity metrics",
                    "Given code with issues, When I analyze it, Then it should identify specific problems",
                    "Given multiple files, When I analyze them, Then it should provide aggregated metrics"
                ],
                "business_value": "Improves code quality by identifying 80% of potential issues"
            }
        }
    
    @staticmethod
    def get_configuration_data() -> Dict[str, Any]:
        """Sample application configuration data."""
        return {
            "application": {
                "name": "PATH Framework Demo",
                "version": "1.0.0",
                "environment": "development",
                "debug": True
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "path_demo_db",
                "username": "path_user",
                "pool_size": 10,
                "timeout": 30
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "cors_enabled": True,
                "rate_limit": {
                    "requests_per_minute": 100,
                    "burst_size": 20
                }
            },
            "features": {
                "logging": {
                    "enabled": True,
                    "level": "INFO",
                    "format": "json"
                },
                "monitoring": {
                    "enabled": True,
                    "metrics_port": 9090
                },
                "caching": {
                    "enabled": False,
                    "ttl_seconds": 3600
                }
            },
            "security": {
                "jwt_secret": "<JWT_SECRET>",
                "token_expiry_hours": 24,
                "password_min_length": 8
            }
        }
    
    @staticmethod
    def get_model_specifications() -> List[Dict[str, Any]]:
        """Sample data model specifications for code generation."""
        return [
            {
                "class_name": "User",
                "description": "User account model with validation",
                "fields": [
                    {
                        "name": "id",
                        "type": "int",
                        "required": True,
                        "description": "Unique user identifier"
                    },
                    {
                        "name": "username",
                        "type": "str",
                        "required": True,
                        "min_length": 3,
                        "max_length": 50,
                        "pattern": r"^[a-zA-Z0-9_]+$",
                        "description": "Unique username"
                    },
                    {
                        "name": "email",
                        "type": "str",
                        "required": True,
                        "pattern": r"^[^@]+@[^@]+\.[^@]+$",
                        "description": "User email address"
                    },
                    {
                        "name": "age",
                        "type": "int",
                        "required": False,
                        "min_value": 0,
                        "max_value": 150,
                        "description": "User age in years"
                    },
                    {
                        "name": "is_active",
                        "type": "bool",
                        "default": True,
                        "description": "Account active status"
                    },
                    {
                        "name": "created_at",
                        "type": "datetime",
                        "default": "now",
                        "description": "Account creation timestamp"
                    }
                ],
                "methods": ["validate", "to_dict", "from_dict", "__str__", "__repr__"],
                "base_class": "BaseModel"
            },
            
            {
                "class_name": "Product",
                "description": "Product catalog model",
                "fields": [
                    {
                        "name": "id",
                        "type": "str",
                        "required": True,
                        "pattern": r"^PROD-\d{6}$",
                        "description": "Product SKU"
                    },
                    {
                        "name": "name",
                        "type": "str",
                        "required": True,
                        "min_length": 1,
                        "max_length": 200,
                        "description": "Product name"
                    },
                    {
                        "name": "price",
                        "type": "float",
                        "required": True,
                        "min_value": 0.01,
                        "description": "Product price in USD"
                    },
                    {
                        "name": "category",
                        "type": "str",
                        "required": True,
                        "enum": ["electronics", "clothing", "books", "home", "sports"],
                        "description": "Product category"
                    },
                    {
                        "name": "in_stock",
                        "type": "bool",
                        "default": True,
                        "description": "Stock availability"
                    },
                    {
                        "name": "tags",
                        "type": "List[str]",
                        "default": [],
                        "description": "Product tags for search"
                    }
                ],
                "methods": ["validate", "calculate_discount", "update_stock", "__str__"],
                "base_class": None
            }
        ]
    
    @staticmethod
    def get_sample_code() -> Dict[str, str]:
        """Sample code for analysis and testing."""
        return {
            "simple_function": '''
def calculate_total(items):
    """Calculate total price of items."""
    total = 0
    for item in items:
        total += item.get("price", 0)
    return total
''',
            
            "complex_class": '''
class UserManager:
    """Manages user operations with validation."""
    
    def __init__(self, database):
        self.db = database
        self.cache = {}
    
    def create_user(self, username, email, age=None):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150")
        
        user_data = {
            "username": username,
            "email": email,
            "age": age,
            "created_at": datetime.now()
        }
        
        user_id = self.db.insert("users", user_data)
        self.cache[user_id] = user_data
        return user_id
    
    def _validate_email(self, email):
        import re
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return re.match(pattern, email) is not None
    
    def get_user(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        
        user = self.db.get("users", user_id)
        if user:
            self.cache[user_id] = user
        return user
''',
            
            "algorithm_example": '''
def fibonacci_sequence(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[i-1] + sequence[i-2]
        sequence.append(next_num)
    
    return sequence

def binary_search(arr, target):
    """Binary search implementation."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
'''
        }
    
    @staticmethod
    def get_test_data() -> Dict[str, List[Dict[str, Any]]]:
        """Sample test data for various scenarios."""
        return {
            "users": [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john@example.com",
                    "age": 28,
                    "is_active": True,
                    "is_premium": False
                },
                {
                    "id": 2,
                    "username": "jane_smith",
                    "email": "jane@example.com",
                    "age": 34,
                    "is_active": True,
                    "is_premium": True
                },
                {
                    "id": 3,
                    "username": "bob_wilson",
                    "email": "bob@example.com",
                    "age": 17,
                    "is_active": False,
                    "is_premium": False
                }
            ],
            
            "products": [
                {
                    "id": "PROD-001234",
                    "name": "Wireless Headphones",
                    "price": 99.99,
                    "category": "electronics",
                    "in_stock": True,
                    "tags": ["audio", "wireless", "bluetooth"]
                },
                {
                    "id": "PROD-001235",
                    "name": "Programming Book",
                    "price": 49.99,
                    "category": "books",
                    "in_stock": True,
                    "tags": ["programming", "python", "education"]
                },
                {
                    "id": "PROD-001236",
                    "name": "Running Shoes",
                    "price": 129.99,
                    "category": "sports",
                    "in_stock": False,
                    "tags": ["running", "fitness", "shoes"]
                }
            ],
            
            "orders": [
                {
                    "id": "ORD-2024-001",
                    "user_id": 1,
                    "items": [
                        {"product_id": "PROD-001234", "quantity": 1, "price": 99.99}
                    ],
                    "total": 99.99,
                    "status": "completed",
                    "created_at": "2024-01-15T10:30:00Z"
                },
                {
                    "id": "ORD-2024-002",
                    "user_id": 2,
                    "items": [
                        {"product_id": "PROD-001235", "quantity": 2, "price": 49.99},
                        {"product_id": "PROD-001236", "quantity": 1, "price": 129.99}
                    ],
                    "total": 229.97,
                    "status": "pending",
                    "created_at": "2024-01-16T14:45:00Z"
                }
            ]
        }
    
    @staticmethod
    def get_command_examples() -> List[Dict[str, Any]]:
        """Sample command execution examples."""
        return [
            {
                "name": "System Info",
                "command": "uname",
                "args": ["-a"],
                "description": "Get system information"
            },
            {
                "name": "Current Directory",
                "command": "pwd",
                "args": [],
                "description": "Show current working directory"
            },
            {
                "name": "List Files",
                "command": "ls",
                "args": ["-la", "/tmp"],
                "description": "List files in /tmp directory"
            },
            {
                "name": "Python Version",
                "command": "python3",
                "args": ["--version"],
                "description": "Check Python version"
            },
            {
                "name": "Disk Usage",
                "command": "df",
                "args": ["-h"],
                "description": "Show disk usage in human readable format"
            }
        ]