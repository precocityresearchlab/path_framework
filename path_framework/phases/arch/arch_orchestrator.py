"""
Architecture Phase Orchestrator
PATH Framework - Process/AI/Technology/Human

Coordinates all PATH components for the Architecture phase:
- Process: Workflows, quality gates, validation
- AI: Domain analysis, system architecture, component design, integration
- Technology: Architecture tools, design patterns, modeling frameworks  
- Human: Oversight, approval gates, creative input

Implements the 7-step Architecture process:
1. Context Analysis
2. Domain Modeling  
3. Architecture Design
4. Component Design
5. Integration Design
6. Validation & Review
7. Documentation & Handoff
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging

from ..base import BasePhase
from ...exceptions import PathFrameworkError
from ...models.arch_models import (
    RequirementAnalysis, 
    DomainModel, 
    SystemArchitecture,
    BusinessRule,
    ComponentDesign,
    IntegrationDesign
)

# Import PATH pillar components
from .process.workflows import ArchitectureWorkflow
from .process.quality_gates import ArchitectureQualityGates
from .process.validation import ArchitectureValidation

from .ai.domain_analyst import AIDomainAnalyst, DomainAnalysisRequest, AnalysisType
from .ai.system_architect import AISystemArchitect, ArchitectureRequest
from .ai.component_designer import AIComponentDesigner, ComponentDesignRequest
from .ai.integration_architect import AIIntegrationArchitect, IntegrationRequest

from .technology import ArchitectureTools, DesignPatterns, ModelingFrameworks

from .human import HumanOversight, ApprovalGates, CreativeInput


class ArchStep(Enum):
    """Architecture phase steps"""
    CONTEXT_ANALYSIS = "context_analysis"
    DOMAIN_MODELING = "domain_modeling"
    ARCHITECTURE_DESIGN = "architecture_design"
    COMPONENT_DESIGN = "component_design"
    INTEGRATION_DESIGN = "integration_design"
    VALIDATION_REVIEW = "validation_review"
    DOCUMENTATION_HANDOFF = "documentation_handoff"


@dataclass
class ArchRequest:
    """Input request for Architecture phase"""
    project_name: str
    project_description: str
    business_context: str
    stakeholder_input: List[str] = None
    constraints: List[str] = None
    quality_requirements: Dict[str, str] = None
    team_expertise: List[str] = None
    existing_documentation: List[str] = None
    compliance_frameworks: List[str] = None


@dataclass
class ArchStepResult:
    """Result from a single architecture step"""
    step: ArchStep
    success: bool
    outputs: Dict[str, Any]
    confidence_score: float
    human_review_required: bool
    recommendations: List[str] = None
    validation_errors: List[str] = None
    execution_time: float = 0.0


@dataclass
class ArchOutput:
    """Complete output from Architecture phase"""
    project_name: str
    requirements_analysis: Optional[RequirementAnalysis] = None
    domain_model: Optional[DomainModel] = None
    system_architecture: Optional[SystemArchitecture] = None
    component_designs: List[ComponentDesign] = None
    integration_design: Optional[IntegrationDesign] = None
    architecture_decisions: List[Dict[str, Any]] = None
    validation_results: Dict[str, bool] = None
    human_approvals: Dict[str, bool] = None
    next_phase_inputs: Dict[str, Any] = None
    recommendations: List[str] = None
    created_at: datetime = None


class ArchOrchestrator(BasePhase):
    """
    Architecture Phase Orchestrator
    
    Coordinates Process/AI/Technology/Human components to execute
    the complete architecture design workflow.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            phase_name="Architecture",
            phase_number=1,
            config=config
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Initialize PATH components
        self._init_process_components()
        self._init_ai_components()
        self._init_technology_components()
        self._init_human_components()
        
        # Track phase state
        self.current_step = None
        self.step_results = {}
        self.overall_confidence = 0.0
    
    def _init_process_components(self):
        """Initialize Process pillar components"""
        self.workflow = ArchitectureWorkflow()
        self.quality_gates = ArchitectureQualityGates()
        self.validation = ArchitectureValidation()
    
    def _init_ai_components(self):
        """Initialize AI pillar components"""
        self.domain_analyst = AIDomainAnalyst(self.config)
        self.system_architect = AISystemArchitect(self.config)
        self.component_designer = AIComponentDesigner(self.config)
        self.integration_architect = AIIntegrationArchitect(self.config)
    
    def _init_technology_components(self):
        """Initialize Technology pillar components"""
        self.arch_tools = ArchitectureTools()
        self.design_patterns = DesignPatterns()
        self.modeling_frameworks = ModelingFrameworks()
    
    def _init_human_components(self):
        """Initialize Human pillar components"""
        self.human_oversight = HumanOversight()
        self.approval_gates = ApprovalGates(self.human_oversight)
        self.creative_input = CreativeInput()

    async def execute_phase(self, request: ArchRequest) -> ArchOutput:
        """
        Execute complete Architecture phase
        
        Args:
            request: Architecture phase input request
            
        Returns:
            Complete architecture phase output
        """
        try:
            self.logger.info(f"Starting Architecture phase for {request.project_name}")
            
            # Initialize phase output
            phase_output = ArchOutput(
                project_name=request.project_name,
                created_at=datetime.now()
            )
            
            # Execute each step in sequence
            for step in ArchStep:
                self.current_step = step
                self.logger.info(f"Executing step: {step.value}")
                
                step_result = await self._execute_step(step, request, phase_output)
                self.step_results[step] = step_result
                
                if not step_result.success:
                    self.logger.error(f"Step {step.value} failed")
                    if step_result.validation_errors:
                        raise PathFrameworkError(f"Step {step.value} validation failed: {step_result.validation_errors}")
                    else:
                        raise PathFrameworkError(f"Step {step.value} execution failed")
                
                # Update phase output with step results
                await self._update_phase_output(phase_output, step_result)
                
                # Check if human review is required
                if step_result.human_review_required:
                    self.logger.info(f"Step {step.value} requires human review")
                    await self._request_human_review(step, step_result)
            
            # Final validation
            final_validation = await self._final_validation(phase_output)
            if not final_validation:
                raise PathFrameworkError("Final phase validation failed")
            
            # Prepare inputs for next phase
            phase_output.next_phase_inputs = await self._prepare_next_phase_inputs(phase_output)
            
            # Calculate overall confidence
            self.overall_confidence = self._calculate_overall_confidence()
            
            self.logger.info(f"Architecture phase completed successfully with confidence: {self.overall_confidence}")
            return phase_output
            
        except Exception as e:
            self.logger.error(f"Architecture phase execution failed: {str(e)}")
            raise PathFrameworkError(f"Architecture phase execution failed: {str(e)}")

    async def _execute_step(self, step: ArchStep, request: ArchRequest, current_output: ArchOutput) -> ArchStepResult:
        """Execute a single architecture step"""
        start_time = datetime.now()
        
        try:
            if step == ArchStep.CONTEXT_ANALYSIS:
                result = await self._execute_context_analysis(request)
            elif step == ArchStep.DOMAIN_MODELING:
                result = await self._execute_domain_modeling(request, current_output)
            elif step == ArchStep.ARCHITECTURE_DESIGN:
                result = await self._execute_architecture_design(request, current_output)
            elif step == ArchStep.COMPONENT_DESIGN:
                result = await self._execute_component_design(request, current_output)
            elif step == ArchStep.INTEGRATION_DESIGN:
                result = await self._execute_integration_design(request, current_output)
            elif step == ArchStep.VALIDATION_REVIEW:
                result = await self._execute_validation_review(current_output)
            elif step == ArchStep.DOCUMENTATION_HANDOFF:
                result = await self._execute_documentation_handoff(current_output)
            else:
                raise PathFrameworkError(f"Unknown step: {step}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            
            return result
            
        except Exception as e:
            self.logger.error(f"Step {step.value} execution failed: {str(e)}")
            return ArchStepResult(
                step=step,
                success=False,
                outputs={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=[str(e)],
                execution_time=(datetime.now() - start_time).total_seconds()
            )

    async def _execute_context_analysis(self, request: ArchRequest) -> ArchStepResult:
        """Execute context analysis step - Process + AI coordination"""
        # Process: Initialize workflow
        workflow_context = await self.workflow.initialize_context(
            request.project_name,
            request.project_description,
            request.business_context
        )
        
        # AI: Domain analyst for requirements analysis
        domain_request = DomainAnalysisRequest(
            project_name=request.project_name,
            project_description=request.project_description,
            business_context=request.business_context,
            stakeholder_input=request.stakeholder_input or [],
            analysis_type=AnalysisType.REQUIREMENTS,
            existing_documentation=request.existing_documentation or [],
            compliance_frameworks=request.compliance_frameworks or []
        )
        
        analysis_result = await self.domain_analyst.analyze_requirements(domain_request)
        
        # Process: Quality gate validation
        quality_check = await self.quality_gates.validate_requirements_analysis(
            analysis_result.requirements,
            analysis_result.confidence_score
        )
        
        return ArchStepResult(
            step=ArchStep.CONTEXT_ANALYSIS,
            success=quality_check["passed"],
            outputs={
                "workflow_context": workflow_context,
                "requirements_analysis": analysis_result.requirements,
                "confidence_score": analysis_result.confidence_score
            },
            confidence_score=analysis_result.confidence_score,
            human_review_required=analysis_result.human_review_required,
            recommendations=analysis_result.recommendations,
            validation_errors=quality_check.get("errors", [])
        )

    async def _execute_domain_modeling(self, request: ArchRequest, current_output: ArchOutput) -> ArchStepResult:
        """Execute domain modeling step - AI + Technology coordination"""
        # AI: Domain analyst for domain modeling
        domain_request = DomainAnalysisRequest(
            project_name=request.project_name,
            project_description=request.project_description,
            business_context=request.business_context,
            stakeholder_input=request.stakeholder_input or [],
            analysis_type=AnalysisType.DOMAIN_MODEL
        )
        
        domain_result = await self.domain_analyst.model_domain(domain_request)
        
        # Technology: Generate domain model artifacts
        if domain_result.domain_model:
            domain_entities = [
                {
                    "name": entity.name,
                    "description": entity.description,
                    "attributes": entity.attributes,
                    "behaviors": entity.behaviors
                }
                for entity in domain_result.domain_model.entities
            ]
            
            # Generate modeling artifacts
            plantuml_diagram = self.modeling_frameworks.export_to_plantuml({
                "entities": domain_entities
            })
            
            c4_model = self.modeling_frameworks.generate_c4_model(
                current_output.system_architecture if current_output.system_architecture else None
            )
        
        return ArchStepResult(
            step=ArchStep.DOMAIN_MODELING,
            success=domain_result.domain_model is not None,
            outputs={
                "domain_model": domain_result.domain_model,
                "plantuml_diagram": plantuml_diagram if domain_result.domain_model else None,
                "c4_model": c4_model if domain_result.domain_model else None
            },
            confidence_score=domain_result.confidence_score,
            human_review_required=domain_result.human_review_required,
            recommendations=domain_result.recommendations
        )

    async def _execute_architecture_design(self, request: ArchRequest, current_output: ArchOutput) -> ArchStepResult:
        """Execute architecture design step - AI + Technology + Human coordination"""
        # AI: System architect for architecture design
        arch_request = ArchitectureRequest(
            project_name=request.project_name,
            requirements=current_output.requirements_analysis,
            domain_model=current_output.domain_model,
            constraints=request.constraints,
            quality_requirements=request.quality_requirements,
            team_expertise=request.team_expertise
        )
        
        arch_result = await self.system_architect.design_architecture(arch_request)
        
        # Technology: Generate architecture artifacts
        if arch_result.architecture:
            # Get architecture pattern recommendations
            pattern_recommendations = self.arch_tools.recommend_patterns({
                "team_size": len(request.team_expertise) if request.team_expertise else 1,
                "complexity": "high" if len(request.constraints or []) > 3 else "medium"
            })
            
            # Generate architecture diagram configuration
            diagram_config = self.arch_tools.generate_architecture_diagram_config(
                arch_result.architecture
            )
            
            # Assess technology stack
            tech_assessment = self.arch_tools.assess_technology_stack({
                "team_experience": "medium",
                "performance": "medium",
                "enterprise": bool(request.compliance_frameworks)
            })
        
        # Human: Request architecture approval
        approval_request_id = self.human_oversight.request_approval(
            title=f"Architecture Design for {request.project_name}",
            description="Complete system architecture including patterns and technology stack",
            artifact_type="architecture",
            artifact_data=asdict(arch_result.architecture) if arch_result.architecture else {},
            stakeholder_roles=["ARCHITECT", "TECH_LEAD"],
            priority="high"
        )
        
        return ArchStepResult(
            step=ArchStep.ARCHITECTURE_DESIGN,
            success=arch_result.architecture is not None,
            outputs={
                "system_architecture": arch_result.architecture,
                "architecture_decisions": arch_result.decisions,
                "pattern_recommendations": pattern_recommendations if arch_result.architecture else [],
                "diagram_config": diagram_config if arch_result.architecture else {},
                "tech_assessment": tech_assessment if arch_result.architecture else {},
                "approval_request_id": approval_request_id
            },
            confidence_score=arch_result.confidence_score,
            human_review_required=True,  # Always require human review for architecture
            recommendations=arch_result.recommendations
        )

    async def _execute_component_design(self, request: ArchRequest, current_output: ArchOutput) -> ArchStepResult:
        """Execute component design step - AI + Technology coordination"""
        if not current_output.system_architecture:
            return ArchStepResult(
                step=ArchStep.COMPONENT_DESIGN,
                success=False,
                outputs={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=["System architecture required for component design"]
            )
        
        # AI: Component designer
        component_request = ComponentDesignRequest(
            project_name=request.project_name,
            system_architecture=current_output.system_architecture,
            domain_model=current_output.domain_model,
            design_principles=["SOLID", "DRY", "KISS"]
        )
        
        component_result = await self.component_designer.design_components(component_request)
        
        # Technology: Apply design patterns
        if component_result.components:
            # Get design pattern recommendations
            pattern_recommendations = []
            for component in component_result.components:
                patterns = self.design_patterns.recommend_patterns(
                    f"Component for {component.name} with responsibilities: {component.responsibilities}"
                )
                pattern_recommendations.extend(patterns)
        
        return ArchStepResult(
            step=ArchStep.COMPONENT_DESIGN,
            success=bool(component_result.components),
            outputs={
                "component_designs": component_result.components,
                "design_patterns": pattern_recommendations if component_result.components else []
            },
            confidence_score=component_result.confidence_score,
            human_review_required=component_result.human_review_required,
            recommendations=component_result.recommendations
        )

    async def _execute_integration_design(self, request: ArchRequest, current_output: ArchOutput) -> ArchStepResult:
        """Execute integration design step - AI coordination"""
        if not current_output.system_architecture or not current_output.component_designs:
            return ArchStepResult(
                step=ArchStep.INTEGRATION_DESIGN,
                success=False,
                outputs={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=["System architecture and component designs required"]
            )
        
        # AI: Integration architect
        integration_request = IntegrationRequest(
            project_name=request.project_name,
            system_architecture=current_output.system_architecture,
            components=current_output.component_designs,
            integration_requirements=request.quality_requirements or {}
        )
        
        integration_result = await self.integration_architect.design_integration(integration_request)
        
        return ArchStepResult(
            step=ArchStep.INTEGRATION_DESIGN,
            success=integration_result.integration_design is not None,
            outputs={
                "integration_design": integration_result.integration_design
            },
            confidence_score=integration_result.confidence_score,
            human_review_required=integration_result.human_review_required,
            recommendations=integration_result.recommendations
        )

    async def _execute_validation_review(self, current_output: ArchOutput) -> ArchStepResult:
        """Execute validation and review step - Process + Human coordination"""
        # Process: Comprehensive validation
        validation_results = await self.validation.validate_complete_architecture(
            current_output.requirements_analysis,
            current_output.domain_model,
            current_output.system_architecture,
            current_output.component_designs,
            current_output.integration_design
        )
        
        # Human: Schedule architecture review session
        if not validation_results["all_valid"]:
            review_session_id = self.creative_input.schedule_creative_session(
                title="Architecture Review Session",
                objective="Review and improve architecture design",
                facilitator="lead_architect",
                participants=["system_architect", "tech_lead", "senior_developer"],
                session_type="architecture_review"
            )
        
        return ArchStepResult(
            step=ArchStep.VALIDATION_REVIEW,
            success=validation_results["all_valid"],
            outputs={
                "validation_results": validation_results,
                "review_session_id": review_session_id if not validation_results["all_valid"] else None
            },
            confidence_score=validation_results.get("confidence", 0.8),
            human_review_required=not validation_results["all_valid"],
            validation_errors=validation_results.get("errors", [])
        )

    async def _execute_documentation_handoff(self, current_output: ArchOutput) -> ArchStepResult:
        """Execute documentation and handoff step - Technology + Process coordination"""
        # Technology: Generate comprehensive documentation
        documentation = {
            "architecture_overview": {
                "project_name": current_output.project_name,
                "architecture_pattern": current_output.system_architecture.pattern.value if current_output.system_architecture else "unknown",
                "technology_stack": asdict(current_output.system_architecture.technology_stack) if current_output.system_architecture else {},
                "components_count": len(current_output.component_designs) if current_output.component_designs else 0
            },
            "design_decisions": current_output.architecture_decisions or [],
            "next_phase_readiness": True
        }
        
        # Process: Prepare handoff package
        handoff_package = await self.workflow.prepare_phase_handoff(
            current_output.requirements_analysis,
            current_output.system_architecture,
            current_output.component_designs,
            current_output.integration_design
        )
        
        return ArchStepResult(
            step=ArchStep.DOCUMENTATION_HANDOFF,
            success=True,
            outputs={
                "documentation": documentation,
                "handoff_package": handoff_package
            },
            confidence_score=0.9,
            human_review_required=False
        )

    async def _update_phase_output(self, phase_output: ArchOutput, step_result: ArchStepResult) -> None:
        """Update phase output with step results"""
        if step_result.step == ArchStep.CONTEXT_ANALYSIS:
            phase_output.requirements_analysis = step_result.outputs.get("requirements_analysis")
        elif step_result.step == ArchStep.DOMAIN_MODELING:
            phase_output.domain_model = step_result.outputs.get("domain_model")
        elif step_result.step == ArchStep.ARCHITECTURE_DESIGN:
            phase_output.system_architecture = step_result.outputs.get("system_architecture")
            phase_output.architecture_decisions = step_result.outputs.get("architecture_decisions", [])
        elif step_result.step == ArchStep.COMPONENT_DESIGN:
            phase_output.component_designs = step_result.outputs.get("component_designs", [])
        elif step_result.step == ArchStep.INTEGRATION_DESIGN:
            phase_output.integration_design = step_result.outputs.get("integration_design")
        elif step_result.step == ArchStep.VALIDATION_REVIEW:
            phase_output.validation_results = step_result.outputs.get("validation_results", {})
        elif step_result.step == ArchStep.DOCUMENTATION_HANDOFF:
            phase_output.next_phase_inputs = step_result.outputs.get("handoff_package", {})

    async def _request_human_review(self, step: ArchStep, step_result: ArchStepResult) -> None:
        """Request human review for a step"""
        self.logger.info(f"Requesting human review for step: {step.value}")
        # In a real implementation, this would integrate with notification systems
        # For now, we'll log the request
        
    async def _final_validation(self, phase_output: ArchOutput) -> bool:
        """Final validation of complete phase output"""
        required_outputs = [
            phase_output.requirements_analysis,
            phase_output.domain_model,
            phase_output.system_architecture
        ]
        
        return all(output is not None for output in required_outputs)

    async def _prepare_next_phase_inputs(self, phase_output: ArchOutput) -> Dict[str, Any]:
        """Prepare inputs for the next phase (TDD)"""
        return {
            "architecture_design": asdict(phase_output.system_architecture) if phase_output.system_architecture else {},
            "component_specifications": [asdict(comp) for comp in phase_output.component_designs] if phase_output.component_designs else [],
            "integration_requirements": asdict(phase_output.integration_design) if phase_output.integration_design else {},
            "quality_attributes": phase_output.system_architecture.quality_attributes if phase_output.system_architecture else {},
            "technology_stack": asdict(phase_output.system_architecture.technology_stack) if phase_output.system_architecture else {},
            "architecture_decisions": phase_output.architecture_decisions or []
        }

    def _calculate_overall_confidence(self) -> float:
        """Calculate overall phase confidence"""
        if not self.step_results:
            return 0.0
        
        confidences = [result.confidence_score for result in self.step_results.values()]
        return sum(confidences) / len(confidences)

    async def get_phase_status(self) -> Dict[str, Any]:
        """Get current phase status"""
        return {
            "phase_name": "Architecture",
            "current_step": self.current_step.value if self.current_step else None,
            "completed_steps": [step.value for step, result in self.step_results.items() if result.success],
            "overall_confidence": self.overall_confidence,
            "step_results": {
                step.value: {
                    "success": result.success,
                    "confidence": result.confidence_score,
                    "human_review_required": result.human_review_required,
                    "execution_time": result.execution_time
                }
                for step, result in self.step_results.items()
            }
        }
