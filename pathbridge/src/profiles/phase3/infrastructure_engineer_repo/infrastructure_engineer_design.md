---
created_date: 2025-09-23
created_by: PATH Framework Team
last_modified: 2025-09-23
version: 1.0.0
purpose: Infrastructure Engineer agent design specification
framework_phase: 3
dependencies: [base_agent, llm_interface, knowledge_base, pipeline_architect]
status: active
tags: [infrastructure-engineer, phase3, infrastructure, provisioning]
---

# Infrastructure Engineer Agent Design

## Purpose
Design and provision infrastructure for application deployment and operations.

## Core Capabilities
- Design infrastructure architecture
- Provision cloud resources
- Configure networking and security
- Implement Infrastructure as Code

## System Capabilities
- **File Operations**: Read/write infrastructure configs, create IaC templates, manage deployment files
- **Command Execution**: Execute infrastructure tools, run provisioning commands, interact with cloud APIs
- **Code Generation**: Generate IaC templates, create configuration files, produce infrastructure documentation
- **Analysis Tools**: Analyze infrastructure costs, validate configurations, assess security posture

## Operations

### design_infrastructure
- **Input**: `{application_requirements, scalability_needs}`
- **Output**: `{infrastructure_design, resource_specifications, cost_estimates}`
- **Purpose**: Design infrastructure architecture

### provision_resources
- **Input**: `{infrastructure_design, environment_config}`
- **Output**: `{provisioned_resources, configuration_status, access_details}`
- **Purpose**: Provision and configure infrastructure

### configure_security
- **Input**: `{security_requirements, compliance_needs}`
- **Output**: `{security_configuration, policies, monitoring_setup}`
- **Purpose**: Implement security controls and policies

## Quality Metrics
- Infrastructure reliability score
- Security compliance percentage
- Cost optimization ratio
- Provisioning success rate

## Integration Points
- **Input from**: Pipeline Architect
- **Output to**: Deployment Specialist
- **Shared Knowledge**: Infrastructure configuration, resource details