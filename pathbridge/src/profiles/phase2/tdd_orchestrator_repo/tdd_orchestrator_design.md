---
created_date: 2025-09-23
created_by: PATH Framework Team
last_modified: 2025-09-23
version: 1.0.0
purpose: TDD Orchestrator agent design specification
framework_phase: 2
dependencies: [base_agent, llm_interface, knowledge_base, integration_architect]
status: active
tags: [tdd-orchestrator, phase2, test-driven-development, orchestration]
---

# TDD Orchestrator Agent Design

## Purpose
Orchestrate the Test-Driven Development process, coordinating between test creation and implementation.

## Core Capabilities
- Coordinate Red-Green-Refactor cycles
- Manage test execution workflow
- Ensure TDD discipline adherence
- Track development progress

## System Capabilities
- **File Operations**: Read/write test files, create test configurations, manage test data
- **Command Execution**: Execute test runners, run coverage tools, interact with build systems
- **Code Generation**: Generate test templates, create test fixtures, produce test reports
- **Analysis Tools**: Analyze test results, track coverage metrics, assess TDD compliance

## Operations

### orchestrate_tdd_cycle
- **Input**: `{requirements, current_state}`
- **Output**: `{cycle_plan, test_priorities, implementation_order}`
- **Purpose**: Plan and coordinate TDD cycles

### manage_red_phase
- **Input**: `{failing_tests, requirements}`
- **Output**: `{test_validation, next_actions, cycle_status}`
- **Purpose**: Manage the Red phase of TDD cycle

### manage_green_phase
- **Input**: `{tests, implementation_status}`
- **Output**: `{implementation_guidance, completion_check, quality_metrics}`
- **Purpose**: Manage the Green phase of TDD cycle

### manage_refactor_phase
- **Input**: `{working_code, quality_metrics}`
- **Output**: `{refactor_recommendations, code_improvements, cycle_completion}`
- **Purpose**: Manage the Refactor phase of TDD cycle

## Quality Metrics
- TDD cycle adherence score
- Test-first discipline measurement
- Code coverage progression
- Refactoring effectiveness

## Integration Points
- **Input from**: Integration Architect (Phase 1)
- **Output to**: Test Strategist, Implementation Specialist
- **Shared Knowledge**: TDD progress, cycle status