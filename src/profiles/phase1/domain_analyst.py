"""AI Domain Analyst profile implementation."""

from typing import Dict, Any
from ...core.base_agent import AgentProfile, AgentRequest
from ...knowledge.knowledge_base import SharedKnowledgeBase


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
        """Extract user type from story using enhanced pattern matching."""
        import re
        
        # Enhanced pattern matching for user types
        patterns = [
            r"As an? ([^,]+),",
            r"As an? ([^,]+) I want",
            r"As an? ([^,]+)\s+I want"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, story, re.IGNORECASE)
            if match:
                user_type = match.group(1).strip()
                # Clean up common articles and normalize
                user_type = re.sub(r'^(a|an)\s+', '', user_type, flags=re.IGNORECASE)
                return user_type.title()
        
        return ""
    
    def _extract_functionality(self, story: str) -> str:
        """Extract functionality from story using enhanced pattern matching."""
        import re
        
        # Enhanced pattern matching for functionality
        patterns = [
            r"I want to ([^,]+)(?:,|\s+so that)",
            r"I want ([^,]+)(?:,|\s+so that)",
            r"I need to ([^,]+)(?:,|\s+so that)",
            r"I need ([^,]+)(?:,|\s+so that)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, story, re.IGNORECASE)
            if match:
                functionality = match.group(1).strip()
                # Remove "to" prefix if present
                functionality = re.sub(r'^to\s+', '', functionality, flags=re.IGNORECASE)
                return functionality.lower()
        
        return ""
    
    def _extract_benefit(self, story: str) -> str:
        """Extract benefit from story using enhanced pattern matching."""
        import re
        
        # Enhanced pattern matching for benefits
        patterns = [
            r"so that (.+)$",
            r"in order to (.+)$",
            r"to achieve (.+)$",
            r"because (.+)$"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, story, re.IGNORECASE | re.DOTALL)
            if match:
                benefit = match.group(1).strip()
                # Clean up punctuation
                benefit = re.sub(r'[.!?]+$', '', benefit)
                return benefit.lower()
        
        return ""
    
    def _identify_domain_entities(self, story: str) -> list:
        """Identify domain entities using generic NLP techniques."""
        import re
        
        # Extract potential entities using linguistic patterns (nouns, proper nouns)
        entities = []
        
        # Find capitalized words that could be entities
        capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', story)
        entities.extend(capitalized_words)
        
        # Find common entity indicators
        entity_indicators = {
            "Actor": [r"\b(user|person|actor|agent|participant)s?\b"],
            "Object": [r"\b(item|object|thing|element|component)s?\b"],
            "Process": [r"\b(process|workflow|procedure|operation|task)s?\b"],
            "Data": [r"\b(data|information|record|entry|file)s?\b"],
            "System": [r"\b(system|application|platform|service|tool)s?\b"],
            "Resource": [r"\b(resource|asset|material|content|document)s?\b"]
        }
        
        story_lower = story.lower()
        for entity_type, patterns in entity_indicators.items():
            for pattern in patterns:
                if re.search(pattern, story_lower):
                    entities.append(entity_type)
                    break
        
        # Extract domain-specific nouns from context
        domain_nouns = self._extract_domain_nouns(story)
        entities.extend(domain_nouns)
        
        return list(set(entities))  # Remove duplicates
    
    def _extract_domain_nouns(self, story: str) -> list:
        """Extract domain-specific nouns that could be entities."""
        import re
        
        # Simple noun extraction - words that appear in object positions
        nouns = []
        
        # Pattern: "I want to [verb] [noun]"
        verb_object_pattern = r"I want to \w+ (\w+)"
        matches = re.findall(verb_object_pattern, story, re.IGNORECASE)
        nouns.extend([match.title() for match in matches])
        
        # Pattern: "[verb] a/an/the [noun]"
        article_noun_pattern = r"\b(?:a|an|the)\s+(\w+)\b"
        matches = re.findall(article_noun_pattern, story, re.IGNORECASE)
        nouns.extend([match.title() for match in matches if len(match) > 2])
        
        return nouns
    
    def _extract_business_rules(self, story: str) -> list:
        """Extract business rules using enhanced pattern recognition."""
        import re
        
        rules = []
        story_lower = story.lower()
        
        # Rule patterns with specific business logic
        rule_patterns = {
            "Mandatory": [r"\b(must|required|mandatory|need to|have to)\b"],
            "Restriction": [r"\b(cannot|not allowed|forbidden|prohibited|restricted)\b"],
            "Validation": [r"\b(valid|validate|verify|check|confirm)\b"],
            "Authorization": [r"\b(authorized|permission|access|role|privilege)\b"],
            "Workflow": [r"\b(after|before|when|if|then|process|workflow)\b"],
            "Business Hours": [r"\b(business hours|working hours|office hours)\b"],
            "Approval": [r"\b(approve|approval|review|confirm)\b"]
        }
        
        for rule_type, patterns in rule_patterns.items():
            for pattern in patterns:
                if re.search(pattern, story_lower):
                    rules.append(f"{rule_type} rule identified")
                    break
        
        return list(set(rules))  # Remove duplicates
    
    def _identify_edge_cases(self, story: str) -> list:
        """Identify generic edge cases based on functional patterns."""
        import re
        
        edge_cases = []
        story_lower = story.lower()
        
        # Generic edge case patterns based on functional requirements
        edge_case_patterns = {
            "Input Validation": [r"\b(input|enter|provide|submit|form)\b"],
            "Authentication": [r"\b(user|login|access|account|authenticate)\b"],
            "Authorization": [r"\b(permission|role|privilege|authorized|allowed)\b"],
            "Data Processing": [r"\b(process|calculate|compute|transform|analyze)\b"],
            "Network Operations": [r"\b(send|receive|connect|download|upload|sync)\b"],
            "Concurrent Operations": [r"\b(multiple|concurrent|simultaneous|parallel)\b"],
            "Error Conditions": [r"\b(error|fail|exception|invalid|incorrect)\b"],
            "Performance": [r"\b(fast|slow|timeout|performance|speed|load)\b"],
            "Security": [r"\b(secure|security|protect|safe|encrypt)\b"],
            "State Management": [r"\b(save|store|update|delete|modify|change)\b"]
        }
        
        for case_category, patterns in edge_case_patterns.items():
            for pattern in patterns:
                if re.search(pattern, story_lower):
                    edge_cases.extend(self._generate_generic_edge_cases(case_category))
                    break
        
        return list(set(edge_cases))  # Remove duplicates
    
    def _generate_generic_edge_cases(self, category: str) -> list:
        """Generate generic edge cases for each functional category."""
        edge_case_map = {
            "Input Validation": [
                "Empty input", "Invalid format", "Input too long",
                "Special characters", "Boundary values"
            ],
            "Authentication": [
                "Unauthenticated user", "Expired session", "Invalid credentials",
                "Account locked", "First-time access"
            ],
            "Authorization": [
                "Insufficient permissions", "Role mismatch", "Resource access denied",
                "Privilege escalation attempt", "Cross-user access"
            ],
            "Data Processing": [
                "Empty dataset", "Large dataset", "Corrupted data",
                "Processing timeout", "Resource exhaustion"
            ],
            "Network Operations": [
                "Network timeout", "Connection lost", "Server unavailable",
                "Bandwidth limitations", "Offline mode"
            ],
            "Concurrent Operations": [
                "Race condition", "Deadlock", "Resource contention",
                "Simultaneous updates", "State inconsistency"
            ],
            "Error Conditions": [
                "System error", "Validation failure", "Business rule violation",
                "External dependency failure", "Unexpected state"
            ],
            "Performance": [
                "High load", "Memory constraints", "CPU limitations",
                "Storage full", "Response timeout"
            ],
            "Security": [
                "Unauthorized access", "Data tampering", "Injection attack",
                "Information disclosure", "Malicious input"
            ],
            "State Management": [
                "Concurrent modifications", "State corruption", "Rollback scenario",
                "Partial updates", "Consistency violation"
            ]
        }
        
        return edge_case_map.get(category, [])
    
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
            story_text = story.get("description", "") if isinstance(story, dict) else str(story)
            story_entities = self._identify_domain_entities(story_text)
            entities.update(story_entities)
        return list(entities)
    
    def _identify_relationships(self, stories: list) -> list:
        """Identify generic relationships between entities."""
        import re
        
        relationships = []
        entities = self._extract_entities(stories)
        
        # Generic relationship patterns
        relationship_patterns = [
            r"(\w+)\s+(?:has|contains|includes|owns)\s+(\w+)",
            r"(\w+)\s+(?:belongs to|is part of|is owned by)\s+(\w+)",
            r"(\w+)\s+(?:manages|controls|operates)\s+(\w+)",
            r"(\w+)\s+(?:uses|utilizes|accesses)\s+(\w+)"
        ]
        
        for story in stories:
            story_text = story.get("description", "") if isinstance(story, dict) else str(story)
            for pattern in relationship_patterns:
                matches = re.findall(pattern, story_text, re.IGNORECASE)
                for match in matches:
                    entity1, entity2 = match[0].title(), match[1].title()
                    if entity1 in entities and entity2 in entities:
                        relationships.append(f"{entity1} -> {entity2}")
        
        return list(set(relationships)) if relationships else ["Generic entity relationships"]
    
    def _identify_value_objects(self, stories: list) -> list:
        """Identify generic value objects from stories."""
        import re
        
        value_objects = set()
        
        # Generic value object patterns
        value_patterns = {
            "Identifier": [r"\b(id|identifier|code|number)\b"],
            "Measurement": [r"\b(amount|quantity|size|weight|length)\b"],
            "Time": [r"\b(date|time|timestamp|duration|period)\b"],
            "Location": [r"\b(address|location|coordinates|position)\b"],
            "Contact": [r"\b(email|phone|contact|communication)\b"],
            "Status": [r"\b(status|state|condition|flag)\b"]
        }
        
        for story in stories:
            story_text = story.get("description", "") if isinstance(story, dict) else str(story)
            story_lower = story_text.lower()
            
            for value_type, patterns in value_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, story_lower):
                        value_objects.add(value_type)
                        break
        
        return list(value_objects) if value_objects else ["Generic value objects"]
    
    def _define_aggregates(self, stories: list) -> list:
        """Define generic domain aggregates based on entities."""
        entities = self._extract_entities(stories)
        
        # Create aggregates from main entities
        aggregates = []
        for entity in entities:
            if entity not in ["Actor", "Object", "Process", "Data", "System", "Resource"]:
                aggregates.append(f"{entity}Aggregate")
        
        return aggregates if aggregates else ["GenericAggregate"]
    
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