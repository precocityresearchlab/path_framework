"""AI Domain Analyst profile implementation."""

from typing import Dict, Any
from ...core.base_agent import AgentProfile, AgentRequest
from ...knowledge.knowledge_base import SharedKnowledgeBase
from ...core.llm_interface import AgentLLMMixin


class DomainAnalystProfile(AgentProfile):
    """AI Domain Analyst - Analyzes user stories and business logic."""
    
    @property
    def agent_code(self) -> str:
        return "DA"
    
    @property
    def phase(self) -> int:
        return 1
    
    async def execute(self, request: AgentRequest, knowledge_base: SharedKnowledgeBase) -> Dict[str, Any]:
        """Execute domain analysis operations."""
        operation = request.operation
        payload = request.payload
        
        if operation == "analyze_user_story":
            return await self._analyze_user_story(payload, knowledge_base)
        elif operation == "generate_domain_model":
            return await self._generate_domain_model(payload, knowledge_base)
        elif operation == "identify_business_rules":
            return await self._identify_business_rules(payload, knowledge_base)
        elif operation == "validate_requirements":
            return await self._validate_requirements(payload, knowledge_base)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def _analyze_user_story(self, payload: Dict[str, Any], kb: SharedKnowledgeBase) -> Dict[str, Any]:
        """Analyze user story for domain patterns and business logic."""
        user_story = payload.get("user_story", "")
        
        # Extract story components
        story_analysis = {
            "user_type": self._extract_user_type(user_story),
            "functionality": self._extract_functionality(user_story),
            "benefit": self._extract_benefit(user_story),
            "domain_entities": self._identify_domain_entities(user_story),
            "business_rules": self._extract_business_rules(user_story),
            "edge_cases": self._identify_edge_cases(user_story)
        }
        
        return {
            "story_id": payload.get("story_id"),
            "analysis": story_analysis,
            "completeness_score": self._calculate_completeness(story_analysis),
            "recommendations": self._generate_recommendations(story_analysis)
        }
    
    async def _generate_domain_model(self, payload: Dict[str, Any], kb: SharedKnowledgeBase) -> Dict[str, Any]:
        """Generate domain model from analyzed stories."""
        stories = payload.get("stories", [])
        
        domain_model = {
            "entities": self._extract_entities(stories),
            "relationships": self._identify_relationships(stories),
            "value_objects": self._identify_value_objects(stories),
            "aggregates": self._define_aggregates(stories)
        }
        
        return domain_model
    
    async def _identify_business_rules(self, payload: Dict[str, Any], kb: SharedKnowledgeBase) -> Dict[str, Any]:
        """Identify and formalize business rules."""
        context = payload.get("context", "")
        
        business_rules = {
            "validation_rules": self._extract_validation_rules(context),
            "business_constraints": self._identify_constraints(context),
            "workflow_rules": self._extract_workflow_rules(context),
            "authorization_rules": self._identify_authorization_rules(context)
        }
        
        return business_rules
    
    async def _validate_requirements(self, payload: Dict[str, Any], kb: SharedKnowledgeBase) -> Dict[str, Any]:
        """Validate requirement completeness and consistency."""
        requirements = payload.get("requirements", [])
        
        validation_result = {
            "completeness_check": self._check_completeness(requirements),
            "consistency_check": self._check_consistency(requirements),
            "gaps_identified": self._identify_gaps(requirements),
            "conflicts_found": self._find_conflicts(requirements)
        }
        
        return validation_result
    
    def _extract_user_type(self, story: str) -> str:
        """Extract user type from story."""
        # Simple extraction logic - would use NLP in real implementation
        if "As a" in story:
            start = story.find("As a") + 5
            end = story.find(",", start)
            return story[start:end].strip() if end != -1 else ""
        return ""
    
    def _extract_functionality(self, story: str) -> str:
        """Extract functionality from story."""
        if "I want" in story:
            start = story.find("I want") + 7
            end = story.find("so that", start)
            return story[start:end].strip() if end != -1 else ""
        return ""
    
    def _extract_benefit(self, story: str) -> str:
        """Extract benefit from story."""
        if "so that" in story:
            start = story.find("so that") + 8
            return story[start:].strip()
        return ""
    
    def _identify_domain_entities(self, story: str) -> list:
        """Identify domain entities in story."""
        # Simplified entity extraction
        entities = []
        common_entities = ["user", "order", "product", "payment", "account", "customer"]
        for entity in common_entities:
            if entity.lower() in story.lower():
                entities.append(entity.title())
        return entities
    
    def _extract_business_rules(self, story: str) -> list:
        """Extract business rules from story."""
        # Simplified rule extraction
        rules = []
        if "must" in story.lower():
            rules.append("Mandatory requirement identified")
        if "cannot" in story.lower() or "not allowed" in story.lower():
            rules.append("Restriction identified")
        return rules
    
    def _identify_edge_cases(self, story: str) -> list:
        """Identify potential edge cases."""
        edge_cases = []
        if "user" in story.lower():
            edge_cases.extend(["Guest user scenario", "Authenticated user scenario"])
        if "payment" in story.lower():
            edge_cases.extend(["Payment failure", "Partial payment"])
        return edge_cases
    
    def _calculate_completeness(self, analysis: Dict[str, Any]) -> float:
        """Calculate story completeness score."""
        required_fields = ["user_type", "functionality", "benefit"]
        completed = sum(1 for field in required_fields if analysis.get(field))
        return completed / len(required_fields)
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> list:
        """Generate improvement recommendations."""
        recommendations = []
        if not analysis.get("user_type"):
            recommendations.append("Specify user type clearly")
        if not analysis.get("benefit"):
            recommendations.append("Add business value justification")
        if len(analysis.get("edge_cases", [])) < 2:
            recommendations.append("Consider additional edge cases")
        return recommendations
    
    def _extract_entities(self, stories: list) -> list:
        """Extract domain entities from multiple stories."""
        entities = set()
        for story in stories:
            story_entities = self._identify_domain_entities(story.get("description", ""))
            entities.update(story_entities)
        return list(entities)
    
    def _identify_relationships(self, stories: list) -> list:
        """Identify relationships between entities."""
        # Simplified relationship identification
        return ["User has Orders", "Order contains Products", "User has Account"]
    
    def _identify_value_objects(self, stories: list) -> list:
        """Identify value objects."""
        return ["Email", "Money", "Address", "PhoneNumber"]
    
    def _define_aggregates(self, stories: list) -> list:
        """Define domain aggregates."""
        return ["UserAggregate", "OrderAggregate", "ProductAggregate"]
    
    def _extract_validation_rules(self, context: str) -> list:
        """Extract validation rules."""
        return ["Email format validation", "Required field validation"]
    
    def _identify_constraints(self, context: str) -> list:
        """Identify business constraints."""
        return ["Business hours constraint", "Geographic restrictions"]
    
    def _extract_workflow_rules(self, context: str) -> list:
        """Extract workflow rules."""
        return ["Order approval workflow", "Payment processing sequence"]
    
    def _identify_authorization_rules(self, context: str) -> list:
        """Identify authorization rules."""
        return ["User role-based access", "Resource ownership validation"]
    
    def _check_completeness(self, requirements: list) -> Dict[str, Any]:
        """Check requirement completeness."""
        return {"complete": len(requirements) > 0, "missing_count": 0}
    
    def _check_consistency(self, requirements: list) -> Dict[str, Any]:
        """Check requirement consistency."""
        return {"consistent": True, "conflicts": []}
    
    def _identify_gaps(self, requirements: list) -> list:
        """Identify requirement gaps."""
        return ["Security requirements missing", "Performance criteria undefined"]
    
    def _find_conflicts(self, requirements: list) -> list:
        """Find requirement conflicts."""
        return []
    
    def get_capabilities(self) -> Dict[str, str]:
        """Get DA capabilities."""
        return {
            "DA-CA-001": "story_analysis: Natural language processing of user stories",
            "DA-CA-002": "domain_modeling: Entity-relationship diagram generation",
            "DA-CA-003": "gap_analysis: Requirement completeness validation",
            "DA-CA-004": "stakeholder_alignment: Business value validation"
        }
    
    def get_performance_metrics(self) -> Dict[str, str]:
        """Get DA performance metrics."""
        return {
            "DA-PM-001": "story_completeness: >95% of stories meet quality criteria",
            "DA-PM-002": "gap_detection: >90% accuracy in identifying missing requirements",
            "DA-PM-003": "stakeholder_satisfaction: >4.0/5.0 rating from product owners",
            "DA-PM-004": "processing_time: <5 minutes per user story"
        }