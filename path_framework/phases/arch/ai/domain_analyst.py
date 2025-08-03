"""
AI Domain Analyst - Phase 1 Agent
PATH Framework - Process/AI/Technology/Human

Responsible for:
- Requirements analysis and domain modeling
- Business rule extraction and validation
- Stakeholder analysis and compliance requirements
- Domain-driven design foundations

Decision Authority: Autonomous for analysis, Human approval for critical business decisions
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

from ....agents_base import BaseAgent
from ....exceptions import PathFrameworkError
from ....models.arch_models import (
    RequirementAnalysis,
    DomainModel,
    DomainEntity,
    BusinessRule,
    Requirement,
    RequirementType,
    RequirementPriority,
    StakeholderAnalysis
)


class AnalysisType(Enum):
    REQUIREMENTS = "requirements"
    DOMAIN_MODEL = "domain_model"
    BUSINESS_RULES = "business_rules"
    STAKEHOLDER = "stakeholder"
    COMPLIANCE = "compliance"


@dataclass
class DomainAnalysisRequest:
    """Request structure for domain analysis"""
    project_name: str
    project_description: str
    business_context: str
    stakeholder_input: List[str]
    analysis_type: AnalysisType
    existing_documentation: List[str] = None
    compliance_frameworks: List[str] = None
    industry_domain: str = ""


@dataclass
class DomainAnalysisResult:
    """Result structure for domain analysis"""
    analysis_type: AnalysisType
    confidence_score: float
    domain_model: Optional[DomainModel] = None
    requirements: Optional[List[Requirement]] = None
    business_rules: Optional[List[BusinessRule]] = None
    stakeholders: Optional[StakeholderAnalysis] = None
    compliance_requirements: Optional[Dict[str, Any]] = None
    recommendations: List[str] = None
    human_review_required: bool = False
    validation_errors: List[str] = None


class AIDomainAnalyst(BaseAgent):
    """
    AI Domain Analyst - Specialized in requirements analysis and domain modeling
    
    Decision Authority: Autonomous for analysis, Human approval for business decisions
    Capabilities:
    - Natural language requirements extraction
    - Domain entity identification and modeling
    - Business rule extraction and validation
    - Stakeholder analysis and mapping
    - Compliance requirement identification
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            agent_id="ai_domain_analyst",
            name="AI Domain Analyst", 
            specialization="Requirements analysis & domain modeling",
            decision_authority="Autonomous",
            phase=1,
            config=config
        )
        
        # Domain analysis capabilities
        self.supported_domains = [
            "business_applications",
            "data_processing", 
            "protocol_systems",
            "real_time_systems",
            "web_applications",
            "mobile_applications",
            "enterprise_systems"
        ]
        
        # Analysis patterns and templates
        self.analysis_patterns = {
            "entity_extraction": [
                "nouns_identification",
                "relationship_mapping", 
                "attribute_extraction",
                "behavior_identification"
            ],
            "requirement_classification": [
                "functional_requirements",
                "non_functional_requirements", 
                "business_requirements",
                "technical_requirements"
            ],
            "business_rule_patterns": [
                "constraint_rules",
                "derivation_rules",
                "existence_rules", 
                "reaction_rules"
            ]
        }

    async def analyze_requirements(self, request: DomainAnalysisRequest) -> DomainAnalysisResult:
        """
        Analyze project requirements from natural language descriptions
        
        Args:
            request: Domain analysis request with project context
            
        Returns:
            DomainAnalysisResult with extracted requirements
        """
        try:
            self.logger.info(f"Starting requirements analysis for {request.project_name}")
            
            # Validate input
            if not request.project_description or not request.business_context:
                raise PathFrameworkError("Project description and business context are required")
            
            # Extract requirements using NLP patterns
            requirements = await self._extract_requirements(
                request.project_description,
                request.business_context,
                request.stakeholder_input
            )
            
            # Classify and prioritize requirements
            classified_requirements = await self._classify_requirements(requirements)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(classified_requirements, request)
            
            # Determine if human review is needed
            human_review = self._requires_human_review(classified_requirements, confidence)
            
            result = DomainAnalysisResult(
                analysis_type=AnalysisType.REQUIREMENTS,
                confidence_score=confidence,
                requirements=classified_requirements,
                human_review_required=human_review,
                recommendations=await self._generate_requirements_recommendations(classified_requirements)
            )
            
            self.logger.info(f"Requirements analysis completed with {len(classified_requirements)} requirements")
            return result
            
        except Exception as e:
            self.logger.error(f"Stakeholder analysis failed: {str(e)}")
            raise PathFrameworkError(f"Stakeholder analysis failed: {str(e)}")

    async def model_domain(self, request: DomainAnalysisRequest) -> DomainAnalysisResult:
        """
        Create domain model from requirements and business context
        
        Args:
            request: Domain analysis request
            
        Returns:
            DomainAnalysisResult with domain model
        """
        try:
            self.logger.info(f"Starting domain modeling for {request.project_name}")
            
            # Extract domain entities
            entities = await self._extract_domain_entities(
                request.project_description,
                request.business_context
            )
            
            # Model relationships
            relationships = await self._model_relationships(entities)
            
            # Create domain model
            domain_model = DomainModel(
                name=f"{request.project_name}_domain",
                description=f"Domain model for {request.project_name}",
                entities=entities,
                bounded_contexts=await self._identify_bounded_contexts(entities),
                domain_services=await self._identify_domain_services(entities)
            )
            
            confidence = self._calculate_domain_model_confidence(domain_model)
            
            result = DomainAnalysisResult(
                analysis_type=AnalysisType.DOMAIN_MODEL,
                confidence_score=confidence,
                domain_model=domain_model,
                human_review_required=confidence < 0.8,
                recommendations=await self._generate_domain_model_recommendations(domain_model)
            )
            
            self.logger.info(f"Domain modeling completed with {len(entities)} entities")
            return result
            
        except Exception as e:
            self.logger.error(f"Domain modeling failed: {str(e)}")
            raise PathFrameworkError(f"Domain modeling failed: {str(e)}")

    async def extract_business_rules(self, request: DomainAnalysisRequest) -> DomainAnalysisResult:
        """
        Extract and validate business rules from requirements
        
        Args:
            request: Domain analysis request
            
        Returns:
            DomainAnalysisResult with business rules
        """
        try:
            self.logger.info(f"Extracting business rules for {request.project_name}")
            
            # Extract business rules using pattern matching
            business_rules = await self._extract_business_rules(
                request.project_description,
                request.business_context
            )
            
            # Validate rule consistency
            validated_rules = await self._validate_business_rules(business_rules)
            
            confidence = self._calculate_business_rules_confidence(validated_rules)
            
            result = DomainAnalysisResult(
                analysis_type=AnalysisType.BUSINESS_RULES,
                confidence_score=confidence,
                business_rules=validated_rules,
                human_review_required=confidence < 0.7,
                recommendations=await self._generate_business_rules_recommendations(validated_rules)
            )
            
            self.logger.info(f"Business rules extraction completed with {len(validated_rules)} rules")
            return result
            
        except Exception as e:
            self.logger.error(f"Business rules extraction failed: {str(e)}")
            raise PathFrameworkError(f"Business rules extraction failed: {str(e)}")

    async def analyze_stakeholders(self, request: DomainAnalysisRequest) -> DomainAnalysisResult:
        """
        Analyze stakeholders and their concerns
        
        Args:
            request: Domain analysis request
            
        Returns:
            DomainAnalysisResult with stakeholder analysis
        """
        try:
            self.logger.info(f"Analyzing stakeholders for {request.project_name}")
            
            # Extract stakeholder information
            stakeholder_analysis = await self._analyze_stakeholders(
                request.stakeholder_input,
                request.business_context
            )
            
            confidence = self._calculate_stakeholder_confidence(stakeholder_analysis)
            
            result = DomainAnalysisResult(
                analysis_type=AnalysisType.STAKEHOLDER,
                confidence_score=confidence,
                stakeholders=stakeholder_analysis,
                human_review_required=True,  # Always require human review for stakeholder analysis
                recommendations=await self._generate_stakeholder_recommendations(stakeholder_analysis)
            )
            
            self.logger.info("Stakeholder analysis completed")
            return result
            
        except Exception as e:
            self.logger.error(f"Stakeholder analysis failed: {str(e)}")
            raise PathFrameworkError(f"Stakeholder analysis failed: {str(e)}")

    # Private helper methods
    async def _extract_requirements(self, description: str, context: str, stakeholder_input: List[str]) -> List[Requirement]:
        """Extract requirements from natural language text"""
        requirements = []
        
        # Simple pattern-based extraction (in real implementation, use NLP models)
        requirement_indicators = [
            "must", "should", "shall", "will", "requires", "needs",
            "user can", "system will", "application should"
        ]
        
        # Combine all text sources
        all_text = f"{description} {context} {' '.join(stakeholder_input or [])}"
        sentences = all_text.split('.')
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in requirement_indicators):
                req = Requirement(
                    title=f"Requirement {i+1}",
                    description=sentence,
                    type=self._classify_requirement_type(sentence),
                    priority=self._assess_requirement_priority(sentence)
                )
                requirements.append(req)
        
        return requirements

    async def _classify_requirements(self, requirements: List[Requirement]) -> List[Requirement]:
        """Classify and enhance requirements"""
        for req in requirements:
            # Add acceptance criteria
            req.acceptance_criteria = await self._generate_acceptance_criteria(req.description)
            
            # Assess complexity
            req.complexity_score = self._assess_complexity(req.description)
            
            # Identify dependencies
            req.dependencies = await self._identify_dependencies(req, requirements)
        
        return requirements

    def _classify_requirement_type(self, text: str) -> RequirementType:
        """Classify requirement type based on content"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["performance", "security", "scalability", "availability"]):
            return RequirementType.NON_FUNCTIONAL
        elif any(word in text_lower for word in ["business", "process", "workflow", "compliance"]):
            return RequirementType.BUSINESS
        elif any(word in text_lower for word in ["technical", "database", "api", "integration"]):
            return RequirementType.TECHNICAL
        else:
            return RequirementType.FUNCTIONAL

    def _assess_requirement_priority(self, text: str) -> RequirementPriority:
        """Assess requirement priority"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["critical", "essential", "must have"]):
            return RequirementPriority.CRITICAL
        elif any(word in text_lower for word in ["important", "should have"]):
            return RequirementPriority.HIGH
        elif any(word in text_lower for word in ["nice to have", "could have"]):
            return RequirementPriority.LOW
        else:
            return RequirementPriority.MEDIUM

    async def _extract_domain_entities(self, description: str, context: str) -> List[DomainEntity]:
        """Extract domain entities from text"""
        entities = []
        
        # Simple noun extraction (in real implementation, use NLP)
        # This is a simplified pattern-based approach
        common_entity_patterns = [
            "user", "customer", "order", "product", "payment", "account",
            "service", "system", "data", "report", "transaction", "session"
        ]
        
        text = f"{description} {context}".lower()
        
        for pattern in common_entity_patterns:
            if pattern in text:
                entity = DomainEntity(
                    name=pattern.title(),
                    description=f"{pattern.title()} entity in the domain",
                    attributes={"id": "string", "created_at": "datetime"},
                    behaviors=[f"create_{pattern}", f"update_{pattern}", f"delete_{pattern}"]
                )
                entities.append(entity)
        
        return entities

    async def _model_relationships(self, entities: List[DomainEntity]) -> Dict[str, str]:
        """Model relationships between entities"""
        relationships = {}
        
        # Simple relationship modeling
        for entity in entities:
            for other_entity in entities:
                if entity.name != other_entity.name:
                    # Simple heuristic for relationships
                    if "user" in entity.name.lower() and "order" in other_entity.name.lower():
                        relationships[f"{entity.name}_to_{other_entity.name}"] = "one_to_many"
        
        return relationships

    async def _identify_bounded_contexts(self, entities: List[DomainEntity]) -> List[str]:
        """Identify bounded contexts"""
        contexts = set()
        
        # Group entities by domain areas
        for entity in entities:
            if any(word in entity.name.lower() for word in ["user", "customer", "account"]):
                contexts.add("User Management")
            elif any(word in entity.name.lower() for word in ["order", "product", "payment"]):
                contexts.add("Order Management")
            elif any(word in entity.name.lower() for word in ["report", "data", "analytics"]):
                contexts.add("Analytics")
        
        return list(contexts)

    async def _identify_domain_services(self, entities: List[DomainEntity]) -> List[str]:
        """Identify domain services"""
        services = []
        
        # Identify services based on entity behaviors
        for entity in entities:
            for behavior in entity.behaviors:
                if behavior.startswith("create_") or behavior.startswith("process_"):
                    service_name = f"{entity.name}Service"
                    if service_name not in services:
                        services.append(service_name)
        
        return services

    async def _extract_business_rules(self, description: str, context: str) -> List[BusinessRule]:
        """Extract business rules from text"""
        rules = []
        
        # Pattern-based rule extraction
        rule_patterns = [
            ("if", "then"), ("when", "must"), ("should", "unless")
        ]
        
        text = f"{description} {context}"
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip().lower()
            for condition_word, action_word in rule_patterns:
                if condition_word in sentence and action_word in sentence:
                    rule = BusinessRule(
                        name=f"Business Rule {i+1}",
                        description=sentence,
                        condition=sentence.split(condition_word)[1].split(action_word)[0].strip(),
                        action=sentence.split(action_word)[1].strip(),
                        priority=RequirementPriority.MEDIUM
                    )
                    rules.append(rule)
        
        return rules

    async def _validate_business_rules(self, rules: List[BusinessRule]) -> List[BusinessRule]:
        """Validate business rules for consistency"""
        # Simple validation - remove duplicates and empty rules
        validated_rules = []
        seen_descriptions = set()
        
        for rule in rules:
            if rule.description and rule.description not in seen_descriptions:
                validated_rules.append(rule)
                seen_descriptions.add(rule.description)
        
        return validated_rules

    async def _analyze_stakeholders(self, stakeholder_input: List[str], context: str) -> StakeholderAnalysis:
        """Analyze stakeholders"""
        primary_stakeholders = []
        secondary_stakeholders = []
        stakeholder_concerns = {}
        
        # Extract stakeholder information
        if stakeholder_input:
            for input_text in stakeholder_input:
                # Simple pattern matching for stakeholder types
                if any(word in input_text.lower() for word in ["user", "customer", "client"]):
                    primary_stakeholders.append("End Users")
                elif any(word in input_text.lower() for word in ["business", "manager", "owner"]):
                    primary_stakeholders.append("Business Stakeholders")
                elif any(word in input_text.lower() for word in ["developer", "technical", "admin"]):
                    secondary_stakeholders.append("Technical Team")
        
        # Default stakeholders if none identified
        if not primary_stakeholders:
            primary_stakeholders = ["Business Owner", "End Users"]
        if not secondary_stakeholders:
            secondary_stakeholders = ["Development Team", "Operations Team"]
        
        # Generate stakeholder concerns
        for stakeholder in primary_stakeholders:
            stakeholder_concerns[stakeholder] = [
                "System usability and performance",
                "Business value delivery",
                "Return on investment"
            ]
        
        return StakeholderAnalysis(
            primary_stakeholders=primary_stakeholders,
            secondary_stakeholders=secondary_stakeholders,
            stakeholder_concerns=stakeholder_concerns,
            communication_plan={
                "Business Owner": "Weekly status meetings",
                "End Users": "User acceptance testing sessions",
                "Development Team": "Daily standups and sprint reviews"
            }
        )

    # Confidence calculation methods
    def _calculate_confidence(self, requirements: List[Requirement], request: DomainAnalysisRequest) -> float:
        """Calculate confidence score for requirements analysis"""
        if not requirements:
            return 0.0
        
        # Base confidence on completeness and clarity
        completeness_score = min(len(requirements) / 10.0, 1.0)  # Assume 10 requirements is complete
        clarity_score = sum(1 for req in requirements if len(req.description) > 20) / len(requirements)
        context_score = 1.0 if request.business_context else 0.5
        
        return (completeness_score + clarity_score + context_score) / 3.0

    def _calculate_domain_model_confidence(self, domain_model: DomainModel) -> float:
        """Calculate confidence score for domain model"""
        entity_score = min(len(domain_model.entities) / 5.0, 1.0)  # Assume 5 entities is good
        context_score = min(len(domain_model.bounded_contexts) / 3.0, 1.0)  # Assume 3 contexts is good
        service_score = min(len(domain_model.domain_services) / 3.0, 1.0)
        
        return (entity_score + context_score + service_score) / 3.0

    def _calculate_business_rules_confidence(self, rules: List[BusinessRule]) -> float:
        """Calculate confidence score for business rules"""
        if not rules:
            return 0.0
        
        # Base confidence on rule completeness
        complete_rules = sum(1 for rule in rules if rule.condition and rule.action)
        return complete_rules / len(rules)

    def _calculate_stakeholder_confidence(self, analysis: StakeholderAnalysis) -> float:
        """Calculate confidence score for stakeholder analysis"""
        primary_score = min(len(analysis.primary_stakeholders) / 3.0, 1.0)
        secondary_score = min(len(analysis.secondary_stakeholders) / 3.0, 1.0)
        concerns_score = 1.0 if analysis.stakeholder_concerns else 0.0
        
        return (primary_score + secondary_score + concerns_score) / 3.0

    def _requires_human_review(self, requirements: List[Requirement], confidence: float) -> bool:
        """Determine if human review is required"""
        # Require human review for low confidence or business-critical requirements
        if confidence < 0.7:
            return True
        
        critical_requirements = [req for req in requirements if req.priority == RequirementPriority.CRITICAL]
        business_requirements = [req for req in requirements if req.type == RequirementType.BUSINESS]
        
        return len(critical_requirements) > 0 or len(business_requirements) > 3

    def _assess_complexity(self, description: str) -> float:
        """Assess requirement complexity"""
        complexity_indicators = ["integration", "complex", "multiple", "advanced", "algorithm"]
        score = sum(1 for indicator in complexity_indicators if indicator in description.lower())
        return min(score / len(complexity_indicators), 1.0)

    async def _generate_acceptance_criteria(self, description: str) -> List[str]:
        """Generate acceptance criteria for a requirement"""
        return [
            f"Given the requirement: {description[:50]}...",
            "When the feature is implemented",
            "Then it should meet the specified behavior"
        ]

    async def _identify_dependencies(self, requirement: Requirement, all_requirements: List[Requirement]) -> List[str]:
        """Identify dependencies between requirements"""
        dependencies = []
        
        # Simple keyword-based dependency detection
        req_keywords = set(requirement.description.lower().split())
        
        for other_req in all_requirements:
            if other_req.id != requirement.id:
                other_keywords = set(other_req.description.lower().split())
                if len(req_keywords.intersection(other_keywords)) > 2:
                    dependencies.append(other_req.id)
        
        return dependencies

    # Recommendation generation methods
    async def _generate_requirements_recommendations(self, requirements: List[Requirement]) -> List[str]:
        """Generate recommendations for requirements"""
        recommendations = []
        
        if not requirements:
            recommendations.append("No requirements identified. Consider conducting stakeholder interviews.")
        
        critical_count = len([r for r in requirements if r.priority == RequirementPriority.CRITICAL])
        if critical_count > 5:
            recommendations.append("High number of critical requirements. Consider prioritization review.")
        
        complex_requirements = [r for r in requirements if r.complexity_score > 0.7]
        if complex_requirements:
            recommendations.append(f"Found {len(complex_requirements)} high-complexity requirements. Consider breaking them down.")
        
        return recommendations

    async def _generate_domain_model_recommendations(self, domain_model: DomainModel) -> List[str]:
        """Generate recommendations for domain model"""
        recommendations = []
        
        if len(domain_model.entities) < 3:
            recommendations.append("Consider identifying more domain entities for a complete model.")
        
        if not domain_model.bounded_contexts:
            recommendations.append("Define bounded contexts to better organize the domain.")
        
        if len(domain_model.domain_services) < 2:
            recommendations.append("Consider identifying domain services for business logic encapsulation.")
        
        return recommendations

    async def _generate_business_rules_recommendations(self, rules: List[BusinessRule]) -> List[str]:
        """Generate recommendations for business rules"""
        recommendations = []
        
        if not rules:
            recommendations.append("No business rules identified. Review requirements for implicit business logic.")
        
        incomplete_rules = [r for r in rules if not r.condition or not r.action]
        if incomplete_rules:
            recommendations.append(f"Found {len(incomplete_rules)} incomplete business rules. Review and complete them.")
        
        return recommendations

    async def _generate_stakeholder_recommendations(self, analysis: StakeholderAnalysis) -> List[str]:
        """Generate recommendations for stakeholder analysis"""
        recommendations = []
        
        if len(analysis.primary_stakeholders) < 2:
            recommendations.append("Consider identifying more primary stakeholders.")
        
        if not analysis.communication_plan:
            recommendations.append("Develop a comprehensive stakeholder communication plan.")
        
        recommendations.append("Schedule regular stakeholder reviews throughout the project.")
        
        return recommendations

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute domain analysis task
        
        Args:
            task: Task configuration with analysis parameters
            
        Returns:
            Analysis results and recommendations
        """
        try:
            # Parse task request
            request = DomainAnalysisRequest(**task.get("request", {}))
            analysis_type = request.analysis_type
            
            # Route to appropriate analysis method
            if analysis_type == AnalysisType.REQUIREMENTS:
                result = await self.analyze_requirements(request)
            elif analysis_type == AnalysisType.DOMAIN_MODEL:
                result = await self.model_domain(request)
            elif analysis_type == AnalysisType.BUSINESS_RULES:
                result = await self.extract_business_rules(request)
            elif analysis_type == AnalysisType.STAKEHOLDER:
                result = await self.analyze_stakeholders(request)
            else:
                raise PathFrameworkError(f"Unsupported analysis type: {analysis_type}")
            
            # Format response
            response = {
                "agent_id": self.agent_id,
                "analysis_type": result.analysis_type.value,
                "confidence_score": result.confidence_score,
                "human_review_required": result.human_review_required,
                "recommendations": result.recommendations or [],
                "validation_errors": result.validation_errors or []
            }
            
            # Add type-specific results
            if result.requirements:
                response["requirements"] = [asdict(req) for req in result.requirements]
            if result.domain_model:
                response["domain_model"] = asdict(result.domain_model)
            if result.business_rules:
                response["business_rules"] = [asdict(rule) for rule in result.business_rules]
            if result.stakeholders:
                response["stakeholders"] = asdict(result.stakeholders)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Domain analysis execution failed: {str(e)}")
            raise PathFrameworkError(f"Domain analysis execution failed: {str(e)}")

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate agent output format and completeness
        
        Args:
            output: Agent output to validate
            
        Returns:
            True if output is valid
        """
        required_fields = ["agent_id", "analysis_type", "confidence_score"]
        
        for field in required_fields:
            if field not in output:
                return False
        
        # Validate confidence score
        if not (0.0 <= output["confidence_score"] <= 1.0):
            return False
        
        # Validate analysis type
        valid_types = [t.value for t in AnalysisType]
        if output["analysis_type"] not in valid_types:
            return False
        
        return True
