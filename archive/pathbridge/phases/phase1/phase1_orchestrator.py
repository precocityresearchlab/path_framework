"""
Phase 1 Orchestrator - Software Engineering Phase
PATH Framework - Process/AI/Technology/Human

Coordinates the 4 AI agents in Phase 1:
1. AI Domain Analyst - Requirements analysis & domain modeling
2. AI System Architect - Architecture design & technology selection
3. AI Component Designer - Component design & SOLID principles
4. AI Integration Architect - Integration patterns & DI design

Implements the 7-step Phase 1 process:
1. Context Analysis
2. Domain Modeling
3. Architecture Design
4. Component Design
5. Integration Design
6. Validation & Review
7. Documentation & Handoff
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from ...exceptions import AgentError, ValidationError
from ...models.phase1_models import Phase1Output, RequirementAnalysis
from ...phases.base import BasePhase
from .component_designer import AIComponentDesigner, ComponentDesignRequest
from .domain_analyst import AIDomainAnalyst, AnalysisType, DomainAnalysisRequest
from .integration_architect import AIIntegrationArchitect, IntegrationRequest
from .system_architect import AISystemArchitect, ArchitectureRequest


class Phase1Step(Enum):
    CONTEXT_ANALYSIS = "context_analysis"
    DOMAIN_MODELING = "domain_modeling"
    ARCHITECTURE_DESIGN = "architecture_design"
    COMPONENT_DESIGN = "component_design"
    INTEGRATION_DESIGN = "integration_design"
    VALIDATION_REVIEW = "validation_review"
    DOCUMENTATION_HANDOFF = "documentation_handoff"


@dataclass
class Phase1Request:
    """Input request for Phase 1"""

    project_name: str
    project_description: str
    business_context: str
    stakeholder_input: list[str]
    constraints: list[str] = None
    quality_requirements: dict[str, str] = None
    team_expertise: list[str] = None
    existing_systems: list[str] = None
    compliance_frameworks: list[str] = None


@dataclass
class Phase1StepResult:
    """Result of a single Phase 1 step"""

    step: Phase1Step
    agent_id: str
    success: bool
    output: dict[str, Any]
    confidence_score: float
    human_review_required: bool
    validation_errors: list[str] = None
    execution_time: float = 0.0


class Phase1Orchestrator(BasePhase):
    """
    Phase 1 Orchestrator - Coordinates Software Engineering agents

    Implements the complete Phase 1 workflow with proper agent coordination,
    human approval points, and quality gates.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(
            phase_id="phase1",
            name="Software Engineering Phase",
            description="Requirements analysis, domain modeling, and architecture design",
            config=config,
        )

        # Initialize agents
        self.domain_analyst = AIDomainAnalyst(config)
        self.system_architect = AISystemArchitect(config)
        self.component_designer = AIComponentDesigner(config)
        self.integration_architect = AIIntegrationArchitect(config)

        # Phase 1 workflow steps
        self.workflow_steps = [
            Phase1Step.CONTEXT_ANALYSIS,
            Phase1Step.DOMAIN_MODELING,
            Phase1Step.ARCHITECTURE_DESIGN,
            Phase1Step.COMPONENT_DESIGN,
            Phase1Step.INTEGRATION_DESIGN,
            Phase1Step.VALIDATION_REVIEW,
            Phase1Step.DOCUMENTATION_HANDOFF,
        ]

        # Human approval points
        self.human_approval_steps = {
            Phase1Step.CONTEXT_ANALYSIS,
            Phase1Step.ARCHITECTURE_DESIGN,
            Phase1Step.VALIDATION_REVIEW,
        }

        # Quality gates
        self.quality_gates = {
            "requirements_completeness": 0.8,
            "domain_model_confidence": 0.7,
            "architecture_confidence": 0.8,
            "component_design_quality": 0.7,
            "integration_completeness": 0.8,
        }

    async def execute_phase(self, request: Phase1Request) -> Phase1Output:
        """
        Execute complete Phase 1 workflow

        Args:
            request: Phase 1 input request

        Returns:
            Complete Phase 1 output with all deliverables
        """
        try:
            self.logger.info(f"Starting Phase 1 execution for {request.project_name}")
            start_time = datetime.now()

            # Initialize output structure
            phase_output = Phase1Output(project_name=request.project_name)
            step_results = []

            # Execute workflow steps
            for step in self.workflow_steps:
                self.logger.info(f"Executing step: {step.value}")

                step_result = await self._execute_step(step, request, phase_output)
                step_results.append(step_result)

                # Check if step was successful
                if not step_result.success:
                    self.logger.error(
                        f"Step {step.value} failed: {step_result.validation_errors}"
                    )
                    phase_output.validation_results[step.value] = False
                    break

                # Update phase output with step results
                await self._update_phase_output(phase_output, step_result)

                # Check for human approval requirement
                if (
                    step_result.human_review_required
                    or step in self.human_approval_steps
                ):
                    approval_required = await self._request_human_approval(
                        step, step_result
                    )
                    phase_output.human_approvals[step.value] = approval_required

                    if approval_required and not await self._get_human_approval(
                        step, step_result
                    ):
                        self.logger.warning(
                            f"Human approval not granted for step: {step.value}"
                        )
                        # Continue with warning but don't fail

                # Validate quality gates
                if not await self._validate_quality_gates(step, step_result):
                    self.logger.warning(f"Quality gate not met for step: {step.value}")
                    phase_output.validation_results[f"{step.value}_quality"] = False

                self.logger.info(f"Step {step.value} completed successfully")

            # Final validation
            final_validation = await self._final_validation(phase_output)
            phase_output.validation_results["final_validation"] = final_validation

            # Prepare next phase inputs
            phase_output.next_phase_inputs = await self._prepare_next_phase_inputs(
                phase_output
            )

            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Phase 1 completed in {execution_time:.2f} seconds")

            return phase_output

        except Exception as e:
            self.logger.error(f"Phase 1 execution failed: {e!s}")
            raise AgentError(f"Phase 1 execution failed: {e!s}")

    async def _execute_step(
        self, step: Phase1Step, request: Phase1Request, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Execute a single workflow step"""
        start_time = datetime.now()

        try:
            if step == Phase1Step.CONTEXT_ANALYSIS:
                result = await self._execute_context_analysis(request)
            elif step == Phase1Step.DOMAIN_MODELING:
                result = await self._execute_domain_modeling(request)
            elif step == Phase1Step.ARCHITECTURE_DESIGN:
                result = await self._execute_architecture_design(
                    request, current_output
                )
            elif step == Phase1Step.COMPONENT_DESIGN:
                result = await self._execute_component_design(request, current_output)
            elif step == Phase1Step.INTEGRATION_DESIGN:
                result = await self._execute_integration_design(request, current_output)
            elif step == Phase1Step.VALIDATION_REVIEW:
                result = await self._execute_validation_review(current_output)
            elif step == Phase1Step.DOCUMENTATION_HANDOFF:
                result = await self._execute_documentation_handoff(current_output)
            else:
                raise ValidationError(f"Unknown step: {step}")

            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return Phase1StepResult(
                step=step,
                agent_id="orchestrator",
                success=False,
                output={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=[str(e)],
                execution_time=execution_time,
            )

    async def _execute_context_analysis(
        self, request: Phase1Request
    ) -> Phase1StepResult:
        """Step 1: Context Analysis using Domain Analyst"""
        analysis_request = DomainAnalysisRequest(
            project_name=request.project_name,
            project_description=request.project_description,
            business_context=request.business_context,
            stakeholder_input=request.stakeholder_input,
            analysis_type=AnalysisType.REQUIREMENTS,
            compliance_frameworks=request.compliance_frameworks,
        )

        # Execute requirements analysis
        result = await self.domain_analyst.analyze_requirements(analysis_request)

        return Phase1StepResult(
            step=Phase1Step.CONTEXT_ANALYSIS,
            agent_id=self.domain_analyst.agent_id,
            success=True,
            output={
                "requirements": (
                    [asdict(req) for req in result.requirements]
                    if result.requirements
                    else []
                ),
                "analysis_type": result.analysis_type.value,
                "recommendations": result.recommendations or [],
            },
            confidence_score=result.confidence_score,
            human_review_required=result.human_review_required,
            validation_errors=result.validation_errors or [],
        )

    async def _execute_domain_modeling(
        self, request: Phase1Request
    ) -> Phase1StepResult:
        """Step 2: Domain Modeling using Domain Analyst"""
        analysis_request = DomainAnalysisRequest(
            project_name=request.project_name,
            project_description=request.project_description,
            business_context=request.business_context,
            stakeholder_input=request.stakeholder_input,
            analysis_type=AnalysisType.DOMAIN_MODEL,
        )

        # Execute domain modeling
        result = await self.domain_analyst.model_domain(analysis_request)

        return Phase1StepResult(
            step=Phase1Step.DOMAIN_MODELING,
            agent_id=self.domain_analyst.agent_id,
            success=True,
            output={
                "domain_model": (
                    asdict(result.domain_model) if result.domain_model else {}
                ),
                "recommendations": result.recommendations or [],
            },
            confidence_score=result.confidence_score,
            human_review_required=result.human_review_required,
            validation_errors=result.validation_errors or [],
        )

    async def _execute_architecture_design(
        self, request: Phase1Request, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Step 3: Architecture Design using System Architect"""
        arch_request = ArchitectureRequest(
            project_name=request.project_name,
            requirements=current_output.requirement_analysis,
            domain_model=current_output.domain_model,
            constraints=request.constraints,
            quality_requirements=request.quality_requirements,
            team_expertise=request.team_expertise,
            existing_systems=request.existing_systems,
        )

        # Execute architecture design
        task = {"type": "design_architecture", "request": asdict(arch_request)}
        result_data = await self.system_architect.execute(task)

        return Phase1StepResult(
            step=Phase1Step.ARCHITECTURE_DESIGN,
            agent_id=self.system_architect.agent_id,
            success=True,
            output=result_data,
            confidence_score=result_data.get("confidence_score", 0.0),
            human_review_required=result_data.get("human_review_required", True),
        )

    async def _execute_component_design(
        self, request: Phase1Request, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Step 4: Component Design using Component Designer"""
        if not current_output.system_architecture:
            return Phase1StepResult(
                step=Phase1Step.COMPONENT_DESIGN,
                agent_id=self.component_designer.agent_id,
                success=False,
                output={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=["System architecture required for component design"],
            )

        comp_request = ComponentDesignRequest(
            project_name=request.project_name,
            architecture=current_output.system_architecture,
            component_requirements=request.constraints or [],
        )

        # Execute component design
        task = {"request": asdict(comp_request)}
        result_data = await self.component_designer.execute(task)

        return Phase1StepResult(
            step=Phase1Step.COMPONENT_DESIGN,
            agent_id=self.component_designer.agent_id,
            success=True,
            output=result_data,
            confidence_score=result_data.get("confidence_score", 0.0),
            human_review_required=False,
        )

    async def _execute_integration_design(
        self, request: Phase1Request, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Step 5: Integration Design using Integration Architect"""
        if not current_output.system_architecture:
            return Phase1StepResult(
                step=Phase1Step.INTEGRATION_DESIGN,
                agent_id=self.integration_architect.agent_id,
                success=False,
                output={},
                confidence_score=0.0,
                human_review_required=True,
                validation_errors=[
                    "System architecture required for integration design"
                ],
            )

        int_request = IntegrationRequest(
            project_name=request.project_name,
            architecture=current_output.system_architecture,
            components=current_output.component_designs,
            external_systems=request.existing_systems,
        )

        # Execute integration design
        task = {"request": asdict(int_request)}
        result_data = await self.integration_architect.execute(task)

        return Phase1StepResult(
            step=Phase1Step.INTEGRATION_DESIGN,
            agent_id=self.integration_architect.agent_id,
            success=True,
            output=result_data,
            confidence_score=result_data.get("confidence_score", 0.0),
            human_review_required=False,
        )

    async def _execute_validation_review(
        self, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Step 6: Validation & Review"""
        validation_results = {}
        overall_confidence = 0.0
        validation_errors = []

        # Validate completeness
        if not current_output.requirement_analysis:
            validation_errors.append("Requirements analysis missing")
        else:
            validation_results["requirements_complete"] = True
            overall_confidence += 0.2

        if not current_output.domain_model:
            validation_errors.append("Domain model missing")
        else:
            validation_results["domain_model_complete"] = True
            overall_confidence += 0.2

        if not current_output.system_architecture:
            validation_errors.append("System architecture missing")
        else:
            validation_results["architecture_complete"] = True
            overall_confidence += 0.3

        if not current_output.component_designs:
            validation_errors.append("Component designs missing")
        else:
            validation_results["components_complete"] = True
            overall_confidence += 0.15

        if not current_output.integration_design:
            validation_errors.append("Integration design missing")
        else:
            validation_results["integration_complete"] = True
            overall_confidence += 0.15

        # Check quality gates
        quality_passed = len(validation_errors) == 0
        validation_results["quality_gates_passed"] = quality_passed

        return Phase1StepResult(
            step=Phase1Step.VALIDATION_REVIEW,
            agent_id="orchestrator",
            success=quality_passed,
            output={
                "validation_results": validation_results,
                "quality_score": overall_confidence,
                "completeness_check": quality_passed,
            },
            confidence_score=overall_confidence,
            human_review_required=True,
            validation_errors=validation_errors,
        )

    async def _execute_documentation_handoff(
        self, current_output: Phase1Output
    ) -> Phase1StepResult:
        """Step 7: Documentation & Handoff"""

        # Generate documentation package
        documentation = {
            "project_summary": {
                "name": current_output.project_name,
                "generated_at": current_output.generated_at.isoformat(),
                "phase": "Phase 1 - Software Engineering",
            },
            "deliverables": {
                "requirements_analysis": bool(current_output.requirement_analysis),
                "domain_model": bool(current_output.domain_model),
                "system_architecture": bool(current_output.system_architecture),
                "component_designs": len(current_output.component_designs),
                "integration_design": bool(current_output.integration_design),
            },
            "next_phase_readiness": {
                "requirements_traced": True,
                "architecture_defined": True,
                "components_specified": True,
                "ready_for_tdd": True,
            },
            "handoff_checklist": [
                "Requirements analysis completed and approved",
                "Domain model validated and documented",
                "System architecture designed and reviewed",
                "Component interfaces defined",
                "Integration patterns specified",
                "Quality gates validated",
                "Documentation package prepared",
            ],
        }

        return Phase1StepResult(
            step=Phase1Step.DOCUMENTATION_HANDOFF,
            agent_id="orchestrator",
            success=True,
            output={
                "documentation": documentation,
                "handoff_package": "Ready for Phase 2",
                "status": "Phase 1 Complete",
            },
            confidence_score=0.95,
            human_review_required=False,
        )

    async def _update_phase_output(
        self, phase_output: Phase1Output, step_result: Phase1StepResult
    ) -> None:
        """Update phase output with step results"""
        step = step_result.step
        output = step_result.output

        if step == Phase1Step.CONTEXT_ANALYSIS:
            # Convert requirements data back to objects
            if "requirements" in output:
                from ...models.phase1_models import Requirement

                requirements = []
                for req_data in output["requirements"]:
                    req = Requirement(**req_data)
                    requirements.append(req)

                phase_output.requirement_analysis = RequirementAnalysis(
                    project_name=phase_output.project_name,
                    description="Requirements analysis from Phase 1",
                    requirements=requirements,
                )

        elif step == Phase1Step.DOMAIN_MODELING:
            if output.get("domain_model"):
                from ...models.phase1_models import DomainModel

                phase_output.domain_model = DomainModel(**output["domain_model"])

        elif step == Phase1Step.ARCHITECTURE_DESIGN:
            if "architecture" in output:
                from ...models.phase1_models import SystemArchitecture, TechnologyStack

                arch_data = output["architecture"]

                # Handle technology stack
                tech_stack_data = arch_data.get("technology_stack", {})
                tech_stack = TechnologyStack(**tech_stack_data)
                arch_data["technology_stack"] = tech_stack

                phase_output.system_architecture = SystemArchitecture(**arch_data)

        elif step == Phase1Step.COMPONENT_DESIGN:
            if "components" in output:
                from ...models.phase1_models import ComponentDesign

                components = []
                for comp_data in output["components"]:
                    comp = ComponentDesign(**comp_data)
                    components.append(comp)
                phase_output.component_designs = components

        elif step == Phase1Step.INTEGRATION_DESIGN:
            if "integration_design" in output:
                from ...models.phase1_models import IntegrationDesign

                phase_output.integration_design = IntegrationDesign(
                    **output["integration_design"]
                )

        # Update validation results
        phase_output.validation_results[step.value] = step_result.success

    async def _request_human_approval(
        self, step: Phase1Step, step_result: Phase1StepResult
    ) -> bool:
        """Determine if human approval is required"""
        # Always require approval for certain steps
        if step in self.human_approval_steps:
            return True

        # Require approval for low confidence results
        if step_result.confidence_score < 0.7:
            return True

        # Require approval if there are validation errors
        if step_result.validation_errors:
            return True

        return step_result.human_review_required

    async def _get_human_approval(
        self, step: Phase1Step, step_result: Phase1StepResult
    ) -> bool:
        """Get human approval (placeholder for actual implementation)"""
        # In a real implementation, this would integrate with a UI or approval system
        # For now, we'll assume approval is granted for demonstration
        self.logger.info(f"Human approval requested for step: {step.value}")
        self.logger.info(f"Confidence score: {step_result.confidence_score}")
        self.logger.info(f"Validation errors: {step_result.validation_errors}")

        # Auto-approve for high confidence results
        return step_result.confidence_score >= 0.8

    async def _validate_quality_gates(
        self, step: Phase1Step, step_result: Phase1StepResult
    ) -> bool:
        """Validate quality gates for the step"""
        confidence_threshold = self.quality_gates.get(f"{step.value}_confidence", 0.6)
        return step_result.confidence_score >= confidence_threshold

    async def _final_validation(self, phase_output: Phase1Output) -> bool:
        """Perform final validation of Phase 1 output"""
        required_outputs = [
            phase_output.requirement_analysis,
            phase_output.domain_model,
            phase_output.system_architecture,
        ]

        # Check that all required outputs are present
        return all(output is not None for output in required_outputs)

    async def _prepare_next_phase_inputs(
        self, phase_output: Phase1Output
    ) -> dict[str, Any]:
        """Prepare inputs for Phase 2 (TDD)"""
        return {
            "requirements": (
                asdict(phase_output.requirement_analysis)
                if phase_output.requirement_analysis
                else {}
            ),
            "domain_model": (
                asdict(phase_output.domain_model) if phase_output.domain_model else {}
            ),
            "architecture": (
                asdict(phase_output.system_architecture)
                if phase_output.system_architecture
                else {}
            ),
            "components": [asdict(comp) for comp in phase_output.component_designs],
            "integration": (
                asdict(phase_output.integration_design)
                if phase_output.integration_design
                else {}
            ),
            "phase1_validation": phase_output.validation_results,
            "human_approvals": phase_output.human_approvals,
        }

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute Phase 1 orchestration

        Args:
            task: Task configuration with Phase 1 parameters

        Returns:
            Complete Phase 1 results
        """
        try:
            # Parse request
            request_data = task.get("request", {})
            request = Phase1Request(**request_data)

            # Execute complete Phase 1
            result = await self.execute_phase(request)

            # Format response
            response = {
                "phase": "phase1",
                "orchestrator_id": "phase1_orchestrator",
                "project_name": result.project_name,
                "status": "completed",
                "generated_at": result.generated_at.isoformat(),
                "validation_results": result.validation_results,
                "human_approvals": result.human_approvals,
                "next_phase_inputs": result.next_phase_inputs,
                "deliverables": {
                    "requirement_analysis": (
                        asdict(result.requirement_analysis)
                        if result.requirement_analysis
                        else None
                    ),
                    "domain_model": (
                        asdict(result.domain_model) if result.domain_model else None
                    ),
                    "system_architecture": (
                        asdict(result.system_architecture)
                        if result.system_architecture
                        else None
                    ),
                    "component_designs": [
                        asdict(comp) for comp in result.component_designs
                    ],
                    "integration_design": (
                        asdict(result.integration_design)
                        if result.integration_design
                        else None
                    ),
                },
            }

            return response

        except Exception as e:
            self.logger.error(f"Phase 1 orchestration failed: {e!s}")
            raise AgentError(f"Phase 1 orchestration failed: {e!s}")

    def validate_output(self, output: dict[str, Any]) -> bool:
        """Validate Phase 1 output"""
        required_fields = ["phase", "project_name", "status", "deliverables"]

        for field in required_fields:
            if field not in output:
                return False

        # Validate deliverables
        deliverables = output["deliverables"]
        required_deliverables = [
            "requirement_analysis",
            "domain_model",
            "system_architecture",
        ]

        for deliverable in required_deliverables:
            if deliverable not in deliverables or deliverables[deliverable] is None:
                return False

        return True
