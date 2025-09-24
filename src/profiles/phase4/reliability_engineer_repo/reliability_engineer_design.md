---
created_date: 2025-09-23
created_by: PATH Framework Team
last_modified: 2025-09-23
version: 1.0.0
purpose: Reliability Engineer agent design specification
framework_phase: 4
dependencies: [base_agent, llm_interface, knowledge_base, monitoring_analyst]
status: active
tags: [reliability-engineer, phase4, sre, operations]
---

# Reliability Engineer Agent Design

## Purpose
Ensure system reliability, availability, and performance in production environments.

## Core Capabilities
- Monitor system reliability metrics
- Implement SRE practices and procedures
- Manage incident response and recovery
- Optimize system performance and availability

## System Capabilities
- **File Operations**: Read/write monitoring configurations, create runbooks, manage incident logs
- **Command Execution**: Execute monitoring tools, run diagnostic commands, interact with infrastructure
- **Code Generation**: Generate monitoring scripts, create automation tools, produce operational documentation
- **Analysis Tools**: Analyze system metrics, validate SRE practices, assess reliability patterns

## Operations

### monitor_reliability
- **Input**: `{system_metrics, sla_requirements}`
- **Output**: `{reliability_status, trend_analysis, recommendations}`
- **Purpose**: Monitor and analyze system reliability

### manage_incidents
- **Input**: `{incident_data, severity_level}`
- **Output**: `{response_plan, escalation_procedures, resolution_steps}`
- **Purpose**: Coordinate incident response and resolution

### optimize_performance
- **Input**: `{performance_metrics, bottleneck_analysis}`
- **Output**: `{optimization_plan, resource_adjustments, scaling_recommendations}`
- **Purpose**: Optimize system performance and resource usage

### implement_sre_practices
- **Input**: `{system_architecture, reliability_goals}`
- **Output**: `{sre_procedures, automation_scripts, monitoring_setup}`
- **Purpose**: Implement Site Reliability Engineering practices

## Quality Metrics
- System uptime percentage
- Mean Time To Recovery (MTTR)
- Service Level Objective (SLO) compliance
- Error budget consumption

## Integration Points
- **Input from**: Monitoring Analyst (Phase 3)
- **Output to**: Operations Specialist
- **Shared Knowledge**: Reliability metrics, incident procedures