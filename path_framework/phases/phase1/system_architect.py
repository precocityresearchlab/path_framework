"""
AI System Architect - Phase 1 Agent
PATH Framework - Process/AI/Technology/Human

Responsible for:
- Architecture design and pattern selection
- Technology stack selection and validation
- Quality attributes definition and validation
- System-level design decisions

Decision Authority: Human approval required for architectural decisions
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

from ...agents.base import BaseAgent
from ...exceptions import ValidationError, AgentError
from ...models.phase1_models import (
    SystemArchitecture,
    TechnologyStack,
    ArchitecturePattern,
    RequirementAnalysis,
    DomainModel
)


class ArchitectureDecisionType(Enum):
    PATTERN_SELECTION = "pattern_selection"
    TECHNOLOGY_STACK = "technology_stack"
    QUALITY_ATTRIBUTES = "quality_attributes"
    SYSTEM_STRUCTURE = "system_structure"
    INTEGRATION_STRATEGY = "integration_strategy"


@dataclass
class ArchitectureRequest:
    """Request structure for architecture design"""
    project_name: str
    requirements: RequirementAnalysis
    domain_model: Optional[DomainModel] = None
    constraints: List[str] = None
    quality_requirements: Dict[str, str] = None
    existing_systems: List[str] = None
    team_expertise: List[str] = None
    budget_constraints: str = ""
    timeline_constraints: str = ""


@dataclass
class ArchitectureDecision:
    """Architecture decision record"""
    id: str
    title: str
    decision_type: ArchitectureDecisionType
    description: str
    rationale: str
    alternatives_considered: List[str]
    consequences: List[str]
    confidence_score: float
    human_approval_required: bool = True


@dataclass
class ArchitectureResult:
    """Result structure for architecture design"""
    architecture: SystemArchitecture
    decisions: List[ArchitectureDecision]
    confidence_score: float
    validation_results: Dict[str, bool]
    recommendations: List[str]
    human_review_required: bool = True
    risk_assessment: Dict[str, str] = None


class AISystemArchitect(BaseAgent):
    """
    AI System Architect - Specialized in architecture design and technology selection
    
    Decision Authority: Human approval required for architectural decisions
    Capabilities:
    - Architecture pattern recommendation and validation
    - Technology stack selection based on requirements
    - Quality attributes analysis and design
    - System structure and component organization
    - Integration strategy development
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            agent_id="ai_system_architect",
            name="AI System Architect",
            specialization="Architecture design & technology selection",
            decision_authority="Human approval",
            phase=1,
            config=config
        )
        
        # Architecture knowledge base
        self.architecture_patterns = {
            ArchitecturePattern.MICROSERVICES: {
                "description": "Distributed architecture with independent services",
                "strengths": ["Scalability", "Technology diversity", "Independent deployment"],
                "weaknesses": ["Complexity", "Network overhead", "Data consistency"],
                "use_cases": ["Large scale", "Multiple teams", "High availability"]
            },
            ArchitecturePattern.MONOLITHIC: {
                "description": "Single deployable unit architecture",
                "strengths": ["Simplicity", "Easy debugging", "Single deployment"],
                "weaknesses": ["Scaling limitations", "Technology lock-in", "Team bottlenecks"],
                "use_cases": ["Small to medium projects", "Single team", "Rapid prototyping"]
            },
            ArchitecturePattern.LAYERED: {
                "description": "Hierarchical layered architecture",
                "strengths": ["Separation of concerns", "Reusability", "Testability"],
                "weaknesses": ["Performance overhead", "Layer isolation challenges"],
                "use_cases": ["Enterprise applications", "Clear domain separation"]
            },
            ArchitecturePattern.HEXAGONAL: {
                "description": "Ports and adapters architecture",
                "strengths": ["Testability", "External dependency isolation", "Clean boundaries"],
                "weaknesses": ["Initial complexity", "Learning curve"],
                "use_cases": ["Domain-driven design", "Clean architecture needs"]
            },
            ArchitecturePattern.EVENT_DRIVEN: {
                "description": "Event-based communication architecture",
                "strengths": ["Loose coupling", "Scalability", "Real-time processing"],
                "weaknesses": ["Event ordering", "Debugging complexity", "Eventual consistency"],
                "use_cases": ["Real-time systems", "High throughput", "Reactive systems"]
            },
            ArchitecturePattern.SERVERLESS: {
                "description": "Function-as-a-Service architecture",
                "strengths": ["Auto-scaling", "Cost efficiency", "No server management"],
                "weaknesses": ["Vendor lock-in", "Cold starts", "State management"],
                "use_cases": ["Event processing", "Variable workloads", "Cost optimization"]
            }
        }
        
        # Technology stacks knowledge
        self.technology_recommendations = {
            "web_applications": {
                "frontend": ["React", "Vue.js", "Angular", "Svelte"],
                "backend": ["Node.js", "Python/FastAPI", "Java/Spring", "C#/.NET"],
                "database": ["PostgreSQL", "MongoDB", "Redis"],
                "deployment": ["Docker", "Kubernetes", "AWS/Azure/GCP"]
            },
            "mobile_applications": {
                "native_ios": ["Swift", "SwiftUI"],
                "native_android": ["Kotlin", "Jetpack Compose"],
                "cross_platform": ["React Native", "Flutter", "Xamarin"],
                "backend": ["Node.js", "Python", "Java", "C#"]
            },
            "data_processing": {
                "languages": ["Python", "Scala", "Java", "R"],
                "frameworks": ["Apache Spark", "Pandas", "Dask", "Apache Flink"],
                "databases": ["PostgreSQL", "ClickHouse", "Cassandra", "InfluxDB"],
                "orchestration": ["Apache Airflow", "Prefect", "Dagster"]
            },
            "real_time_systems": {
                "languages": ["C++", "Rust", "Go", "Java"],
                "frameworks": ["Akka", "Tokio", "Go Channels"],
                "messaging": ["Apache Kafka", "RabbitMQ", "Redis Streams"],
                "monitoring": ["Prometheus", "Grafana", "DataDog"]
            }
        }
        
        # Quality attributes
        self.quality_attributes = {
            "performance": ["Response time", "Throughput", "Resource utilization"],
            "scalability": ["Horizontal scaling", "Vertical scaling", "Load handling"],
            "availability": ["Uptime", "Fault tolerance", "Disaster recovery"],
            "security": ["Authentication", "Authorization", "Data protection"],
            "maintainability": ["Code quality", "Documentation", "Testability"],
            "usability": ["User experience", "Accessibility", "Responsiveness"]
        }

    async def design_architecture(self, request: ArchitectureRequest) -> ArchitectureResult:
        """
        Design system architecture based on requirements and constraints
        
        Args:
            request: Architecture design request
            
        Returns:
            Complete architecture design with decisions and recommendations
        """
        try:
            self.logger.info(f"Starting architecture design for {request.project_name}")
            
            # Validate input
            if not request.requirements:
                raise ValidationError("Requirements are required for architecture design")
            
            # Analyze requirements for architecture needs
            architecture_needs = await self._analyze_architecture_needs(request)
            
            # Select architecture pattern
            pattern_decision = await self._select_architecture_pattern(request, architecture_needs)
            
            # Design technology stack
            tech_stack_decision = await self._design_technology_stack(request, pattern_decision)
            
            # Define quality attributes
            quality_decisions = await self._define_quality_attributes(request)
            
            # Create system structure
            structure_decision = await self._design_system_structure(request, pattern_decision)
            
            # Compile all decisions
            decisions = [pattern_decision, tech_stack_decision] + quality_decisions + [structure_decision]
            
            # Create complete architecture
            architecture = await self._create_system_architecture(request, decisions)
            
            # Validate architecture
            validation_results = await self._validate_architecture(architecture, request)
            
            # Calculate overall confidence
            confidence = self._calculate_architecture_confidence(decisions, validation_results)
            
            # Generate recommendations
            recommendations = await self._generate_architecture_recommendations(
                architecture, decisions, validation_results
            )
            
            # Assess risks
            risk_assessment = await self._assess_architecture_risks(architecture, decisions)
            
            result = ArchitectureResult(
                architecture=architecture,
                decisions=decisions,
                confidence_score=confidence,
                validation_results=validation_results,
                recommendations=recommendations,
                human_review_required=True,  # Always require human review for architecture
                risk_assessment=risk_assessment
            )
            
            self.logger.info(f"Architecture design completed with {len(decisions)} decisions")
            return result
            
        except Exception as e:
            self.logger.error(f"Architecture design failed: {str(e)}")
            raise AgentError(f"Architecture design failed: {str(e)}")

    async def evaluate_technology_stack(self, request: ArchitectureRequest) -> ArchitectureResult:
        """
        Evaluate and recommend technology stack
        
        Args:
            request: Architecture request with technology constraints
            
        Returns:
            Technology stack recommendations and analysis
        """
        try:
            self.logger.info(f"Evaluating technology stack for {request.project_name}")
            
            # Analyze technology requirements
            tech_requirements = await self._analyze_technology_requirements(request)
            
            # Generate technology recommendations
            tech_decision = await self._design_technology_stack(request, None)
            
            # Create minimal architecture for tech stack evaluation
            architecture = SystemArchitecture(
                name=f"{request.project_name}_tech_architecture",
                description="Technology stack architecture",
                technology_stack=tech_decision.description,  # Will be created in _design_technology_stack
                constraints=request.constraints or []
            )
            
            # Validate technology choices
            validation_results = await self._validate_technology_stack(tech_decision, request)
            
            result = ArchitectureResult(
                architecture=architecture,
                decisions=[tech_decision],
                confidence_score=tech_decision.confidence_score,
                validation_results=validation_results,
                recommendations=await self._generate_technology_recommendations(tech_decision, validation_results),
                human_review_required=True
            )
            
            self.logger.info("Technology stack evaluation completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Technology stack evaluation failed: {str(e)}")
            raise AgentError(f"Technology stack evaluation failed: {str(e)}")

    # Private helper methods
    async def _analyze_architecture_needs(self, request: ArchitectureRequest) -> Dict[str, Any]:
        """Analyze requirements to determine architecture needs"""
        needs = {
            "scalability_requirements": "medium",
            "performance_requirements": "medium", 
            "complexity_level": "medium",
            "team_size": "small",
            "domain_complexity": "medium"
        }
        
        # Analyze requirements for architecture drivers
        if request.requirements and request.requirements.requirements:
            # Check for scalability needs
            scalability_reqs = [req for req in request.requirements.requirements 
                             if "scale" in req.description.lower() or "load" in req.description.lower()]
            if len(scalability_reqs) > 2:
                needs["scalability_requirements"] = "high"
            
            # Check for performance needs
            performance_reqs = [req for req in request.requirements.requirements
                              if "performance" in req.description.lower() or "fast" in req.description.lower()]
            if len(performance_reqs) > 1:
                needs["performance_requirements"] = "high"
            
            # Assess overall complexity
            complex_reqs = [req for req in request.requirements.requirements
                           if req.complexity_score > 0.7]
            if len(complex_reqs) > 3:
                needs["complexity_level"] = "high"
        
        # Factor in domain model complexity
        if request.domain_model and len(request.domain_model.entities) > 10:
            needs["domain_complexity"] = "high"
        
        # Consider team expertise
        if request.team_expertise and len(request.team_expertise) > 5:
            needs["team_size"] = "large"
        
        return needs

    async def _select_architecture_pattern(self, request: ArchitectureRequest, needs: Dict[str, Any]) -> ArchitectureDecision:
        """Select appropriate architecture pattern"""
        
        # Pattern selection logic based on needs
        pattern_scores = {}
        
        for pattern, info in self.architecture_patterns.items():
            score = 0.0
            
            # Score based on scalability needs
            if needs["scalability_requirements"] == "high":
                if pattern in [ArchitecturePattern.MICROSERVICES, ArchitecturePattern.EVENT_DRIVEN]:
                    score += 0.3
                elif pattern == ArchitecturePattern.MONOLITHIC:
                    score -= 0.2
            
            # Score based on complexity tolerance
            if needs["complexity_level"] == "low":
                if pattern in [ArchitecturePattern.MONOLITHIC, ArchitecturePattern.LAYERED]:
                    score += 0.2
                elif pattern == ArchitecturePattern.MICROSERVICES:
                    score -= 0.3
            
            # Score based on team size
            if needs["team_size"] == "large":
                if pattern == ArchitecturePattern.MICROSERVICES:
                    score += 0.2
            elif needs["team_size"] == "small":
                if pattern in [ArchitecturePattern.MONOLITHIC, ArchitecturePattern.LAYERED]:
                    score += 0.2
            
            # Score based on performance needs
            if needs["performance_requirements"] == "high":
                if pattern in [ArchitecturePattern.MONOLITHIC, ArchitecturePattern.EVENT_DRIVEN]:
                    score += 0.1
            
            pattern_scores[pattern] = max(0.0, min(1.0, score + 0.5))  # Normalize to 0-1
        
        # Select pattern with highest score
        selected_pattern = max(pattern_scores.items(), key=lambda x: x[1])
        pattern, confidence = selected_pattern
        
        # Consider alternatives
        alternatives = [p.value for p, s in pattern_scores.items() if s > 0.4 and p != pattern]
        
        return ArchitectureDecision(
            id="pattern_selection",
            title="Architecture Pattern Selection",
            decision_type=ArchitectureDecisionType.PATTERN_SELECTION,
            description=f"Selected {pattern.value} architecture pattern",
            rationale=f"Best fit for {needs}. {self.architecture_patterns[pattern]['description']}",
            alternatives_considered=alternatives,
            consequences=self.architecture_patterns[pattern]['strengths'] + 
                        [f"Risk: {w}" for w in self.architecture_patterns[pattern]['weaknesses']],
            confidence_score=confidence,
            human_approval_required=True
        )

    async def _design_technology_stack(self, request: ArchitectureRequest, pattern_decision: Optional[ArchitectureDecision]) -> ArchitectureDecision:
        """Design technology stack based on requirements"""
        
        # Determine project type from requirements
        project_type = self._determine_project_type(request)
        
        # Get base technology recommendations
        base_tech = self.technology_recommendations.get(project_type, self.technology_recommendations["web_applications"])
        
        # Customize based on team expertise
        selected_tech = {}
        justification = {}
        
        for category, options in base_tech.items():
            if request.team_expertise:
                # Prefer technologies the team knows
                team_tech = [tech for tech in options if any(expert in tech for expert in request.team_expertise)]
                if team_tech:
                    selected_tech[category] = team_tech[0]
                    justification[category] = f"Team has expertise in {team_tech[0]}"
                else:
                    selected_tech[category] = options[0]
                    justification[category] = f"Recommended for {project_type}"
            else:
                selected_tech[category] = options[0]
                justification[category] = f"Industry standard for {project_type}"
        
        # Consider constraints
        if request.constraints:
            for constraint in request.constraints:
                if "budget" in constraint.lower():
                    # Prefer open-source technologies
                    if "frontend" in selected_tech:
                        selected_tech["frontend"] = "React"  # Open source
                    justification["budget"] = "Open-source technologies for budget constraints"
        
        # Create technology stack
        tech_stack = TechnologyStack(
            languages=selected_tech.get("languages", [selected_tech.get("backend", "Python")]),
            frameworks=selected_tech.get("frameworks", [selected_tech.get("frontend", "React")]),
            databases=selected_tech.get("database", ["PostgreSQL"]) if isinstance(selected_tech.get("database"), str) else selected_tech.get("database", ["PostgreSQL"]),
            infrastructure=selected_tech.get("deployment", ["Docker"]) if isinstance(selected_tech.get("deployment"), str) else selected_tech.get("deployment", ["Docker"]),
            tools=["Git", "CI/CD", "Testing Framework"],
            justification=justification
        )
        
        # Calculate confidence based on team expertise and constraints
        confidence = 0.7  # Base confidence
        if request.team_expertise:
            expertise_match = len([tech for tech in str(tech_stack) if any(expert in tech for expert in request.team_expertise)])
            confidence += min(0.2, expertise_match * 0.05)
        
        return ArchitectureDecision(
            id="technology_stack",
            title="Technology Stack Selection",
            decision_type=ArchitectureDecisionType.TECHNOLOGY_STACK,
            description=f"Selected technology stack for {project_type}",
            rationale=f"Technologies chosen based on project requirements, team expertise, and industry best practices",
            alternatives_considered=[tech for tech_list in base_tech.values() for tech in tech_list if tech not in str(tech_stack)],
            consequences=[
                f"Team will need expertise in: {', '.join(tech_stack.languages + tech_stack.frameworks)}",
                f"Infrastructure requirements: {', '.join(tech_stack.infrastructure)}",
                "Regular technology updates and maintenance required"
            ],
            confidence_score=confidence,
            human_approval_required=True
        )

    async def _define_quality_attributes(self, request: ArchitectureRequest) -> List[ArchitectureDecision]:
        """Define quality attributes and their requirements"""
        decisions = []
        
        # Analyze requirements for quality attributes
        quality_needs = {}
        if request.requirements and request.requirements.requirements:
            for req in request.requirements.requirements:
                req_text = req.description.lower()
                for qa, indicators in self.quality_attributes.items():
                    if any(indicator.lower() in req_text for indicator in indicators):
                        quality_needs[qa] = quality_needs.get(qa, 0) + 1
        
        # Add explicit quality requirements
        if request.quality_requirements:
            for qa, requirement in request.quality_requirements.items():
                quality_needs[qa] = quality_needs.get(qa, 0) + 2  # Higher weight for explicit requirements
        
        # Create decisions for significant quality attributes
        for qa, count in quality_needs.items():
            if count > 0:
                decision = ArchitectureDecision(
                    id=f"quality_{qa}",
                    title=f"{qa.title()} Requirements",
                    decision_type=ArchitectureDecisionType.QUALITY_ATTRIBUTES,
                    description=f"Define {qa} requirements and strategies",
                    rationale=f"Requirements indicate {count} {qa}-related needs",
                    alternatives_considered=[f"Alternative {qa} strategies", f"Lower {qa} priorities"],
                    consequences=[
                        f"Design must accommodate {qa} requirements",
                        f"Additional {qa} testing and validation needed",
                        f"Potential trade-offs with other quality attributes"
                    ],
                    confidence_score=min(0.9, count * 0.2 + 0.3),
                    human_approval_required=True
                )
                decisions.append(decision)
        
        return decisions

    async def _design_system_structure(self, request: ArchitectureRequest, pattern_decision: ArchitectureDecision) -> ArchitectureDecision:
        """Design high-level system structure"""
        
        # Extract pattern from decision
        pattern_name = pattern_decision.description.split()[1]  # Extract pattern name
        
        # Define structure based on pattern
        if "microservices" in pattern_name.lower():
            structure = {
                "services": ["User Service", "Business Logic Service", "Data Service"],
                "api_gateway": "API Gateway for service coordination",
                "data_layer": "Distributed data management",
                "communication": "HTTP/REST and async messaging"
            }
        elif "monolithic" in pattern_name.lower():
            structure = {
                "application_layer": "Single application with modules",
                "business_layer": "Business logic components", 
                "data_layer": "Centralized data access",
                "presentation_layer": "User interface layer"
            }
        elif "layered" in pattern_name.lower():
            structure = {
                "presentation_layer": "User interface and controllers",
                "business_layer": "Business logic and services",
                "data_access_layer": "Data access and repositories",
                "database_layer": "Data storage and management"
            }
        else:
            structure = {
                "core_components": "Main application components",
                "integration_layer": "External system integration",
                "data_management": "Data handling and storage"
            }
        
        return ArchitectureDecision(
            id="system_structure",
            title="System Structure Design",
            decision_type=ArchitectureDecisionType.SYSTEM_STRUCTURE,
            description=f"High-level system structure for {pattern_name} pattern",
            rationale=f"Structure aligns with {pattern_name} pattern principles and project requirements",
            alternatives_considered=["Alternative component organizations", "Different layer arrangements"],
            consequences=[
                "Clear separation of concerns",
                "Defined component boundaries",
                "Specific integration patterns required"
            ],
            confidence_score=0.8,
            human_approval_required=True
        )

    async def _create_system_architecture(self, request: ArchitectureRequest, decisions: List[ArchitectureDecision]) -> SystemArchitecture:
        """Create complete system architecture from decisions"""
        
        # Extract pattern
        pattern_decision = next((d for d in decisions if d.decision_type == ArchitectureDecisionType.PATTERN_SELECTION), None)
        pattern = ArchitecturePattern.LAYERED  # Default
        if pattern_decision:
            pattern_name = pattern_decision.description.split()[1].upper()
            try:
                pattern = ArchitecturePattern[pattern_name]
            except KeyError:
                pattern = ArchitecturePattern.LAYERED
        
        # Extract technology stack
        tech_decision = next((d for d in decisions if d.decision_type == ArchitectureDecisionType.TECHNOLOGY_STACK), None)
        tech_stack = TechnologyStack()
        if tech_decision:
            # Parse technology stack from decision (simplified)
            tech_stack = TechnologyStack(
                languages=["Python", "JavaScript"],  # Default - in real implementation, parse from decision
                frameworks=["React", "FastAPI"],
                databases=["PostgreSQL"],
                infrastructure=["Docker", "Kubernetes"],
                tools=["Git", "CI/CD"],
                justification={"selection": "Based on project requirements and team expertise"}
            )
        
        # Extract quality attributes
        quality_decisions = [d for d in decisions if d.decision_type == ArchitectureDecisionType.QUALITY_ATTRIBUTES]
        quality_attributes = {}
        for decision in quality_decisions:
            qa_name = decision.id.replace("quality_", "")
            quality_attributes[qa_name] = decision.description
        
        # Extract components from structure decision
        structure_decision = next((d for d in decisions if d.decision_type == ArchitectureDecisionType.SYSTEM_STRUCTURE), None)
        components = []
        if structure_decision:
            # Extract component information (simplified)
            components = [
                {"name": "Core Component", "type": "business_logic", "description": "Main business functionality"},
                {"name": "Data Component", "type": "data_access", "description": "Data management and storage"},
                {"name": "API Component", "type": "interface", "description": "External interface and API"}
            ]
        
        # Create architecture
        architecture = SystemArchitecture(
            name=f"{request.project_name}_architecture",
            description=f"System architecture for {request.project_name}",
            pattern=pattern,
            technology_stack=tech_stack,
            components=components,
            quality_attributes=quality_attributes,
            constraints=request.constraints or [],
            assumptions=[
                "Team has necessary technical expertise",
                "Infrastructure resources are available",
                "Requirements are stable"
            ],
            risks=[
                "Technology learning curve",
                "Integration complexity",
                "Scalability challenges"
            ]
        )
        
        return architecture

    async def _validate_architecture(self, architecture: SystemArchitecture, request: ArchitectureRequest) -> Dict[str, bool]:
        """Validate architecture against requirements and constraints"""
        validation_results = {}
        
        # Validate pattern selection
        validation_results["pattern_appropriate"] = True  # Simplified validation
        
        # Validate technology stack
        validation_results["technology_compatible"] = True
        if request.constraints:
            for constraint in request.constraints:
                if "no cloud" in constraint.lower() and "cloud" in str(architecture.technology_stack).lower():
                    validation_results["technology_compatible"] = False
        
        # Validate quality attributes coverage
        quality_coverage = len(architecture.quality_attributes) > 0
        validation_results["quality_attributes_defined"] = quality_coverage
        
        # Validate component structure
        validation_results["components_defined"] = len(architecture.components) > 0
        
        # Validate constraint compliance
        constraint_compliance = True
        if request.constraints:
            # Check each constraint (simplified)
            for constraint in request.constraints:
                if "budget" in constraint.lower():
                    # Check for cost-effective choices
                    if any("enterprise" in str(tech).lower() for tech in architecture.technology_stack.frameworks):
                        constraint_compliance = False
        validation_results["constraints_satisfied"] = constraint_compliance
        
        return validation_results

    async def _validate_technology_stack(self, tech_decision: ArchitectureDecision, request: ArchitectureRequest) -> Dict[str, bool]:
        """Validate technology stack selection"""
        validation_results = {}
        
        # Validate team expertise alignment
        if request.team_expertise:
            expertise_match = any(expert in tech_decision.description for expert in request.team_expertise)
            validation_results["team_expertise_match"] = expertise_match
        else:
            validation_results["team_expertise_match"] = True  # No constraints
        
        # Validate constraint compliance
        constraint_compliance = True
        if request.constraints:
            for constraint in request.constraints:
                if "open source" in constraint.lower() and "enterprise" in tech_decision.description.lower():
                    constraint_compliance = False
        validation_results["constraint_compliance"] = constraint_compliance
        
        # Validate technology compatibility
        validation_results["technology_compatibility"] = True  # Simplified - assume compatible
        
        return validation_results

    def _determine_project_type(self, request: ArchitectureRequest) -> str:
        """Determine project type from requirements"""
        if not request.requirements or not request.requirements.requirements:
            return "web_applications"
        
        req_text = " ".join([req.description.lower() for req in request.requirements.requirements])
        
        if any(word in req_text for word in ["mobile", "ios", "android", "app"]):
            return "mobile_applications"
        elif any(word in req_text for word in ["data", "analytics", "processing", "etl"]):
            return "data_processing"
        elif any(word in req_text for word in ["real-time", "low latency", "high performance"]):
            return "real_time_systems"
        else:
            return "web_applications"

    def _calculate_architecture_confidence(self, decisions: List[ArchitectureDecision], validation_results: Dict[str, bool]) -> float:
        """Calculate overall architecture confidence"""
        # Average decision confidence
        decision_confidence = sum(d.confidence_score for d in decisions) / len(decisions) if decisions else 0.0
        
        # Validation success rate
        validation_score = sum(validation_results.values()) / len(validation_results) if validation_results else 0.0
        
        # Weighted average
        return (decision_confidence * 0.7) + (validation_score * 0.3)

    async def _generate_architecture_recommendations(self, architecture: SystemArchitecture, decisions: List[ArchitectureDecision], validation_results: Dict[str, bool]) -> List[str]:
        """Generate architecture recommendations"""
        recommendations = []
        
        # Check for validation failures
        failed_validations = [k for k, v in validation_results.items() if not v]
        if failed_validations:
            recommendations.append(f"Address validation issues: {', '.join(failed_validations)}")
        
        # Check decision confidence
        low_confidence_decisions = [d for d in decisions if d.confidence_score < 0.6]
        if low_confidence_decisions:
            recommendations.append(f"Review low-confidence decisions: {', '.join([d.title for d in low_confidence_decisions])}")
        
        # Architecture-specific recommendations
        if architecture.pattern == ArchitecturePattern.MICROSERVICES:
            recommendations.extend([
                "Consider service discovery and configuration management",
                "Plan for distributed tracing and monitoring",
                "Design for eventual consistency"
            ])
        elif architecture.pattern == ArchitecturePattern.MONOLITHIC:
            recommendations.extend([
                "Plan for modular design within the monolith",
                "Consider future migration path to distributed architecture",
                "Implement proper layering and separation of concerns"
            ])
        
        # Quality attribute recommendations
        if not architecture.quality_attributes:
            recommendations.append("Define specific quality attribute requirements")
        
        return recommendations

    async def _generate_technology_recommendations(self, tech_decision: ArchitectureDecision, validation_results: Dict[str, bool]) -> List[str]:
        """Generate technology-specific recommendations"""
        recommendations = []
        
        # Check validation results
        if not validation_results.get("team_expertise_match", True):
            recommendations.append("Consider team training for selected technologies")
        
        if not validation_results.get("constraint_compliance", True):
            recommendations.append("Review technology choices against constraints")
        
        # General technology recommendations
        recommendations.extend([
            "Evaluate technology learning curve and team readiness",
            "Plan for technology updates and maintenance",
            "Consider long-term support and community",
            "Establish development and deployment environments"
        ])
        
        return recommendations

    async def _assess_architecture_risks(self, architecture: SystemArchitecture, decisions: List[ArchitectureDecision]) -> Dict[str, str]:
        """Assess architecture risks"""
        risks = {}
        
        # Pattern-specific risks
        if architecture.pattern == ArchitecturePattern.MICROSERVICES:
            risks["complexity"] = "High - Distributed system complexity"
            risks["operational"] = "Medium - Multiple deployment units"
            risks["data_consistency"] = "High - Eventual consistency challenges"
        elif architecture.pattern == ArchitecturePattern.MONOLITHIC:
            risks["scalability"] = "Medium - Single scaling unit"
            risks["technology_lock"] = "Medium - Single technology stack"
            risks["team_bottleneck"] = "Medium - Single deployment pipeline"
        
        # Technology risks
        new_technologies = len([tech for tech in architecture.technology_stack.languages + architecture.technology_stack.frameworks])
        if new_technologies > 5:
            risks["technology_learning"] = "High - Many new technologies"
        
        # Decision confidence risks
        low_confidence_decisions = [d for d in decisions if d.confidence_score < 0.7]
        if low_confidence_decisions:
            risks["decision_uncertainty"] = f"Medium - {len(low_confidence_decisions)} uncertain decisions"
        
        return risks

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute architecture design task
        
        Args:
            task: Task configuration with architecture parameters
            
        Returns:
            Architecture design results and recommendations
        """
        try:
            # Parse task request
            request_data = task.get("request", {})
            request = ArchitectureRequest(**request_data)
            
            task_type = task.get("type", "design_architecture")
            
            # Route to appropriate method
            if task_type == "design_architecture":
                result = await self.design_architecture(request)
            elif task_type == "evaluate_technology_stack":
                result = await self.evaluate_technology_stack(request)
            else:
                raise ValidationError(f"Unsupported task type: {task_type}")
            
            # Format response
            response = {
                "agent_id": self.agent_id,
                "task_type": task_type,
                "confidence_score": result.confidence_score,
                "human_review_required": result.human_review_required,
                "architecture": asdict(result.architecture),
                "decisions": [asdict(decision) for decision in result.decisions],
                "validation_results": result.validation_results,
                "recommendations": result.recommendations,
                "risk_assessment": result.risk_assessment or {}
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"Architecture design execution failed: {str(e)}")
            raise AgentError(f"Architecture design execution failed: {str(e)}")

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate agent output format and completeness
        
        Args:
            output: Agent output to validate
            
        Returns:
            True if output is valid
        """
        required_fields = ["agent_id", "task_type", "confidence_score", "architecture", "decisions"]
        
        for field in required_fields:
            if field not in output:
                return False
        
        # Validate confidence score
        if not (0.0 <= output["confidence_score"] <= 1.0):
            return False
        
        # Validate architecture structure
        architecture = output["architecture"]
        if not isinstance(architecture, dict) or "name" not in architecture:
            return False
        
        # Validate decisions
        decisions = output["decisions"]
        if not isinstance(decisions, list):
            return False
        
        return True
