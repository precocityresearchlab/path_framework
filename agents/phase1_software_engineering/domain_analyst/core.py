"""
Domain Analyst Agent

This agent specializes in requirements analysis and domain modeling for the 
PATH Framework. It extracts business requirements, creates domain models,
and establishes the ubiquitous language for the project.

The Domain Analyst Agent is responsible for:
- Parsing business requirements into structured domain models
- Identifying stakeholders and their constraints
- Creating comprehensive domain models with clear relationships
- Establishing ubiquitous language for the project
- Analyzing compliance and regulatory requirements
"""

import asyncio
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.base_agent import BaseAgent, AgentRequest, AgentResponse, ValidationResult, DecisionAuthority


@dataclass
class DomainEntity:
    """Represents a domain entity with attributes and business rules"""
    name: str
    attributes: List[Dict[str, str]]
    business_rules: List[str]
    relationships: List[Dict[str, Any]]
    description: str


@dataclass
class DomainModel:
    """Complete domain model for the project"""
    entities: List[DomainEntity]
    relationships: List[Dict[str, Any]]
    business_rules: List[str]
    ubiquitous_language: Dict[str, str]
    compliance_requirements: List[str]
    stakeholder_constraints: List[Dict[str, Any]]


@dataclass
class RequirementAnalysis:
    """Analysis results from requirement processing"""
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    stakeholders: List[Dict[str, Any]]
    constraints: List[str]
    assumptions: List[str]
    domain_model: DomainModel


class DomainAnalystAgent(BaseAgent):
    """
    Domain Analyst Agent for requirements analysis and domain modeling.
    
    This agent specializes in:
    - Natural language processing for requirement extraction
    - Domain-driven design principles
    - Stakeholder analysis and constraint identification
    - Compliance and regulatory requirement analysis
    """
    
    def __init__(self, config: Dict[str, Any], llm_provider=None):
        super().__init__(config, llm_provider)
        
        # Domain analysis capabilities
        self.domain_patterns = self._load_domain_patterns()
        self.compliance_frameworks = self._load_compliance_frameworks()
        self.entity_extractors = self._initialize_entity_extractors()
        
        # Decision authority configuration
        self.decision_authority_map = {
            "domain_model_validation": DecisionAuthority.AUTONOMOUS,
            "requirement_prioritization": DecisionAuthority.HUMAN_APPROVAL,
            "compliance_analysis": DecisionAuthority.COLLABORATIVE,
            "stakeholder_mapping": DecisionAuthority.AUTONOMOUS,
            "ubiquitous_language": DecisionAuthority.AUTONOMOUS
        }
        
        self.logger.info("Domain Analyst Agent initialized")
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """
        Process domain analysis requests.
        
        Supported request types:
        - analyze_requirements: Analyze business requirements
        - extract_domain_model: Extract domain entities and relationships
        - validate_domain: Validate domain model against patterns
        - analyze_compliance: Analyze regulatory requirements
        """
        try:
            if request.request_type == "analyze_requirements":
                return await self._analyze_requirements(request)
            elif request.request_type == "extract_domain_model":
                return await self._extract_domain_model(request)
            elif request.request_type == "validate_domain":
                return await self._validate_domain_model(request)
            elif request.request_type == "analyze_compliance":
                return await self._analyze_compliance(request)
            else:
                return self._create_error_response(
                    request, f"Unknown request type: {request.request_type}"
                )
                
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return self._create_error_response(request, str(e))
    
    async def validate_output(self, output: Any) -> ValidationResult:
        """Validate domain analysis output"""
        errors = []
        warnings = []
        
        if isinstance(output, RequirementAnalysis):
            # Validate requirement analysis
            if not output.functional_requirements:
                errors.append("No functional requirements identified")
            
            if not output.domain_model.entities:
                errors.append("No domain entities identified")
            
            if len(output.domain_model.ubiquitous_language) < 5:
                warnings.append("Limited ubiquitous language vocabulary")
                
        elif isinstance(output, DomainModel):
            # Validate domain model
            if not output.entities:
                errors.append("Domain model must contain at least one entity")
            
            for entity in output.entities:
                if not entity.attributes:
                    warnings.append(f"Entity {entity.name} has no attributes")
                if not entity.business_rules:
                    warnings.append(f"Entity {entity.name} has no business rules")
        
        confidence_score = max(0.0, 1.0 - (len(errors) * 0.3) - (len(warnings) * 0.1))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            confidence_score=confidence_score,
            recommendations=self._generate_recommendations(errors, warnings)
        )
    
    async def _analyze_requirements(self, request: AgentRequest) -> AgentResponse:
        """Analyze business requirements and extract structured information"""
        requirements_text = request.data.get("requirements_text", "")
        project_context = request.data.get("project_context", {})
        
        self.logger.info("Analyzing business requirements")
        
        # Extract functional and non-functional requirements
        functional_reqs = await self._extract_functional_requirements(requirements_text)
        non_functional_reqs = await self._extract_non_functional_requirements(requirements_text)
        
        # Identify stakeholders and constraints
        stakeholders = await self._identify_stakeholders(requirements_text, project_context)
        constraints = await self._extract_constraints(requirements_text)
        assumptions = await self._extract_assumptions(requirements_text)
        
        # Create domain model
        domain_model = await self._create_domain_model(
            requirements_text, functional_reqs, stakeholders
        )
        
        # Analyze compliance requirements
        compliance_reqs = await self._analyze_compliance_requirements(
            requirements_text, project_context
        )
        domain_model.compliance_requirements = compliance_reqs
        
        analysis = RequirementAnalysis(
            functional_requirements=functional_reqs,
            non_functional_requirements=non_functional_reqs,
            stakeholders=stakeholders,
            constraints=constraints,
            assumptions=assumptions,
            domain_model=domain_model
        )
        
        # Validate the analysis
        validation = await self.validate_output(analysis)
        
        return AgentResponse(
            id=self._generate_response_id(),
            request_id=request.id,
            timestamp=datetime.utcnow(),
            from_agent=self.agent_id,
            to_agent=request.from_agent,
            response_type="requirement_analysis",
            data={"analysis": analysis, "validation": validation},
            status="success" if validation.is_valid else "partial",
            confidence_score=validation.confidence_score,
            reasoning=self._generate_analysis_reasoning(analysis)
        )
    
    async def _extract_domain_model(self, request: AgentRequest) -> AgentResponse:
        """Extract domain entities and relationships from requirements"""
        requirements = request.data.get("requirements", [])
        existing_model = request.data.get("existing_model")
        
        self.logger.info("Extracting domain model from requirements")
        
        # Extract entities
        entities = []
        for req in requirements:
            req_entities = await self._extract_entities_from_requirement(req)
            entities.extend(req_entities)
        
        # Deduplicate and merge entities
        merged_entities = self._merge_duplicate_entities(entities)
        
        # Identify relationships
        relationships = await self._identify_entity_relationships(merged_entities)
        
        # Extract business rules
        business_rules = await self._extract_business_rules(requirements)
        
        # Build ubiquitous language
        ubiquitous_language = self._build_ubiquitous_language(
            merged_entities, relationships, business_rules
        )
        
        domain_model = DomainModel(
            entities=merged_entities,
            relationships=relationships,
            business_rules=business_rules,
            ubiquitous_language=ubiquitous_language,
            compliance_requirements=[],
            stakeholder_constraints=[]
        )
        
        validation = await self.validate_output(domain_model)
        
        return AgentResponse(
            id=self._generate_response_id(),
            request_id=request.id,
            timestamp=datetime.utcnow(),
            from_agent=self.agent_id,
            to_agent=request.from_agent,
            response_type="domain_model",
            data={"domain_model": domain_model, "validation": validation},
            status="success" if validation.is_valid else "partial",
            confidence_score=validation.confidence_score,
            reasoning="Domain model extracted using DDD principles"
        )
    
    async def _extract_functional_requirements(self, text: str) -> List[str]:
        """Extract functional requirements from requirements text"""
        # Use LLM to identify functional requirements
        if self.llm_provider:
            prompt = f"""
            Analyze the following requirements text and extract all functional requirements.
            A functional requirement describes what the system should do.
            
            Requirements text:
            {text}
            
            Extract functional requirements as a numbered list:
            """
            response = await self.llm_provider.generate_response(prompt)
            return self._parse_numbered_list(response)
        
        # Fallback: simple pattern matching
        functional_patterns = [
            r"The system shall (.+)",
            r"The system must (.+)",
            r"The system should (.+)",
            r"Users can (.+)",
            r"Users must be able to (.+)"
        ]
        
        requirements = []
        for pattern in functional_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend(matches)
        
        return requirements
    
    async def _extract_non_functional_requirements(self, text: str) -> List[str]:
        """Extract non-functional requirements from requirements text"""
        if self.llm_provider:
            prompt = f"""
            Analyze the following requirements text and extract all non-functional requirements.
            Non-functional requirements describe quality attributes like performance, security, usability.
            
            Requirements text:
            {text}
            
            Extract non-functional requirements as a numbered list:
            """
            response = await self.llm_provider.generate_response(prompt)
            return self._parse_numbered_list(response)
        
        # Fallback: pattern matching for common NFRs
        nfr_patterns = [
            r"response time.{0,20}(\d+\s*(?:ms|seconds?))",
            r"availability.{0,20}(\d+\.?\d*%)",
            r"concurrent users.{0,20}(\d+)",
            r"security.{0,50}(authentication|authorization|encryption)",
            r"scalability.{0,50}(\d+.{0,20}users)"
        ]
        
        requirements = []
        for pattern in nfr_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                requirements.append(f"Performance requirement: {match}")
        
        return requirements
    
    async def _identify_stakeholders(self, text: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify project stakeholders and their roles"""
        stakeholders = []
        
        # Common stakeholder patterns
        stakeholder_patterns = [
            r"(users?|customers?|clients?)",
            r"(administrators?|admins?)",
            r"(managers?|supervisors?)",
            r"(developers?|engineers?)",
            r"(testers?|QA)",
            r"(support staff|help desk)"
        ]
        
        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                stakeholder = {
                    "role": match.lower(),
                    "responsibilities": [],
                    "constraints": [],
                    "influence": "medium"
                }
                if stakeholder not in stakeholders:
                    stakeholders.append(stakeholder)
        
        return stakeholders
    
    async def _create_domain_model(self, text: str, functional_reqs: List[str], 
                                 stakeholders: List[Dict[str, Any]]) -> DomainModel:
        """Create a comprehensive domain model"""
        # Extract entities from requirements
        entities = []
        
        # Common entity patterns (nouns that represent business concepts)
        entity_patterns = [
            r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b",  # Capitalized nouns
            r"\b(user|customer|product|order|task|project|account|profile)\b"
        ]
        
        entity_names = set()
        for pattern in entity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                if len(match) > 2 and match.lower() not in ['the', 'and', 'for', 'with']:
                    entity_names.add(match.title())
        
        # Create entity objects
        for name in entity_names:
            entity = DomainEntity(
                name=name,
                attributes=self._extract_entity_attributes(name, text),
                business_rules=self._extract_entity_rules(name, functional_reqs),
                relationships=[],
                description=f"Domain entity representing {name}"
            )
            entities.append(entity)
        
        return DomainModel(
            entities=entities,
            relationships=[],
            business_rules=[],
            ubiquitous_language={},
            compliance_requirements=[],
            stakeholder_constraints=[]
        )
    
    def _extract_entity_attributes(self, entity_name: str, text: str) -> List[Dict[str, str]]:
        """Extract attributes for a specific entity"""
        attributes = []
        
        # Look for common attribute patterns
        attribute_patterns = [
            rf"{entity_name}\s+(?:has|contains|includes)\s+([^.]+)",
            rf"([a-z_]+)\s+(?:of|for)\s+{entity_name}",
            rf"{entity_name}['']s\s+([a-z_]+)"
        ]
        
        for pattern in attribute_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                attr_name = match.strip().lower().replace(' ', '_')
                if attr_name and len(attr_name) > 1:
                    attributes.append({
                        "name": attr_name,
                        "type": "string",  # Default type
                        "required": True,
                        "description": f"Attribute of {entity_name}"
                    })
        
        # Add common attributes if none found
        if not attributes:
            attributes = [
                {"name": "id", "type": "string", "required": True, "description": "Unique identifier"},
                {"name": "created_at", "type": "datetime", "required": True, "description": "Creation timestamp"},
                {"name": "updated_at", "type": "datetime", "required": True, "description": "Last update timestamp"}
            ]
        
        return attributes
    
    def _extract_entity_rules(self, entity_name: str, requirements: List[str]) -> List[str]:
        """Extract business rules for a specific entity"""
        rules = []
        
        for req in requirements:
            if entity_name.lower() in req.lower():
                # Extract rules that mention this entity
                rule_patterns = [
                    rf"{entity_name}\s+(?:must|shall|should)\s+([^.]+)",
                    rf"([^.]+)\s+for\s+{entity_name}",
                    rf"{entity_name}\s+(?:cannot|must not)\s+([^.]+)"
                ]
                
                for pattern in rule_patterns:
                    matches = re.findall(pattern, req, re.IGNORECASE)
                    rules.extend(matches)
        
        return [rule.strip() for rule in rules if rule.strip()]
    
    def _build_ubiquitous_language(self, entities: List[DomainEntity], 
                                 relationships: List[Dict[str, Any]], 
                                 business_rules: List[str]) -> Dict[str, str]:
        """Build ubiquitous language dictionary"""
        language = {}
        
        # Add entity definitions
        for entity in entities:
            language[entity.name] = entity.description
            
            # Add attribute definitions
            for attr in entity.attributes:
                key = f"{entity.name}.{attr['name']}"
                language[key] = attr.get('description', f"{attr['name']} of {entity.name}")
        
        # Add relationship definitions
        for rel in relationships:
            rel_name = f"{rel.get('from', '')}_{rel.get('type', '')}"
            language[rel_name] = rel.get('description', f"Relationship: {rel}")
        
        return language
    
    def _merge_duplicate_entities(self, entities: List[DomainEntity]) -> List[DomainEntity]:
        """Merge duplicate entities based on name similarity"""
        merged = {}
        
        for entity in entities:
            key = entity.name.lower()
            if key in merged:
                # Merge attributes and rules
                existing = merged[key]
                existing.attributes.extend(entity.attributes)
                existing.business_rules.extend(entity.business_rules)
                # Remove duplicates
                existing.attributes = list({attr['name']: attr for attr in existing.attributes}.values())
                existing.business_rules = list(set(existing.business_rules))
            else:
                merged[key] = entity
        
        return list(merged.values())
    
    async def _identify_entity_relationships(self, entities: List[DomainEntity]) -> List[Dict[str, Any]]:
        """Identify relationships between entities"""
        relationships = []
        
        # Simple relationship detection based on common patterns
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check for common relationship patterns
                if self._has_relationship(entity1, entity2):
                    relationship = {
                        "type": "association",
                        "from": entity1.name,
                        "to": entity2.name,
                        "cardinality": "many-to-many",
                        "description": f"Relationship between {entity1.name} and {entity2.name}"
                    }
                    relationships.append(relationship)
        
        return relationships
    
    def _has_relationship(self, entity1: DomainEntity, entity2: DomainEntity) -> bool:
        """Check if two entities have a relationship"""
        # Simple heuristic: check if one entity name appears in the other's attributes
        entity1_attrs = [attr['name'] for attr in entity1.attributes]
        entity2_attrs = [attr['name'] for attr in entity2.attributes]
        
        return (entity2.name.lower() in ' '.join(entity1_attrs).lower() or
                entity1.name.lower() in ' '.join(entity2_attrs).lower())
    
    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse a numbered list from text"""
        lines = text.split('\n')
        items = []
        
        for line in lines:
            line = line.strip()
            # Match numbered list items (1., 1), etc.)
            if re.match(r'^\d+[\.\)]\s+', line):
                item = re.sub(r'^\d+[\.\)]\s+', '', line)
                if item:
                    items.append(item)
        
        return items
    
    def _generate_recommendations(self, errors: List[str], warnings: List[str]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if "No functional requirements identified" in errors:
            recommendations.append("Review requirements document to identify system capabilities")
        
        if "No domain entities identified" in errors:
            recommendations.append("Analyze business requirements to identify key domain objects")
        
        if any("no business rules" in warning for warning in warnings):
            recommendations.append("Define business rules for each domain entity")
        
        return recommendations
    
    def _generate_analysis_reasoning(self, analysis: RequirementAnalysis) -> str:
        """Generate human-readable reasoning for the analysis"""
        entity_count = len(analysis.domain_model.entities)
        stakeholder_count = len(analysis.stakeholders)
        
        return (f"Analyzed requirements and identified {entity_count} domain entities "
                f"and {stakeholder_count} stakeholders. Domain model follows DDD principles "
                f"with clear separation of concerns and ubiquitous language.")
    
    # Additional helper methods for loading patterns and frameworks
    def _load_domain_patterns(self) -> Dict[str, Any]:
        """Load domain modeling patterns"""
        return {
            "aggregate_patterns": ["User-Profile", "Order-OrderItem", "Project-Task"],
            "value_object_patterns": ["Email", "Money", "Address"],
            "service_patterns": ["Authentication", "Notification", "Payment"]
        }
    
    def _load_compliance_frameworks(self) -> Dict[str, Any]:
        """Load compliance frameworks"""
        return {
            "GDPR": ["data_protection", "right_to_be_forgotten", "consent_management"],
            "HIPAA": ["data_encryption", "access_control", "audit_trail"],
            "SOX": ["financial_controls", "data_integrity", "audit_requirements"]
        }
    
    def _initialize_entity_extractors(self) -> Dict[str, Any]:
        """Initialize entity extraction tools"""
        return {
            "nlp_processor": "spacy_model",  # Placeholder for NLP processor
            "pattern_matcher": "regex_patterns",
            "ml_classifier": "entity_classifier_model"
        }
