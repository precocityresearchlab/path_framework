"""Technology Components for Architecture Phase

This module provides comprehensive technology tools and frameworks for architecture design,
covering architecture patterns, modeling tools, design frameworks, and technology assessment.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from path_framework.models.arch_models import SystemArchitecture


class ArchitecturePatternType(Enum):
    """Types of architecture patterns"""

    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    MICROSERVICES = "microservices"
    EVENT_DRIVEN = "event_driven"
    SERVERLESS = "serverless"
    MVC = "mvc"
    MVP = "mvp"
    MVVM = "mvvm"
    CLEAN = "clean"
    ONION = "onion"


class TechnologyCategory(Enum):
    """Technology categories for assessment"""

    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"
    MESSAGING = "messaging"
    CACHING = "caching"
    MONITORING = "monitoring"
    SECURITY = "security"
    DEPLOYMENT = "deployment"
    TESTING = "testing"


@dataclass
class ArchitecturePattern:
    """Architecture pattern definition"""

    name: str
    pattern_type: ArchitecturePatternType
    description: str
    benefits: list[str] = field(default_factory=list)
    drawbacks: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)
    implementation_guidelines: dict[str, Any] = field(default_factory=dict)
    technology_requirements: list[str] = field(default_factory=list)


@dataclass
class TechnologyAssessment:
    """Technology assessment result"""

    technology: str
    category: TechnologyCategory
    score: float  # 0-10 scale
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    compatibility: dict[str, str] = field(default_factory=dict)
    learning_curve: str = "medium"  # low, medium, high
    community_support: str = "good"  # poor, fair, good, excellent
    maturity: str = "stable"  # experimental, alpha, beta, stable, mature


class ArchitectureTools:
    """Architecture design tools and utilities"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._patterns = self._load_architecture_patterns()
        self._tech_database = self._load_technology_database()

    def _load_architecture_patterns(self) -> dict[str, ArchitecturePattern]:
        """Load predefined architecture patterns"""
        patterns = {
            "layered": ArchitecturePattern(
                name="Layered Architecture",
                pattern_type=ArchitecturePatternType.LAYERED,
                description="Organizes system into horizontal layers with specific responsibilities",
                benefits=[
                    "Clear separation of concerns",
                    "Easy to understand and maintain",
                    "Good for team specialization",
                    "Well-established pattern",
                ],
                drawbacks=[
                    "Can become monolithic",
                    "Performance overhead from layer crossing",
                    "Potential for god objects",
                    "Tight coupling between layers",
                ],
                use_cases=[
                    "Traditional enterprise applications",
                    "CRUD-heavy applications",
                    "Applications with clear business layers",
                ],
                implementation_guidelines={
                    "presentation_layer": "UI components, controllers, view models",
                    "business_layer": "Business logic, domain services, rules",
                    "data_layer": "Data access, repositories, persistence",
                    "cross_cutting": "Logging, security, caching",
                },
                technology_requirements=[
                    "Framework supporting layered architecture",
                    "ORM",
                    "DI container",
                ],
            ),
            "hexagonal": ArchitecturePattern(
                name="Hexagonal Architecture (Ports & Adapters)",
                pattern_type=ArchitecturePatternType.HEXAGONAL,
                description="Isolates core business logic from external concerns using ports and adapters",
                benefits=[
                    "High testability",
                    "Technology independence",
                    "Clear boundaries",
                    "Easy to change external dependencies",
                ],
                drawbacks=[
                    "Initial complexity",
                    "More code to write",
                    "Learning curve for teams",
                    "Overkill for simple applications",
                ],
                use_cases=[
                    "Domain-rich applications",
                    "Applications requiring high testability",
                    "Systems with multiple external integrations",
                ],
                implementation_guidelines={
                    "domain_core": "Pure business logic, no external dependencies",
                    "ports": "Interfaces defining contracts",
                    "adapters": "Implementations of ports for external systems",
                    "application_services": "Orchestrate domain operations",
                },
                technology_requirements=[
                    "Dependency injection",
                    "Interface/contract support",
                    "Mocking frameworks",
                ],
            ),
            "microservices": ArchitecturePattern(
                name="Microservices Architecture",
                pattern_type=ArchitecturePatternType.MICROSERVICES,
                description="Decomposes application into small, independent, deployable services",
                benefits=[
                    "Independent deployment",
                    "Technology diversity",
                    "Scalability",
                    "Team autonomy",
                    "Fault isolation",
                ],
                drawbacks=[
                    "Distributed system complexity",
                    "Network latency",
                    "Data consistency challenges",
                    "Operational overhead",
                    "Testing complexity",
                ],
                use_cases=[
                    "Large-scale applications",
                    "Multiple team organizations",
                    "High scalability requirements",
                    "Different technology needs per service",
                ],
                implementation_guidelines={
                    "service_boundaries": "Business capability based",
                    "communication": "HTTP/REST, messaging, events",
                    "data_management": "Database per service",
                    "deployment": "Containerized, automated CI/CD",
                },
                technology_requirements=[
                    "Container platform",
                    "API gateway",
                    "Service mesh",
                    "Monitoring tools",
                ],
            ),
        }

        return patterns

    def _load_technology_database(self) -> dict[str, list[TechnologyAssessment]]:
        """Load technology assessment database"""
        return {
            "backend": [
                TechnologyAssessment(
                    technology="Python/FastAPI",
                    category=TechnologyCategory.BACKEND,
                    score=8.5,
                    pros=[
                        "Fast development",
                        "Excellent async support",
                        "Great documentation",
                        "Type hints",
                    ],
                    cons=["Performance limitations", "GIL for CPU tasks"],
                    compatibility={
                        "frontend": "excellent",
                        "database": "excellent",
                        "cloud": "excellent",
                    },
                    learning_curve="medium",
                    community_support="excellent",
                    maturity="stable",
                ),
                TechnologyAssessment(
                    technology="Node.js/Express",
                    category=TechnologyCategory.BACKEND,
                    score=8.0,
                    pros=[
                        "JavaScript everywhere",
                        "Large ecosystem",
                        "Good performance",
                        "Event-driven",
                    ],
                    cons=[
                        "Callback complexity",
                        "Single-threaded",
                        "Rapid ecosystem changes",
                    ],
                    compatibility={
                        "frontend": "excellent",
                        "database": "good",
                        "cloud": "excellent",
                    },
                    learning_curve="medium",
                    community_support="excellent",
                    maturity="stable",
                ),
                TechnologyAssessment(
                    technology="Java/Spring Boot",
                    category=TechnologyCategory.BACKEND,
                    score=8.8,
                    pros=[
                        "Enterprise ready",
                        "Excellent tooling",
                        "Strong typing",
                        "Performance",
                    ],
                    cons=["Verbose syntax", "Memory usage", "Slow startup"],
                    compatibility={
                        "frontend": "good",
                        "database": "excellent",
                        "cloud": "excellent",
                    },
                    learning_curve="high",
                    community_support="excellent",
                    maturity="mature",
                ),
            ],
            "frontend": [
                TechnologyAssessment(
                    technology="React",
                    category=TechnologyCategory.FRONTEND,
                    score=9.0,
                    pros=[
                        "Large ecosystem",
                        "Component reusability",
                        "Virtual DOM",
                        "Strong community",
                    ],
                    cons=["Learning curve", "Rapid changes", "JSX complexity"],
                    compatibility={
                        "backend": "excellent",
                        "mobile": "good",
                        "desktop": "good",
                    },
                    learning_curve="medium",
                    community_support="excellent",
                    maturity="stable",
                ),
                TechnologyAssessment(
                    technology="Vue.js",
                    category=TechnologyCategory.FRONTEND,
                    score=8.5,
                    pros=[
                        "Easy learning curve",
                        "Good documentation",
                        "Template syntax",
                        "Progressive adoption",
                    ],
                    cons=[
                        "Smaller ecosystem",
                        "Less job market",
                        "Single maintainer risk",
                    ],
                    compatibility={
                        "backend": "excellent",
                        "mobile": "fair",
                        "desktop": "fair",
                    },
                    learning_curve="low",
                    community_support="good",
                    maturity="stable",
                ),
            ],
            "database": [
                TechnologyAssessment(
                    technology="PostgreSQL",
                    category=TechnologyCategory.DATABASE,
                    score=9.2,
                    pros=[
                        "ACID compliance",
                        "Advanced features",
                        "JSON support",
                        "Extensible",
                    ],
                    cons=["Memory usage", "Complexity for simple use cases"],
                    compatibility={
                        "backend": "excellent",
                        "cloud": "excellent",
                        "scaling": "good",
                    },
                    learning_curve="medium",
                    community_support="excellent",
                    maturity="mature",
                ),
                TechnologyAssessment(
                    technology="MongoDB",
                    category=TechnologyCategory.DATABASE,
                    score=7.8,
                    pros=[
                        "Flexible schema",
                        "Horizontal scaling",
                        "JSON documents",
                        "Fast development",
                    ],
                    cons=[
                        "Data consistency",
                        "Memory usage",
                        "Learning curve for SQL developers",
                    ],
                    compatibility={
                        "backend": "excellent",
                        "cloud": "excellent",
                        "scaling": "excellent",
                    },
                    learning_curve="medium",
                    community_support="excellent",
                    maturity="stable",
                ),
            ],
        }

    def get_pattern(self, pattern_name: str) -> ArchitecturePattern | None:
        """Get architecture pattern by name"""
        return self._patterns.get(pattern_name.lower())

    def list_patterns(self) -> list[ArchitecturePattern]:
        """List all available architecture patterns"""
        return list(self._patterns.values())

    def recommend_patterns(
        self, requirements: dict[str, Any]
    ) -> list[ArchitecturePattern]:
        """Recommend architecture patterns based on requirements"""
        recommended = []

        # Simple rule-based recommendation
        if requirements.get("team_size", 1) > 10:
            recommended.append(self._patterns["microservices"])

        if requirements.get("complexity", "low") == "high":
            recommended.append(self._patterns["hexagonal"])

        if requirements.get("type", "web") == "enterprise":
            recommended.append(self._patterns["layered"])

        # Default recommendation
        if not recommended:
            recommended.append(self._patterns["layered"])

        return recommended

    def assess_technology_stack(
        self, requirements: dict[str, Any]
    ) -> dict[str, list[TechnologyAssessment]]:
        """Assess and recommend technology stack"""
        recommendations = {}

        for category, technologies in self._tech_database.items():
            # Filter and score based on requirements
            scored_techs = []
            for tech in technologies:
                score = self._calculate_compatibility_score(tech, requirements)
                tech_copy = TechnologyAssessment(**tech.__dict__)
                tech_copy.score = score
                scored_techs.append(tech_copy)

            # Sort by score and take top recommendations
            scored_techs.sort(key=lambda x: x.score, reverse=True)
            recommendations[category] = scored_techs[:3]  # Top 3 per category

        return recommendations

    def _calculate_compatibility_score(
        self, tech: TechnologyAssessment, requirements: dict[str, Any]
    ) -> float:
        """Calculate compatibility score based on requirements"""
        base_score = tech.score

        # Adjust based on requirements
        if (
            requirements.get("performance", "medium") == "high"
            and "performance" in tech.pros
        ):
            base_score += 0.5

        if (
            requirements.get("team_experience", "medium") == "low"
            and tech.learning_curve == "low"
        ):
            base_score += 0.3

        if requirements.get("enterprise", False) and tech.maturity == "mature":
            base_score += 0.4

        return min(base_score, 10.0)

    def generate_architecture_diagram_config(
        self, architecture: SystemArchitecture
    ) -> dict[str, Any]:
        """Generate configuration for architecture diagram tools"""
        return {
            "components": [
                {
                    "id": comp.component_id,
                    "name": comp.name,
                    "type": comp.component_type,
                    "layer": getattr(comp, "layer", "application"),
                    "technologies": comp.technologies,
                }
                for comp in architecture.components
            ],
            "relationships": [
                {
                    "from": rel.source_component_id,
                    "to": rel.target_component_id,
                    "type": rel.relationship_type,
                    "description": rel.description,
                }
                for rel in architecture.relationships
            ],
            "layers": ["presentation", "business", "data"],
            "styling": {
                "theme": "modern",
                "layout": "layered",
                "colors": {
                    "presentation": "#4CAF50",
                    "business": "#2196F3",
                    "data": "#FF9800",
                },
            },
        }


class DesignPatterns:
    """Design pattern library and guidance"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._patterns = self._load_design_patterns()

    def _load_design_patterns(self) -> dict[str, dict[str, Any]]:
        """Load design patterns database"""
        return {
            "singleton": {
                "category": "creational",
                "intent": "Ensure a class has only one instance and provide global access",
                "use_cases": [
                    "Configuration management",
                    "Logging",
                    "Database connections",
                ],
                "implementation": {
                    "python": """
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
                    """,
                    "javascript": """
class Singleton {
    constructor() {
        if (Singleton.instance) {
            return Singleton.instance;
        }
        Singleton.instance = this;
    }
}
                    """,
                },
                "pros": ["Controlled instance creation", "Global access"],
                "cons": ["Global state", "Testing difficulties", "Tight coupling"],
            },
            "factory": {
                "category": "creational",
                "intent": "Create objects without specifying exact classes",
                "use_cases": [
                    "Object creation abstraction",
                    "Plugin systems",
                    "Framework development",
                ],
                "implementation": {
                    "python": """
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
        raise ValueError(f"Unknown shape: {shape_type}")
                    """
                },
                "pros": ["Loose coupling", "Extensibility", "Code reuse"],
                "cons": ["Complexity increase", "More classes"],
            },
            "observer": {
                "category": "behavioral",
                "intent": "Define one-to-many dependency between objects",
                "use_cases": [
                    "Event systems",
                    "Model-View architectures",
                    "Reactive programming",
                ],
                "implementation": {
                    "python": """
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
                    """
                },
                "pros": ["Loose coupling", "Dynamic relationships", "Event handling"],
                "cons": [
                    "Memory leaks risk",
                    "Order dependencies",
                    "Performance impact",
                ],
            },
            "strategy": {
                "category": "behavioral",
                "intent": "Define family of algorithms and make them interchangeable",
                "use_cases": [
                    "Payment processing",
                    "Sorting algorithms",
                    "Validation rules",
                ],
                "implementation": {
                    "python": """
class PaymentStrategy:
    def pay(self, amount): pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} with credit card"

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        return f"Paid ${amount} with PayPal"
                    """
                },
                "pros": [
                    "Runtime algorithm selection",
                    "Code reuse",
                    "Open/closed principle",
                ],
                "cons": ["Increased complexity", "More classes", "Client awareness"],
            },
        }

    def get_pattern(self, pattern_name: str) -> dict[str, Any] | None:
        """Get design pattern information"""
        return self._patterns.get(pattern_name.lower())

    def list_patterns_by_category(self, category: str) -> list[dict[str, Any]]:
        """List patterns by category (creational, structural, behavioral)"""
        return [
            {"name": name, **pattern}
            for name, pattern in self._patterns.items()
            if pattern["category"] == category.lower()
        ]

    def recommend_patterns(self, problem_description: str) -> list[dict[str, Any]]:
        """Recommend patterns based on problem description"""
        keywords = problem_description.lower()
        recommendations = []

        if "event" in keywords or "notification" in keywords:
            recommendations.append({"name": "observer", **self._patterns["observer"]})

        if "algorithm" in keywords or "strategy" in keywords or "payment" in keywords:
            recommendations.append({"name": "strategy", **self._patterns["strategy"]})

        if (
            "creation" in keywords
            or "factory" in keywords
            or "instantiation" in keywords
        ):
            recommendations.append({"name": "factory", **self._patterns["factory"]})

        if "single instance" in keywords or "global" in keywords:
            recommendations.append({"name": "singleton", **self._patterns["singleton"]})

        return recommendations


class ModelingFrameworks:
    """Modeling framework tools and utilities"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_domain_model(
        self, domain_entities: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Generate domain model representation"""
        model = {
            "entities": [],
            "relationships": [],
            "value_objects": [],
            "aggregates": [],
        }

        for entity in domain_entities:
            model["entities"].append(
                {
                    "name": entity["name"],
                    "attributes": entity.get("attributes", []),
                    "methods": entity.get("methods", []),
                    "rules": entity.get("business_rules", []),
                }
            )

        return model

    def generate_c4_model(
        self, system_architecture: SystemArchitecture
    ) -> dict[str, Any]:
        """Generate C4 model representation"""
        return {
            "level1_context": {
                "system": system_architecture.system_name,
                "users": ["End Users", "Administrators"],
                "external_systems": ["External APIs", "Third-party Services"],
            },
            "level2_containers": [
                {
                    "name": comp.name,
                    "type": comp.component_type,
                    "technology": (
                        comp.technologies[0] if comp.technologies else "Unknown"
                    ),
                    "description": comp.description,
                }
                for comp in system_architecture.components
            ],
            "level3_components": [
                {"container": comp.name, "components": comp.interfaces}
                for comp in system_architecture.components
                if comp.interfaces
            ],
        }

    def export_to_plantuml(self, model_data: dict[str, Any]) -> str:
        """Export model to PlantUML format"""
        plantuml = "@startuml\n"

        if "entities" in model_data:
            for entity in model_data["entities"]:
                plantuml += f"class {entity['name']} {{\n"
                for attr in entity.get("attributes", []):
                    plantuml += f"  {attr}\n"
                for method in entity.get("methods", []):
                    plantuml += f"  {method}()\n"
                plantuml += "}\n\n"

        plantuml += "@enduml"
        return plantuml

    def export_to_mermaid(self, model_data: dict[str, Any]) -> str:
        """Export model to Mermaid format"""
        mermaid = "graph TD\n"

        if "components" in model_data:
            for comp in model_data["components"]:
                mermaid += f"  {comp['id']}[{comp['name']}]\n"

        if "relationships" in model_data:
            for rel in model_data["relationships"]:
                mermaid += f"  {rel['from']} --> {rel['to']}\n"

        return mermaid
