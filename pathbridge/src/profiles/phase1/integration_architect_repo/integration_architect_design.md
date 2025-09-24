---
created_date: 2025-09-23
created_by: PATH Framework Team
last_modified: 2025-09-23
version: 1.0.0
purpose: Integration Architect agent design specification
framework_phase: 1
dependencies: [base_agent, llm_interface, knowledge_base, component_designer]
status: active
tags: [integration-architect, phase1, integration, communication]
---

# Integration Architect Agent Design

## Purpose
Design integration patterns, communication protocols, and data flow between components and external systems.

## Core Capabilities
- Design integration patterns and strategies
- Define communication protocols
- Map data flow between components
- Plan external system integrations

## System Capabilities
- **File Operations**: Read/write integration configurations, create protocol specifications, manage mapping files
- **Command Execution**: Execute integration tests, run protocol validators, interact with messaging tools
- **Code Generation**: Generate integration adapters, protocol handlers, data transformation code
- **Analysis Tools**: Analyze data flows, validate integration patterns, assess communication protocols

## Operations

### design_integrations
- **Input**: `{components, external_systems, integration_requirements}`
- **Output**: `{integration_patterns, communication_design, protocols}`
- **Purpose**: Design how components integrate with each other

### define_protocols
- **Input**: `{communication_needs, performance_requirements}`
- **Output**: `{protocol_specifications, message_formats, error_handling}`
- **Purpose**: Define communication protocols and message formats

### map_data_flow
- **Input**: `{components, data_requirements, business_processes}`
- **Output**: `{data_flow_diagrams, transformation_rules, validation_points}`
- **Purpose**: Map how data flows through the system

### validate_integrations
- **Input**: `{integration_design, quality_requirements}`
- **Output**: `{validation_results, performance_analysis, risk_assessment}`
- **Purpose**: Validate integration design quality and feasibility

## Quality Metrics
- Integration complexity score
- Data consistency validation
- Performance impact assessment
- Error handling completeness

## Integration Points
- **Input from**: Component Designer
- **Output to**: Phase 2 (TDD Orchestrator)
- **Shared Knowledge**: Integration patterns, communication protocols