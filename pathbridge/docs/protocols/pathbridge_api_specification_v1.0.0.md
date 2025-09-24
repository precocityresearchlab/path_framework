---
created_date: 2025-01-15
created_by: PATH Framework Research Team
last_modified: 2025-01-15
version: 1.0.0
purpose: Complete API specification for PathBridge component interfaces and integration
framework_phase: N/A
dependencies: [AGENT_DATA_EXCHANGE_PROTOCOLS_v1.0.0, PathBridge AI Coding Assistant]
status: alpha
tags: [API Specification, Component Interfaces, Integration, PathBridge, REST API, WebSocket]
---

# PathBridge API Specification v1.0.0

![Framework](https://img.shields.io/badge/Framework-PathBridge%20API-orange?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Alpha-yellow?style=flat-square)
![Institution](https://img.shields.io/badge/Institution-Precocity%20Research-purple?style=flat-square)
![Type](https://img.shields.io/badge/Type-API%20Specification-red?style=flat-square)

## Table of Contents

- [Authentication](#authentication)
- [Core Agent API](#core-agent-api)
- [Knowledge Base API](#knowledge-base-api)
- [Security Component API](#security-component-api)
- [Testing Component API](#testing-component-api)
- [Code Intelligence API](#code-intelligence-api)
- [Human Validation API](#human-validation-api)
- [File Operations API](#file-operations-api)
- [Integration Services API](#integration-services-api)
- [Monitoring API](#monitoring-api)
- [WebSocket Events](#websocket-events)
- [Error Handling](#error-handling)

## Authentication

**Base URL**: `http://localhost:8080/api/v1`

**Authentication Methods**:
- Bearer Token: `Authorization: Bearer <token>`
- API Key: `X-API-Key: <api_key>`

**Token Endpoint**:
```http
POST /auth/token
Content-Type: application/json

{
  "username": "developer",
  "password": "secure_password"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

## Core Agent API

### Agent Status and Control

```http
GET /agent/status
Authorization: Bearer <token>

Response:
{
  "agent_id": "pathbridge_001",
  "status": "active",
  "current_phase": 2,
  "current_task": {
    "task_id": "task_001",
    "story_id": "story_001",
    "description": "Implementing user authentication",
    "progress": 65,
    "estimated_completion": "2025-01-15T14:30:00Z"
  },
  "capabilities": [
    "architecture_design",
    "test_generation",
    "code_implementation",
    "deployment_automation"
  ],
  "uptime": "72h30m15s"
}
```

```http
POST /agent/task
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_story": {
    "title": "User Authentication",
    "description": "As a user, I want to securely log into the system so that I can access my personal dashboard",
    "user_type": "end_user",
    "functionality": "secure login with email and password",
    "benefit": "access to personalized content and features"
  },
  "acceptance_criteria": [
    {
      "given": "I am on the login page",
      "when": "I enter valid credentials",
      "then": "I should be redirected to my dashboard"
    },
    {
      "given": "I enter invalid credentials",
      "when": "I attempt to login",
      "then": "I should see an error message"
    }
  ],
  "priority": "high",
  "estimated_effort": "medium"
}

Response:
{
  "task_id": "task_001",
  "story_id": "story_001",
  "status": "accepted",
  "phase": 1,
  "estimated_duration": "4h",
  "next_steps": [
    "Architecture design",
    "Component specification",
    "Technology selection"
  ]
}
```

```http
GET /agent/task/{task_id}
Authorization: Bearer <token>

Response:
{
  "task_id": "task_001",
  "story_id": "story_001",
  "status": "in_progress",
  "phase": 2,
  "progress": 65,
  "started_at": "2025-01-15T10:00:00Z",
  "estimated_completion": "2025-01-15T14:30:00Z",
  "completed_steps": [
    "Architecture design completed",
    "Component specifications created",
    "Test strategy defined"
  ],
  "current_step": "Generating unit tests",
  "remaining_steps": [
    "Code implementation",
    "Integration testing",
    "Deployment preparation"
  ]
}
```

## Knowledge Base API

### User Stories Management

```http
GET /knowledge/user-stories
Authorization: Bearer <token>
Query Parameters:
  - status: pending|in_progress|completed
  - limit: integer (default: 20)
  - offset: integer (default: 0)

Response:
{
  "stories": [
    {
      "story_id": "story_001",
      "title": "User Authentication",
      "description": "As a user, I want to securely log in...",
      "status": "in_progress",
      "phase": 2,
      "progress": 65,
      "created_at": "2025-01-15T09:00:00Z",
      "updated_at": "2025-01-15T12:30:00Z"
    }
  ],
  "total": 15,
  "limit": 20,
  "offset": 0
}
```

```http
POST /knowledge/user-stories
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "User Profile Management",
  "description": "As a user, I want to update my profile information",
  "user_type": "registered_user",
  "functionality": "edit profile fields and save changes",
  "benefit": "keep personal information current",
  "acceptance_criteria": [...]
}

Response:
{
  "story_id": "story_002",
  "status": "created",
  "message": "User story created successfully"
}
```

### Code Patterns and Templates

```http
GET /knowledge/patterns
Authorization: Bearer <token>
Query Parameters:
  - language: python|javascript|java|go
  - pattern_type: template|snippet|boilerplate
  - search: string

Response:
{
  "patterns": [
    {
      "pattern_id": "pattern_001",
      "name": "fastapi_crud_endpoint",
      "language": "python",
      "pattern_type": "template",
      "description": "FastAPI CRUD endpoint template",
      "template": "@app.post(\"/users/\")\nasync def create_user(user: UserCreate):\n    # Implementation\n    return user",
      "usage_count": 15,
      "created_at": "2025-01-10T10:00:00Z"
    }
  ]
}
```

```http
POST /knowledge/patterns
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "pytest_fixture_template",
  "language": "python",
  "pattern_type": "template",
  "description": "Standard pytest fixture for database testing",
  "template": "@pytest.fixture\ndef db_session():\n    # Setup\n    yield session\n    # Cleanup"
}

Response:
{
  "pattern_id": "pattern_002",
  "status": "created"
}
```

### Architecture Decisions

```http
GET /knowledge/decisions
Authorization: Bearer <token>
Query Parameters:
  - status: active|deprecated|superseded

Response:
{
  "decisions": [
    {
      "decision_id": "decision_001",
      "title": "Authentication Method Selection",
      "decision": "Use JWT tokens with Redis session store",
      "rationale": "Provides stateless authentication with session management capabilities",
      "alternatives": [
        "Session-based authentication",
        "OAuth 2.0 only"
      ],
      "status": "active",
      "created_at": "2025-01-15T09:30:00Z"
    }
  ]
}
```

## Security Component API

### Security Scanning

```http
POST /security/scan
Authorization: Bearer <token>
Content-Type: application/json

{
  "scan_type": "sast",
  "target": {
    "type": "files",
    "files": ["src/auth.py", "src/user.py"],
    "exclude_patterns": ["*.test.py", "migrations/*"]
  },
  "rules": ["sql_injection", "xss", "secrets", "hardcoded_passwords"],
  "severity_threshold": "medium"
}

Response:
{
  "scan_id": "scan_001",
  "status": "started",
  "estimated_duration": "2m30s",
  "message": "Security scan initiated"
}
```

```http
GET /security/scan/{scan_id}
Authorization: Bearer <token>

Response:
{
  "scan_id": "scan_001",
  "status": "completed",
  "started_at": "2025-01-15T10:00:00Z",
  "completed_at": "2025-01-15T10:02:30Z",
  "summary": {
    "total_files_scanned": 15,
    "total_issues": 3,
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0,
    "info": 0
  },
  "vulnerabilities": [
    {
      "id": "vuln_001",
      "type": "sql_injection",
      "severity": "high",
      "file": "src/auth.py",
      "line": 45,
      "column": 20,
      "description": "Potential SQL injection vulnerability in user authentication",
      "code_snippet": "query = f\"SELECT * FROM users WHERE email = '{email}'\"",
      "recommendation": "Use parameterized queries to prevent SQL injection",
      "cwe_id": "CWE-89"
    }
  ]
}
```

### Secrets Detection

```http
POST /security/secrets/scan
Authorization: Bearer <token>
Content-Type: application/json

{
  "target": {
    "type": "directory",
    "path": "src/",
    "recursive": true
  },
  "secret_types": ["api_keys", "passwords", "tokens", "certificates"]
}

Response:
{
  "scan_id": "secrets_001",
  "secrets_found": [
    {
      "type": "api_key",
      "file": "src/config.py",
      "line": 12,
      "description": "Hardcoded API key detected",
      "confidence": "high"
    }
  ]
}
```

## Testing Component API

### Test Generation

```http
POST /testing/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "component": {
    "name": "user_service",
    "source_files": ["src/user_service.py"],
    "dependencies": ["database", "auth_service"]
  },
  "test_types": ["unit", "integration"],
  "coverage_target": 90,
  "test_framework": "pytest",
  "include_edge_cases": true
}

Response:
{
  "generation_id": "testgen_001",
  "status": "completed",
  "tests_generated": [
    {
      "file": "tests/test_user_service.py",
      "test_count": 12,
      "test_methods": [
        "test_create_user_success",
        "test_create_user_duplicate_email",
        "test_update_user_profile",
        "test_delete_user_cascade"
      ],
      "coverage_estimate": 92
    }
  ],
  "total_tests": 12,
  "estimated_coverage": 92
}
```

### Test Execution

```http
POST /testing/execute
Authorization: Bearer <token>
Content-Type: application/json

{
  "test_suite": "user_service_tests",
  "test_files": ["tests/test_user_service.py"],
  "coverage_report": true,
  "parallel": true
}

Response:
{
  "execution_id": "exec_001",
  "status": "running",
  "estimated_duration": "45s"
}
```

```http
GET /testing/execution/{execution_id}
Authorization: Bearer <token>

Response:
{
  "execution_id": "exec_001",
  "status": "completed",
  "results": {
    "total_tests": 12,
    "passed": 11,
    "failed": 1,
    "skipped": 0,
    "duration": "42.3s"
  },
  "coverage": {
    "line_coverage": 91.5,
    "branch_coverage": 87.2,
    "function_coverage": 95.0
  },
  "failed_tests": [
    {
      "test_name": "test_delete_user_cascade",
      "error_message": "AssertionError: Expected user to be deleted",
      "file": "tests/test_user_service.py",
      "line": 89
    }
  ]
}
```

## Code Intelligence API

### Code Parsing and Analysis

```http
POST /code/parse
Authorization: Bearer <token>
Content-Type: application/json

{
  "source_code": "def authenticate_user(email, password):\n    user = User.query.filter_by(email=email).first()\n    if user and user.check_password(password):\n        return user\n    return None",
  "language": "python",
  "analysis_types": ["ast", "dependencies", "complexity", "security"]
}

Response:
{
  "parse_id": "parse_001",
  "language": "python",
  "ast": {
    "type": "FunctionDef",
    "name": "authenticate_user",
    "args": ["email", "password"],
    "returns": "Optional[User]"
  },
  "dependencies": [
    {
      "name": "User",
      "type": "class",
      "module": "models"
    }
  ],
  "complexity": {
    "cyclomatic_complexity": 3,
    "cognitive_complexity": 2,
    "lines_of_code": 4
  },
  "security_issues": [
    {
      "type": "timing_attack",
      "severity": "medium",
      "description": "Potential timing attack in password comparison"
    }
  ]
}
```

### Dependency Analysis

```http
POST /code/dependencies
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_path": "src/",
  "language": "python",
  "include_external": true
}

Response:
{
  "analysis_id": "deps_001",
  "dependencies": {
    "internal": [
      {
        "name": "user_service",
        "path": "src/user_service.py",
        "depends_on": ["database", "auth_service"]
      }
    ],
    "external": [
      {
        "name": "fastapi",
        "version": "0.104.1",
        "type": "runtime"
      },
      {
        "name": "pytest",
        "version": "7.4.3",
        "type": "development"
      }
    ]
  },
  "dependency_graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

## Human Validation API

### Approval Requests

```http
POST /validation/request
Authorization: Bearer <token>
Content-Type: application/json

{
  "decision_type": "architecture_approval",
  "context": {
    "story_id": "story_001",
    "phase": 1,
    "description": "User authentication system architecture"
  },
  "options": [
    {
      "id": "option_1",
      "title": "JWT with Redis Session Store",
      "description": "Stateless JWT tokens with Redis for session management",
      "pros": ["Scalable", "Stateless", "Fast"],
      "cons": ["Token management complexity", "Redis dependency"],
      "estimated_effort": "medium"
    },
    {
      "id": "option_2",
      "title": "Traditional Session-Based",
      "description": "Server-side sessions with database storage",
      "pros": ["Simple", "Secure", "Easy to revoke"],
      "cons": ["Server state required", "Less scalable"],
      "estimated_effort": "low"
    }
  ],
  "recommendation": "option_1",
  "urgency": "medium",
  "timeout": "24h"
}

Response:
{
  "approval_id": "approval_001",
  "status": "pending",
  "expires_at": "2025-01-16T10:00:00Z",
  "notification_sent": true
}
```

```http
GET /validation/request/{approval_id}
Authorization: Bearer <token>

Response:
{
  "approval_id": "approval_001",
  "status": "approved",
  "decision": "option_1",
  "feedback": "Approved with recommendation to implement proper token rotation",
  "approved_by": "senior_architect",
  "approved_at": "2025-01-15T11:30:00Z",
  "additional_requirements": [
    "Implement token rotation every 15 minutes",
    "Add rate limiting for authentication endpoints"
  ]
}
```

### Decision History

```http
GET /validation/history
Authorization: Bearer <token>
Query Parameters:
  - story_id: string
  - decision_type: string
  - status: pending|approved|rejected|expired

Response:
{
  "decisions": [
    {
      "approval_id": "approval_001",
      "decision_type": "architecture_approval",
      "status": "approved",
      "decision": "option_1",
      "approved_by": "senior_architect",
      "approved_at": "2025-01-15T11:30:00Z"
    }
  ]
}
```

## File Operations API

### File Management

```http
GET /files/workspace
Authorization: Bearer <token>
Query Parameters:
  - story_id: string
  - file_type: source|test|config|docs

Response:
{
  "workspace_path": "/app/pathbridge_workspace",
  "files": [
    {
      "file_id": "file_001",
      "path": "story_001/src/auth_service.py",
      "type": "source",
      "language": "python",
      "size": 2048,
      "created_at": "2025-01-15T10:30:00Z",
      "modified_at": "2025-01-15T12:15:00Z"
    }
  ]
}
```

```http
GET /files/{file_id}/content
Authorization: Bearer <token>

Response:
{
  "file_id": "file_001",
  "path": "story_001/src/auth_service.py",
  "content": "from fastapi import FastAPI, HTTPException\n...",
  "encoding": "utf-8",
  "size": 2048
}
```

```http
POST /files/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "authenticate_user",
  "file_types": ["source", "test"],
  "languages": ["python"],
  "story_id": "story_001"
}

Response:
{
  "results": [
    {
      "file_id": "file_001",
      "path": "story_001/src/auth_service.py",
      "matches": [
        {
          "line": 15,
          "content": "def authenticate_user(email, password):",
          "context": "Function definition"
        }
      ]
    }
  ],
  "total_matches": 3
}
```

## Integration Services API

### CI/CD Integration

```http
POST /integration/cicd/pipeline
Authorization: Bearer <token>
Content-Type: application/json

{
  "story_id": "story_001",
  "pipeline_type": "build_and_test",
  "trigger": "code_generation_complete",
  "configuration": {
    "build_command": "uv run python -m pytest",
    "test_command": "uv run pytest tests/",
    "coverage_threshold": 90
  }
}

Response:
{
  "pipeline_id": "pipeline_001",
  "status": "created",
  "webhook_url": "https://pathbridge.local/webhooks/pipeline_001"
}
```

### Git Integration

```http
POST /integration/git/commit
Authorization: Bearer <token>
Content-Type: application/json

{
  "story_id": "story_001",
  "message": "feat(auth): implement user authentication service\n\n- Add JWT token generation\n- Implement password hashing\n- Add user validation logic",
  "files": [
    "story_001/src/auth_service.py",
    "story_001/tests/test_auth_service.py"
  ],
  "branch": "feature/user-authentication"
}

Response:
{
  "commit_id": "abc123def456",
  "branch": "feature/user-authentication",
  "status": "committed",
  "files_committed": 2
}
```

## Monitoring API

### System Metrics

```http
GET /monitoring/metrics
Authorization: Bearer <token>
Query Parameters:
  - timerange: 1h|24h|7d|30d
  - metrics: cpu|memory|requests|errors

Response:
{
  "timerange": "1h",
  "metrics": {
    "cpu_usage": {
      "current": 45.2,
      "average": 38.7,
      "peak": 67.3
    },
    "memory_usage": {
      "current": 512,
      "average": 487,
      "peak": 678
    },
    "requests_per_minute": {
      "current": 23,
      "average": 18,
      "peak": 45
    },
    "error_rate": {
      "current": 0.1,
      "average": 0.2,
      "peak": 1.2
    }
  }
}
```

### Component Health

```http
GET /monitoring/health
Authorization: Bearer <token>

Response:
{
  "overall_status": "healthy",
  "components": {
    "pathbridge_agent": {
      "status": "healthy",
      "response_time": "120ms",
      "last_check": "2025-01-15T12:30:00Z"
    },
    "security_scanner": {
      "status": "healthy",
      "response_time": "250ms",
      "last_check": "2025-01-15T12:30:00Z"
    },
    "database": {
      "status": "healthy",
      "connections": 5,
      "last_check": "2025-01-15T12:30:00Z"
    },
    "external_llm": {
      "status": "degraded",
      "response_time": "2.5s",
      "last_error": "Rate limit exceeded",
      "last_check": "2025-01-15T12:30:00Z"
    }
  }
}
```

## WebSocket Events

### Connection

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8080/ws');

// Authentication
ws.send(JSON.stringify({
  type: 'auth',
  token: 'bearer_token_here'
}));
```

### Event Types

```javascript
// Task Progress Updates
{
  "event_type": "task_progress",
  "data": {
    "task_id": "task_001",
    "phase": 2,
    "progress": 75,
    "current_step": "Generating integration tests",
    "estimated_completion": "2025-01-15T13:45:00Z"
  }
}

// Component Status Changes
{
  "event_type": "component_status",
  "data": {
    "component": "security_scanner",
    "status": "busy",
    "operation": "SAST scan in progress",
    "progress": 60
  }
}

// Human Attention Required
{
  "event_type": "human_attention_required",
  "data": {
    "approval_id": "approval_001",
    "decision_type": "architecture_approval",
    "urgency": "high",
    "timeout": "2025-01-15T14:00:00Z",
    "message": "Architecture decision required for user authentication"
  }
}

// Error Notifications
{
  "event_type": "error_notification",
  "data": {
    "component": "test_generator",
    "error_type": "generation_failed",
    "message": "Failed to generate tests for user_service.py",
    "details": {
      "file": "src/user_service.py",
      "reason": "Syntax error in source code"
    },
    "recoverable": true
  }
}

// Code Generation Complete
{
  "event_type": "code_generation_complete",
  "data": {
    "story_id": "story_001",
    "files_generated": [
      "story_001/src/auth_service.py",
      "story_001/tests/test_auth_service.py",
      "story_001/docs/auth_api.md"
    ],
    "next_phase": 3
  }
}
```

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid user story format",
    "details": {
      "field": "acceptance_criteria",
      "reason": "Missing 'then' condition in criteria 2",
      "expected_format": "Given-When-Then"
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_12345",
    "documentation_url": "https://docs.pathbridge.dev/errors/validation"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data or format |
| `AUTHENTICATION_ERROR` | 401 | Invalid or missing authentication |
| `AUTHORIZATION_ERROR` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Requested resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |
| `COMPONENT_ERROR` | 500 | Component processing error |
| `EXTERNAL_SERVICE_ERROR` | 502 | External service failure |
| `DATABASE_ERROR` | 500 | Database operation failed |

### Rate Limiting

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642248000
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Maximum 100 requests per hour.",
    "retry_after": 60
  }
}
```

---

**Corresponding Author**: PATH Framework Research Team  
**Institution**: Precocity Research Limited  
**Email**: info@precocity.nz  
**Date**: January 15, 2025  
**Version**: 1.0.0  
**Framework Version**: PathBridge v1.0.0 Complete API Specification  
**License**: MIT License - Open Source Methodology