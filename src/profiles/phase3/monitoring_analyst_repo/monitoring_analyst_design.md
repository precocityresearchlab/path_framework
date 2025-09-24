---
created_date: 2025-09-23
created_by: PATH Framework Team
last_modified: 2025-09-23
version: 1.0.0
purpose: Monitoring Analyst agent design specification
framework_phase: 3
dependencies: [base_agent, llm_interface, knowledge_base, deployment_specialist]
status: active
tags: [monitoring-analyst, phase3, monitoring, observability]
---

# Monitoring Analyst Agent Design

## Purpose
Set up comprehensive monitoring, alerting, and observability for production systems.

## Core Capabilities
- Design monitoring strategies
- Configure alerts and dashboards
- Implement observability practices
- Analyze system health metrics

## System Capabilities
- **File Operations**: Read/write monitoring configs, create dashboard definitions, manage alert rules
- **Command Execution**: Execute monitoring tools, run metric collectors, interact with observability platforms
- **Code Generation**: Generate monitoring configurations, create dashboard code, produce observability documentation
- **Analysis Tools**: Analyze system metrics, validate monitoring coverage, assess alert effectiveness

## Operations

### design_monitoring
- **Input**: `{system_architecture, sla_requirements}`
- **Output**: `{monitoring_strategy, metrics_plan, alerting_rules}`
- **Purpose**: Design comprehensive monitoring approach

### configure_observability
- **Input**: `{monitoring_requirements, system_components}`
- **Output**: `{observability_setup, dashboards, trace_configuration}`
- **Purpose**: Implement observability practices

### analyze_system_health
- **Input**: `{metrics_data, performance_baselines}`
- **Output**: `{health_analysis, trend_insights, recommendations}`
- **Purpose**: Analyze system health and performance

## Quality Metrics
- Monitoring coverage percentage
- Alert accuracy ratio
- Mean Time To Detection (MTTD)
- Dashboard effectiveness score

## Integration Points
- **Input from**: Deployment Specialist
- **Output to**: Reliability Engineer (Phase 4)
- **Shared Knowledge**: Monitoring data, system health metrics