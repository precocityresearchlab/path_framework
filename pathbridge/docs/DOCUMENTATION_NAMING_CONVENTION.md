---
created_date: 2025-09-24
created_by: PATH Framework Team
last_modified: 2025-09-24
version: 1.2.0
purpose: Standard naming convention for PathBridge documentation files and content
framework_phase: N/A
dependencies: [PATH Framework documentation rules]
status: active
tags: [naming-convention, documentation, standards, pathbridge, coreagent]
---

# PathBridge Documentation Naming Convention

![Framework](https://img.shields.io/badge/Framework-PATH-orange?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Institution](https://img.shields.io/badge/Institution-PATH%20Framework-purple?style=flat-square)
![Methodology](https://img.shields.io/badge/Methodology-Documentation%20Standards-red?style=flat-square)

## Overview

This document establishes the standard naming convention for all PathBridge documentation files and content, ensuring consistency and discoverability across the project.

## Core Terminology

### Agent Naming
- **CoreAgent**: The foundational agent class (formerly BaseAgent)
- **TypeAgent**: Specialized agent implementations (DomainAnalystAgent, TDDOrchestratorAgent, etc.)
- **PathBridge**: The universal bridge system connecting PATH Framework with external capabilities

### Component Naming
- **CoreAgent**: Base functionality shared by all agents
- **Capability**: Specific functionality that can be executed
- **Profile**: Configuration that defines agent behavior
- **Adapter**: Interface to external systems

## File Naming Patterns

### 1. Core Documentation Files
**Pattern**: `COREAGENT_[PURPOSE].md`
**Case**: UPPERCASE for main documentation
**Examples**:
- `COREAGENT_USAGE.md` - Usage guide and examples
- `COREAGENT_IMPLEMENTATION_TASKS.md` - Implementation task list
- `COREAGENT_API_REFERENCE.md` - API documentation

### 2. Architecture Documentation
**Pattern**: `[component]_architecture.md`
**Case**: lowercase with underscores
**Examples**:
- `coreagent_architecture.md` - CoreAgent design document
- `pathbridge_architecture.md` - PathBridge system architecture
- `capability_architecture.md` - Capability system design

### 3. Implementation Guides
**Pattern**: `[component]_implementation_guide.md`
**Case**: lowercase with underscores
**Examples**:
- `typeagent_implementation_guide.md` - How to create TypeAgents
- `capability_implementation_guide.md` - How to create capabilities
- `adapter_implementation_guide.md` - How to create adapters

### 4. Specifications
**Pattern**: `[COMPONENT]_SPECIFICATION_v[X.Y.Z].md`
**Case**: UPPERCASE for component, version suffix
**Examples**:
- `COREAGENT_SPECIFICATION_v1.0.0.md` - CoreAgent technical spec
- `PATHBRIDGE_SPECIFICATION_v1.0.0.md` - PathBridge system spec
- `AI_CODING_AGENT_SPECIFICATIONS_v1.0.0.md` - AI agent specifications

### 5. Configuration Files
**Pattern**: `[component]_config.md` or `[component]_configuration.md`
**Case**: lowercase with underscores
**Examples**:
- `coreagent_config.md` - CoreAgent configuration guide
- `pathbridge_configuration.md` - PathBridge setup guide
- `deployment_configuration.md` - Deployment setup

### 6. Process Documentation
**Pattern**: `[process]_[type].md`
**Case**: lowercase with underscores
**Examples**:
- `development_roadmap.md` - Development planning
- `testing_strategy.md` - Testing approach
- `deployment_process.md` - Deployment procedures

### 7. Reference Documentation
**Pattern**: `[component]_reference.md`
**Case**: lowercase with underscores
**Examples**:
- `api_reference.md` - API documentation
- `capability_reference.md` - Available capabilities
- `profile_reference.md` - Available profiles

## Content Naming Standards

### Headers and Titles
- **Main Title**: Use proper case with component names
  - ✅ "CoreAgent Usage Guide"
  - ❌ "BaseAgent Usage Guide"
  - ❌ "core agent usage guide"

### Code References
- **Classes**: Use PascalCase
  - ✅ `CoreAgent`
  - ✅ `DomainAnalystAgent`
  - ❌ `BaseAgent`
  - ❌ `baseAgent`

- **Methods**: Use snake_case
  - ✅ `execute_capability()`
  - ✅ `get_session_duration()`
  - ❌ `executeCapability()`

- **Files**: Use snake_case for Python, kebab-case for configs
  - ✅ `core_agent.py`
  - ✅ `docker-compose.yml`
  - ❌ `coreAgent.py`

### Variables and Parameters
- **Python**: Use snake_case
  - ✅ `agent_id`
  - ✅ `session_utc`
  - ❌ `agentId`

- **JSON/YAML**: Use snake_case
  - ✅ `"agent_id": "PATH_DEVELOPMENT"`
  - ❌ `"agentId": "PATH_DEVELOPMENT"`

## Version Management

### Document Versions
- **Format**: `X.Y.Z` (semantic versioning)
- **Increment Rules**:
  - **Major (X)**: Breaking changes, complete rewrites
  - **Minor (Y)**: New sections, significant additions
  - **Patch (Z)**: Corrections, small updates, clarifications

### Version Update Requirements
When updating documents:
1. Increment version number in YAML metadata
2. Update `last_modified` date
3. Add version notes if significant changes
4. Update any cross-references to version numbers

## Directory Structure

```
pathbridge/docs/
├── README.md                                    # Main overview
├── DOCUMENTATION_NAMING_CONVENTION.md          # This document
├── core/                                        # CoreAgent documentation
│   ├── COREAGENT_USAGE.md                      # Usage guide
│   ├── COREAGENT_IMPLEMENTATION_TASKS.md       # Implementation tasks
│   └── coreagent_architecture.md               # Architecture design
├── architecture/                                # System architecture
│   ├── pathbridge_architecture_diagram.md      # Architecture diagrams
│   ├── pathbridge_capability_standards.md      # Capability standards
│   └── pathbridge_interaction_mechanisms.md    # Interaction patterns
├── guides/                                      # Implementation guides
│   ├── pathbridge_llm_integration_guide.md     # LLM integration
│   └── pathbridge_ai_coding_assistant.md       # AI coding assistant
├── specifications/                              # Technical specifications
│   ├── AI_CODING_AGENT_SPECIFICATIONS_v1.0.0.md # AI agent specs
│   └── AGENT_SPECIFICATION_CODES_v1.0.0.md     # Specification codes
├── protocols/                                   # Communication protocols
│   ├── AGENT_DATA_EXCHANGE_PROTOCOLS_v1.0.0.md # Data exchange
│   └── PATH_PROTOCOL_V3.md                     # PATH protocol
└── planning/                                    # Project planning
    ├── AGENT_DEVELOPMENT_ROADMAP.md            # Development roadmap
    └── AGENT_IMPLEMENTATION_PLAN.md            # Implementation plan
```

## Migration from Old Naming

### Completed Migrations
- ✅ `BASEAGENT_USAGE.md` → `COREAGENT_USAGE.md`
- ✅ `core_agent_design.md` → `coreagent_architecture.md`
- ✅ `CORE_AGENT_TASKS.md` → `COREAGENT_IMPLEMENTATION_TASKS.md`

### Content Updates
- ✅ All references to "BaseAgent" updated to "CoreAgent"
- ✅ Version numbers incremented appropriately
- ✅ Metadata updated with new naming

## Validation Checklist

When creating or updating documentation:

### File Naming
- [ ] File name follows established pattern
- [ ] Case convention is correct
- [ ] Version suffix included for specifications
- [ ] No spaces or special characters (except underscores/hyphens)

### Content Naming
- [ ] CoreAgent used instead of BaseAgent
- [ ] Consistent case conventions throughout
- [ ] Proper component names used
- [ ] Code references follow language conventions

### Metadata
- [ ] YAML front matter includes all required fields
- [ ] Version number follows semantic versioning
- [ ] Last modified date is current
- [ ] Tags include relevant keywords

### Cross-References
- [ ] Links to other documents use correct file names
- [ ] Code examples use correct class/method names
- [ ] Version references are current

## Examples

### Good File Names
```
✅ COREAGENT_USAGE.md
✅ coreagent_architecture.md
✅ typeagent_implementation_guide.md
✅ PATHBRIDGE_SPECIFICATION_v1.0.0.md
✅ deployment_configuration.md
```

### Bad File Names
```
❌ BaseAgent_Usage.md
❌ CoreAgentArchitecture.md
❌ TypeAgent Implementation Guide.md
❌ pathbridge-spec-v1.md
❌ DeploymentConfig.md
```

### Good Content Examples
```markdown
# CoreAgent Usage Guide

## Quick Start

```python
from src.core.core_agent import CoreAgent

agent = CoreAgent("development")
```

### Good Class References
- CoreAgent
- DomainAnalystAgent
- CapabilityRequest
```

### Bad Content Examples
```markdown
# BaseAgent Usage Guide

## Quick Start

```python
from src.core.base_agent import BaseAgent

agent = BaseAgent("development")
```

### Bad Class References
- BaseAgent
- domainAnalystAgent
- capabilityrequest
```

## Enforcement

This naming convention is enforced through:
1. **Code Reviews**: All documentation changes reviewed for compliance
2. **Automated Checks**: Scripts to validate file names and content
3. **Documentation Audits**: Regular reviews of naming consistency
4. **Update Procedures**: Systematic migration of non-compliant files

## Future Considerations

As PathBridge evolves, this naming convention may be updated to include:
- New component types and their naming patterns
- Integration-specific documentation patterns
- Multi-language documentation conventions
- API versioning in documentation names

---

**Compliance**: This document follows PATH Framework documentation rules and establishes PathBridge-specific standards for consistent, discoverable documentation.