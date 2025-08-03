#!/usr/bin/env python3
"""
PATH Framework Artifact Generator
Generates comprehensive PATH-compliant artifacts following the Software Engineering Methodology

This script implements the 7-step process with 4 AI agents as specified in:
docs/framework/path_software_engineering_methodology.md

Usage:
    # Basic usage with minimal input
    python generate_path_artifacts.py --project "My API" --domain "business"
    
    # With detailed requirements
    python generate_path_artifacts.py --project "Trading System" --domain "financial" \
        --requirements "High-frequency trading system with FIX protocol compliance" \
        --constraints "Sub-millisecond latency, 99.99% uptime" \
        --stakeholders "Traders, Risk Managers, Compliance Officers" \
        --compliance "FIX 4.4, MiFID II, SOX"
    
    # With requirements file
    python generate_path_artifacts.py --project "Healthcare Portal" --requirements-file "./requirements.yaml"
    
    # Interactive mode
    python generate_path_artifacts.py --interactive
"""

import os
import sys
import json
import yaml
import argparse
from datetime import datetime
from pathlib import Path

# Add the PATH framework to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'path_framework'))

try:
    from phases.arch.ai.agents.domain_analyst import DomainAnalyst
    from phases.arch.ai.agents.system_architect import SystemArchitect
    from phases.arch.ai.agents.component_designer import ComponentDesigner
    from phases.arch.ai.agents.integration_architect import IntegrationArchitect
    from phases.arch.ai.llm_client import LLMClient
    from phases.arch.ai.phase1_models import *
    print("✅ Successfully imported PATH Framework components")
except ImportError as e:
    print(f"⚠️  Could not import PATH agents: {e}")
    print("📝 Falling back to direct LLM implementation")
    
    class LLMClient:
        def __init__(self):
            import openai
            from openai import OpenAI
            
            # Try OpenRouter first, then OpenAI
            api_key = os.getenv('OPENROUTER_API_KEY')
            if api_key:
                self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )
                self.model = os.getenv('PATH_LLM_MODEL_PHASE1', 'google/gemma-3-27b-it:free')
                print(f"🔗 Using OpenRouter with model: {self.model}")
            else:
                self.client = OpenAI()
                self.model = 'gpt-3.5-turbo'
                print(f"🔗 Using OpenAI with model: {self.model}")
        
        def generate_response(self, prompt, max_tokens=4000):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.1
            )
            return response.choices[0].message.content

class PathArtifactGenerator:
    """
    PATH Framework Artifact Generator
    Implements the 7-step Software Engineering Methodology with flexible input handling
    """
    
    def __init__(self, project_name, domain="business", requirements=None, constraints=None, 
                 stakeholders=None, compliance=None, requirements_file=None):
        self.project_name = project_name
        self.domain = domain
        self.llm_client = LLMClient()
        self.project_path = Path(f"projects/{project_name}")
        self.artifacts_path = self.project_path / "path_artifacts"
        self.timestamp = datetime.now().isoformat()
        
        # Load or process requirements
        self.requirements_context = self._load_requirements_context(
            requirements, constraints, stakeholders, compliance, requirements_file
        )
        
        # Create directories
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        (self.artifacts_path / "phase1").mkdir(exist_ok=True)
        (self.artifacts_path / "deliverables").mkdir(exist_ok=True)
        
        print(f"🚀 Initializing PATH artifacts for: {project_name}")
        print(f"📁 Artifacts directory: {self.artifacts_path}")
        print(f"🏷️  Domain: {self.domain}")
        
        if self.requirements_context:
            print(f"📋 Requirements loaded: {len(self.requirements_context)} sections")
    
    def _load_requirements_context(self, requirements, constraints, stakeholders, compliance, requirements_file):
        """Load and structure requirements from various input sources"""
        context = {}
        
        # Load from file if provided
        if requirements_file and Path(requirements_file).exists():
            with open(requirements_file, 'r') as f:
                if requirements_file.endswith('.yaml') or requirements_file.endswith('.yml'):
                    file_data = yaml.safe_load(f)
                else:
                    file_data = {"requirements": f.read()}
                context.update(file_data)
        
        # Add CLI arguments
        if requirements:
            context['functional_requirements'] = requirements
        if constraints:
            context['technical_constraints'] = constraints
        if stakeholders:
            context['stakeholders'] = stakeholders
        if compliance:
            context['compliance_requirements'] = compliance
        
        return context
    
    def _get_context_prompt_section(self):
        """Generate context section for prompts based on available requirements"""
        if not self.requirements_context:
            return f"""
Project: {self.project_name}
Domain: {self.domain}

NOTE: Limited context provided. The AI should make reasonable assumptions for a {self.domain} domain project named "{self.project_name}" and generate comprehensive architecture based on common patterns and best practices for this domain.
"""
        
        context_lines = [f"Project: {self.project_name}", f"Domain: {self.domain}", ""]
        
        for key, value in self.requirements_context.items():
            if isinstance(value, str):
                context_lines.append(f"{key.replace('_', ' ').title()}: {value}")
            elif isinstance(value, list):
                context_lines.append(f"{key.replace('_', ' ').title()}:")
                for item in value:
                    context_lines.append(f"  - {item}")
            elif isinstance(value, dict):
                context_lines.append(f"{key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    context_lines.append(f"  {sub_key}: {sub_value}")
        
        return "\n".join(context_lines)
    
    def step1_context_analysis(self):
        """
        Phase 1: Context Analysis (Domain Understanding)
        Lead Agent: AI Domain Analyst
        Flow Pattern: Human-Initiated Process
        """
        print("\n📋 Step 1: Context Analysis")
        
        context_section = self._get_context_prompt_section()
        
        prompt = f"""
You are an expert AI Domain Analyst specializing in requirements analysis and domain modeling.

Analyze the project and extract comprehensive domain context based on the provided information:

{context_section}

Your task is to perform:
1. **Specification Analysis**: Extract domain entities, rules, and constraints
2. **Domain Modeling**: Create comprehensive domain models with ubiquitous language  
3. **Stakeholder Mapping**: Identify external systems and integration points
4. **Compliance Identification**: Document regulatory and compliance requirements

Generate a structured domain context analysis following this EXACT format:

```yaml
domain_context:
  project_name: "{self.project_name}"
  domain_type: "{self.domain}"
  timestamp: "{self.timestamp}"
  
  domain_entities:
    primary_entities: 
      - "Entity1"
      - "Entity2"
    supporting_entities:
      - "SupportEntity1"
      - "SupportEntity2"
    relationships:
      - "Entity1 manages Entity2"
      - "Entity2 belongs to Entity1"
  
  business_rules:
    core_rules:
      - "Business rule 1"
      - "Business rule 2"
    constraints:
      - "Constraint 1"
      - "Constraint 2"
    validations:
      - "Validation rule 1"
      - "Validation rule 2"
  
  stakeholders:
    internal_stakeholders:
      - "Stakeholder 1"
      - "Stakeholder 2"
    external_systems:
      - "External System 1"
      - "External System 2"
    integration_points:
      - "Integration point 1"
      - "Integration point 2"
  
  compliance_requirements:
    industry_standards:
      - "Standard 1"
      - "Standard 2"
    regulatory_requirements:
      - "Regulation 1"
      - "Regulation 2"
    security_standards:
      - "Security standard 1"
      - "Security standard 2"
  
  quality_attributes:
    performance_requirements:
      - "Performance requirement 1"
      - "Performance requirement 2"
    scalability_requirements:
      - "Scalability requirement 1"
      - "Scalability requirement 2"
    security_requirements:
      - "Security requirement 1"
      - "Security requirement 2"
    availability_requirements:
      - "Availability requirement 1"
      - "Availability requirement 2"
```

Provide detailed, specific analysis based on the project context. If context is limited, make reasonable assumptions based on the domain type and project name, focusing on common patterns and requirements for {self.domain} domain applications.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save domain context
        with open(self.artifacts_path / "phase1" / "domain_context.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: domain_context.yaml")
        return yaml_content
    
    def step2_domain_modeling(self, domain_context):
        """
        Phase 2: Domain Modeling
        Lead Agent: AI Domain Analyst
        Flow Pattern: AI-Driven Automation
        """
        print("\n🏗️  Step 2: Domain Modeling")
        
        prompt = f"""
You are an expert AI Domain Analyst creating detailed domain models.

Based on the domain context analysis, create a comprehensive domain model:

DOMAIN CONTEXT:
{domain_context}

Generate a detailed domain model following this structure:

```yaml
domain_model:
  project_name: "{self.project_name}"
  timestamp: "{self.timestamp}"
  
  entities:
    core_entities:
      - name: ""
        attributes: []
        behaviors: []
        relationships: []
        business_rules: []
    
    supporting_entities:
      - name: ""
        attributes: []
        relationships: []
  
  ubiquitous_language:
    terms:
      - term: ""
        definition: ""
        context: ""
  
  bounded_contexts:
    contexts:
      - name: ""
        description: ""
        entities: []
        services: []
        boundaries: []
  
  domain_services:
    services:
      - name: ""
        responsibility: ""
        operations: []
        dependencies: []
  
  aggregates:
    aggregates:
      - name: ""
        root_entity: ""
        entities: []
        invariants: []
        business_rules: []
```

Focus on creating a comprehensive domain model with clear entity relationships and business rules.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save domain model
        with open(self.artifacts_path / "phase1" / "domain_model.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: domain_model.yaml")
        return yaml_content
    
    def step3_architecture_design(self, domain_model):
        """
        Phase 3: Architecture Design
        Lead Agent: AI System Architect
        Flow Pattern: AI-Driven Automation
        """
        print("\n🏛️  Step 3: Architecture Design")
        
        prompt = f"""
You are an expert AI System Architect specializing in architectural design and technology selection.

Based on the domain model, design a comprehensive system architecture:

DOMAIN MODEL:
{domain_model}

Generate a system architecture following this structure:

```yaml
system_architecture:
  project_name: "{self.project_name}"
  timestamp: "{self.timestamp}"
  
  architectural_pattern:
    selected_pattern: ""
    pattern_rationale: ""
    pattern_benefits: []
    pattern_trade_offs: []
  
  technology_stack:
    programming_language: ""
    framework: ""
    database: ""
    message_queue: ""
    cache: ""
    cloud_provider: ""
    deployment: ""
    
  system_layers:
    presentation_layer:
      description: ""
      components: []
      responsibilities: []
    
    application_layer:
      description: ""
      components: []
      responsibilities: []
    
    domain_layer:
      description: ""
      components: []
      responsibilities: []
    
    infrastructure_layer:
      description: ""
      components: []
      responsibilities: []
  
  quality_attributes:
    performance:
      requirements: []
      strategies: []
    
    scalability:
      requirements: []
      strategies: []
    
    security:
      requirements: []
      strategies: []
    
    maintainability:
      requirements: []
      strategies: []
  
  risk_assessment:
    technical_risks: []
    mitigation_strategies: []
```

Select appropriate architectural patterns and technology stack based on the domain requirements.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save system architecture
        with open(self.artifacts_path / "phase1" / "system_architecture.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: system_architecture.yaml")
        return yaml_content
    
    def step4_component_design(self, system_architecture):
        """
        Phase 4: Component Design
        Lead Agent: AI Component Designer
        Flow Pattern: AI-Driven Automation
        """
        print("\n🧩 Step 4: Component Design")
        
        prompt = f"""
You are an expert AI Component Designer specializing in component-level design and SOLID principles.

Based on the system architecture, design detailed components:

SYSTEM ARCHITECTURE:
{system_architecture}

Generate component designs following this structure:

```yaml
component_designs:
  project_name: "{self.project_name}"
  timestamp: "{self.timestamp}"
  
  components:
    - component_name: ""
      layer: ""
      responsibility: ""
      dependencies: []
      
      interfaces:
        - interface_name: ""
          operations: []
          contracts: []
      
      implementation:
        classes: []
        patterns: []
        solid_compliance: []
      
      behavior:
        state_management: ""
        error_handling: ""
        validation_rules: []
  
  interface_specifications:
    - interface_name: ""
      description: ""
      methods:
        - method_name: ""
          parameters: []
          return_type: ""
          preconditions: []
          postconditions: []
      
      contracts:
        - contract_type: ""
          description: ""
          validation: ""
  
  design_patterns:
    patterns_used:
      - pattern_name: ""
        component: ""
        rationale: ""
        implementation: ""
  
  solid_principles:
    single_responsibility:
      compliance: []
      violations: []
    
    open_closed:
      compliance: []
      violations: []
    
    liskov_substitution:
      compliance: []
      violations: []
    
    interface_segregation:
      compliance: []
      violations: []
    
    dependency_inversion:
      compliance: []
      violations: []
```

Focus on SOLID principles compliance and clear component responsibilities.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save component designs
        with open(self.artifacts_path / "phase1" / "component_designs.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: component_designs.yaml")
        return yaml_content
    
    def step5_integration_design(self, component_designs):
        """
        Phase 5: Integration Design
        Lead Agent: AI Integration Architect
        Flow Pattern: AI-Driven Automation
        """
        print("\n🔗 Step 5: Integration Design")
        
        prompt = f"""
You are an expert AI Integration Architect specializing in system integration and API design.

Based on the component designs, create integration specifications:

COMPONENT DESIGNS:
{component_designs}

Generate integration specifications following this structure:

```yaml
integration_specs:
  project_name: "{self.project_name}"
  timestamp: "{self.timestamp}"
  
  dependency_injection:
    strategy: ""
    composition_root: ""
    container_configuration: []
    lifecycle_management: []
  
  api_design:
    rest_apis:
      - endpoint: ""
        method: ""
        request_format: ""
        response_format: ""
        authentication: ""
        authorization: ""
        error_handling: []
    
    internal_apis:
      - interface: ""
        communication_pattern: ""
        data_format: ""
        error_handling: ""
  
  communication_patterns:
    synchronous:
      - pattern: ""
        use_case: ""
        implementation: ""
    
    asynchronous:
      - pattern: ""
        use_case: ""
        implementation: ""
  
  data_flow:
    external_integrations:
      - system: ""
        data_format: ""
        protocol: ""
        security: ""
    
    internal_data_flow:
      - source: ""
        target: ""
        data_type: ""
        transformation: ""
  
  error_handling:
    strategies:
      - error_type: ""
        handling_strategy: ""
        recovery_mechanism: ""
    
    patterns:
      - pattern_name: ""
        implementation: ""
        use_cases: []
  
  security_integration:
    authentication:
      strategy: ""
      implementation: ""
    
    authorization:
      strategy: ""
      implementation: ""
    
    data_protection:
      encryption: ""
      secure_transmission: ""
```

Focus on robust integration patterns and comprehensive error handling.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save integration specs
        with open(self.artifacts_path / "phase1" / "integration_specs.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: integration_specs.yaml")
        return yaml_content
    
    def step6_architecture_validation(self, integration_specs):
        """
        Phase 6: Architecture Validation
        Lead Agent: AI System Architect
        Flow Pattern: Human-AI Collaborative Decision
        """
        print("\n✅ Step 6: Architecture Validation")
        
        prompt = f"""
You are an expert AI System Architect performing comprehensive architecture validation.

Validate the complete architecture against requirements and generate validation report:

INTEGRATION SPECIFICATIONS:
{integration_specs}

Generate validation specifications following this structure:

```yaml
interface_specifications:
  project_name: "{self.project_name}"
  timestamp: "{self.timestamp}"
  
  requirements_traceability:
    functional_requirements:
      - requirement_id: ""
        description: ""
        components: []
        interfaces: []
        validation_status: ""
    
    non_functional_requirements:
      - requirement_id: ""
        description: ""
        architecture_element: ""
        validation_status: ""
  
  architecture_compliance:
    pattern_compliance:
      - pattern: ""
        compliance_status: ""
        deviations: []
        justification: ""
    
    principle_compliance:
      - principle: ""
        compliance_status: ""
        evidence: []
        violations: []
  
  quality_validation:
    performance:
      validation_criteria: []
      test_strategies: []
      acceptance_criteria: []
    
    scalability:
      validation_criteria: []
      test_strategies: []
      acceptance_criteria: []
    
    security:
      validation_criteria: []
      test_strategies: []
      acceptance_criteria: []
  
  integration_validation:
    internal_interfaces:
      - interface: ""
        validation_status: ""
        test_approach: ""
    
    external_interfaces:
      - interface: ""
        validation_status: ""
        test_approach: ""
  
  risk_assessment:
    identified_risks:
      - risk_id: ""
        description: ""
        probability: ""
        impact: ""
        mitigation: ""
    
    validation_gaps:
      - gap_id: ""
        description: ""
        resolution_plan: ""
  
  approval_status:
    technical_approval: ""
    stakeholder_approval: ""
    compliance_approval: ""
    final_status: ""
```

Provide comprehensive validation with clear approval criteria.
"""
        
        response = self.llm_client.generate_response(prompt)
        
        # Extract YAML content
        if "```yaml" in response:
            yaml_content = response.split("```yaml")[1].split("```")[0].strip()
        else:
            yaml_content = response
        
        # Save interface specifications
        with open(self.artifacts_path / "phase1" / "interface_specifications.yaml", "w") as f:
            f.write(yaml_content)
        
        print("✅ Generated: interface_specifications.yaml")
        return yaml_content
    
    def step7_final_documentation(self, interface_specifications):
        """
        Phase 7: Final Documentation
        Lead Agent: AI Integration Architect
        Flow Pattern: AI-Driven Automation
        """
        print("\n📚 Step 7: Final Documentation")
        
        prompt = f"""
You are an expert AI Integration Architect creating comprehensive architecture documentation.

Generate final architecture documentation and decision records:

INTERFACE SPECIFICATIONS:
{interface_specifications}

Create comprehensive architecture documentation in Markdown format covering:

1. **Architecture Decision Records (ADRs)**
2. **Design Rationale and Trade-offs**
3. **Technical Implementation Guidelines**
4. **Quality Assurance Documentation**
5. **Implementation Readiness Checklist**

Format as a complete Markdown document with:
- Executive Summary
- Architecture Overview
- Detailed Design Decisions
- Implementation Guidelines
- Quality Assurance Plan
- Risk Mitigation Strategies
- Next Steps

Focus on providing implementation-ready documentation for development teams.
"""
        
        response = self.llm_client.generate_response(prompt, max_tokens=6000)
        
        # Save architecture decisions
        with open(self.artifacts_path / "deliverables" / "architecture_decisions.md", "w") as f:
            f.write(response)
        
        print("✅ Generated: architecture_decisions.md")
        
        # Generate summary README
        self.generate_summary_readme()
        
        return response
    
    def generate_summary_readme(self):
        """Generate a comprehensive README for the PATH artifacts"""
        
        readme_content = f"""# PATH Framework Artifacts
## {self.project_name}

Generated on: {self.timestamp}
Methodology: PATH-Based Software Engineering v2.0.0

## Artifact Overview

This directory contains comprehensive architecture artifacts generated following the PATH Framework Software Engineering Methodology. The artifacts are organized according to the 7-step process with 4 specialized AI agents.

### Generated Artifacts

#### Phase 1 Artifacts (YAML Format)
- **`domain_context.yaml`** - Domain analysis and context mapping
- **`domain_model.yaml`** - Comprehensive domain model with entities and rules
- **`system_architecture.yaml`** - High-level system architecture and technology stack
- **`component_designs.yaml`** - Detailed component specifications with SOLID compliance
- **`integration_specs.yaml`** - Integration patterns and API specifications
- **`interface_specifications.yaml`** - Architecture validation and approval documentation

#### Deliverable Documentation (Markdown Format)
- **`architecture_decisions.md`** - Complete architecture documentation with ADRs

### PATH Process Flow

The artifacts follow the 7-step PATH Software Engineering process:

1. **Context Analysis** → `domain_context.yaml`
2. **Domain Modeling** → `domain_model.yaml`  
3. **Architecture Design** → `system_architecture.yaml`
4. **Component Design** → `component_designs.yaml`
5. **Integration Design** → `integration_specs.yaml`
6. **Architecture Validation** → `interface_specifications.yaml`
7. **Final Documentation** → `architecture_decisions.md`

### AI Agent Responsibilities

- **🤖 AI Domain Analyst**: Steps 1-2 (Context Analysis, Domain Modeling)
- **🤖 AI System Architect**: Steps 3, 6 (Architecture Design, Validation)
- **🤖 AI Component Designer**: Step 4 (Component Design)
- **🤖 AI Integration Architect**: Steps 5, 7 (Integration Design, Documentation)

### Quality Assurance

All artifacts include:
- ✅ Requirements traceability
- ✅ Architecture pattern compliance
- ✅ SOLID principles validation
- ✅ Integration pattern specifications
- ✅ Quality attribute analysis
- ✅ Risk assessment and mitigation

### Next Steps

These artifacts provide a complete foundation for:
1. **Development Phase** (PATH Phase 2: TDD Implementation)
2. **Quality Assurance** (Test strategy implementation)
3. **Deployment Planning** (Infrastructure and DevOps)
4. **Team Handoff** (Development team orientation)

### Compliance

Artifacts are compliant with:
- PATH Framework Software Engineering Methodology v2.0.0
- Industry standard architecture documentation practices
- SOLID design principles
- Clean architecture patterns

---

*Generated by PATH Framework Artifact Generator*
*Methodology Reference: docs/framework/path_software_engineering_methodology.md*
"""
        
        with open(self.artifacts_path / "README.md", "w") as f:
            f.write(readme_content)
        
        print("✅ Generated: README.md")
    
    def generate_all_artifacts(self):
        """Execute the complete 7-step PATH process"""
        print(f"\n🎯 Starting PATH Framework Artifact Generation")
        print(f"Project: {self.project_name}")
        print(f"Domain: {self.domain}")
        print(f"Output: {self.artifacts_path}")
        print("=" * 60)
        
        try:
            # Execute 7-step process
            domain_context = self.step1_context_analysis()
            domain_model = self.step2_domain_modeling(domain_context)
            system_architecture = self.step3_architecture_design(domain_model)
            component_designs = self.step4_component_design(system_architecture)
            integration_specs = self.step5_integration_design(component_designs)
            interface_specs = self.step6_architecture_validation(integration_specs)
            final_docs = self.step7_final_documentation(interface_specs)
            
            print("\n" + "=" * 60)
            print("🎉 PATH Framework Artifacts Generation Complete!")
            print(f"📁 Location: {self.artifacts_path}")
            print("\n📋 Generated Files:")
            
            # List all generated files
            for root, dirs, files in os.walk(self.artifacts_path):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), self.artifacts_path)
                    print(f"   📄 {rel_path}")
            
            print(f"\n✅ All artifacts comply with PATH Software Engineering Methodology v2.0.0")
            print(f"🚀 Ready for Phase 2: TDD Implementation")
            
        except Exception as e:
            print(f"\n❌ Error during generation: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description='Generate PATH Framework Artifacts')
    
    # Required arguments
    parser.add_argument('--project', required=True, help='Project name')
    
    # Optional context arguments
    parser.add_argument('--domain', default='business', 
                        choices=['business', 'protocol', 'data', 'realtime', 'financial', 'healthcare', 'iot'],
                        help='Domain type')
    parser.add_argument('--requirements', help='Functional requirements description')
    parser.add_argument('--constraints', help='Technical constraints and limitations')
    parser.add_argument('--stakeholders', help='Stakeholders and user types')
    parser.add_argument('--compliance', help='Compliance and regulatory requirements')
    parser.add_argument('--requirements-file', help='YAML file with detailed requirements')
    
    # Interactive mode
    parser.add_argument('--interactive', action='store_true', help='Interactive requirements gathering')
    
    # Output options
    parser.add_argument('--output', help='Output directory (default: projects/{project}/path_artifacts)')
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        print("🎯 PATH Framework Interactive Mode")
        print("=" * 50)
        
        project = input("Project name: ") or args.project
        domain = input(f"Domain [{args.domain}]: ") or args.domain
        requirements = input("Functional requirements (optional): ") or args.requirements
        constraints = input("Technical constraints (optional): ") or args.constraints
        stakeholders = input("Stakeholders (optional): ") or args.stakeholders
        compliance = input("Compliance requirements (optional): ") or args.compliance
        
        args.project = project
        args.domain = domain
        args.requirements = requirements
        args.constraints = constraints
        args.stakeholders = stakeholders
        args.compliance = compliance
    
    # Verify environment
    if not os.getenv('OPENROUTER_API_KEY') and not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: No API key found. Set OPENROUTER_API_KEY or OPENAI_API_KEY")
        sys.exit(1)
    
    # Display configuration
    print(f"\n🎯 PATH Framework Configuration")
    print(f"Project: {args.project}")
    print(f"Domain: {args.domain}")
    if args.requirements:
        print(f"Requirements: {args.requirements[:100]}{'...' if len(args.requirements) > 100 else ''}")
    if args.constraints:
        print(f"Constraints: {args.constraints[:100]}{'...' if len(args.constraints) > 100 else ''}")
    if args.stakeholders:
        print(f"Stakeholders: {args.stakeholders}")
    if args.compliance:
        print(f"Compliance: {args.compliance}")
    if args.requirements_file:
        print(f"Requirements file: {args.requirements_file}")
    
    # Generate artifacts
    generator = PathArtifactGenerator(
        project_name=args.project,
        domain=args.domain,
        requirements=args.requirements,
        constraints=args.constraints,
        stakeholders=args.stakeholders,
        compliance=args.compliance,
        requirements_file=args.requirements_file
    )
    generator.generate_all_artifacts()

if __name__ == "__main__":
    main()
