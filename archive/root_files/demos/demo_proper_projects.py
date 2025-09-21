#!/usr/bin/env python3
"""
PATH Framework Phase 1 Real Demo
Demonstrates proper project organization and artifact generation
"""

import json
from datetime import datetime
from pathlib import Path


def create_sample_project_artifacts():
    """Create sample Phase 1 artifacts for demonstration"""

    # Define project path in correct location
    project_path = Path("./projects/demo-ecommerce-platform")
    artifacts_path = project_path / "path_artifacts" / "arch"

    # Create directory structure
    artifacts_path.mkdir(parents=True, exist_ok=True)

    print("🚀 Creating Phase 1 artifacts for demo project")
    print(f"📁 Project: {project_path}")
    print(f"📄 Artifacts: {artifacts_path}")
    print("=" * 60)

    # 1. Requirements Analysis
    requirements = {
        "project_name": "EcoMart - Sustainable E-commerce Platform",
        "description": "A modern e-commerce platform focusing on sustainable products with microservices architecture",
        "project_type": "web_application",
        "target_users": [
            "eco-conscious consumers",
            "sustainable vendors",
            "platform administrators",
        ],
        "business_objectives": [
            "Enable sustainable product marketplace",
            "Support 10,000+ concurrent users",
            "Process 1M+ transactions/month",
            "Achieve 99.9% uptime",
            "Reduce carbon footprint by 30%",
        ],
        "functional_requirements": [
            {
                "id": "FR-001",
                "title": "User Authentication",
                "description": "Users must be able to register, login, and manage their accounts",
                "priority": "high",
                "acceptance_criteria": [
                    "User can register with email/password",
                    "User can login with valid credentials",
                    "User can reset forgotten password",
                    "User session expires after 24 hours",
                ],
            },
            {
                "id": "FR-002",
                "title": "Product Catalog",
                "description": "Browse and search sustainable products with detailed information",
                "priority": "high",
                "acceptance_criteria": [
                    "Display products with sustainability ratings",
                    "Filter by category, price, rating",
                    "Search by keywords",
                    "View detailed product information",
                ],
            },
            {
                "id": "FR-003",
                "title": "Shopping Cart",
                "description": "Add products to cart and proceed to checkout",
                "priority": "high",
                "acceptance_criteria": [
                    "Add/remove items from cart",
                    "Update quantities",
                    "Calculate totals with taxes",
                    "Save cart for later",
                ],
            },
        ],
        "non_functional_requirements": [
            {
                "id": "NFR-001",
                "title": "Performance",
                "description": "System must respond quickly to user interactions",
                "criteria": "Page load time < 2 seconds, API response < 200ms",
            },
            {
                "id": "NFR-002",
                "title": "Scalability",
                "description": "Support growing user base and transaction volume",
                "criteria": "Handle 10,000 concurrent users, 1M transactions/month",
            },
            {
                "id": "NFR-003",
                "title": "Security",
                "description": "Protect user data and payment information",
                "criteria": "PCI DSS compliance, GDPR compliance, encrypted data",
            },
        ],
        "constraints": [
            "Budget limit of $500K for initial development",
            "6-month development timeline",
            "Must integrate with existing payment systems",
            "Must support multiple languages (EN, ES, FR)",
        ],
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "requirements.json", "w") as f:
        json.dump(requirements, f, indent=2)
    print("✅ Requirements analysis complete")

    # 2. Domain Model
    domain_model = {
        "entities": [
            {
                "name": "User",
                "description": "Platform users including customers and vendors",
                "attributes": [
                    {"name": "id", "type": "UUID", "required": True},
                    {
                        "name": "email",
                        "type": "String",
                        "required": True,
                        "unique": True,
                    },
                    {"name": "password_hash", "type": "String", "required": True},
                    {"name": "first_name", "type": "String", "required": True},
                    {"name": "last_name", "type": "String", "required": True},
                    {
                        "name": "role",
                        "type": "Enum",
                        "values": ["customer", "vendor", "admin"],
                    },
                    {"name": "created_at", "type": "DateTime", "required": True},
                    {"name": "email_verified", "type": "Boolean", "default": False},
                ],
                "relationships": [
                    {
                        "type": "one_to_many",
                        "target": "Order",
                        "description": "User has many orders",
                    },
                    {
                        "type": "one_to_one",
                        "target": "Cart",
                        "description": "User has one active cart",
                    },
                    {
                        "type": "one_to_many",
                        "target": "Review",
                        "description": "User can write many reviews",
                    },
                ],
            },
            {
                "name": "Product",
                "description": "Sustainable products available in the marketplace",
                "attributes": [
                    {"name": "id", "type": "UUID", "required": True},
                    {"name": "name", "type": "String", "required": True},
                    {"name": "description", "type": "Text", "required": True},
                    {"name": "price", "type": "Decimal", "required": True},
                    {
                        "name": "sustainability_score",
                        "type": "Integer",
                        "min": 1,
                        "max": 10,
                    },
                    {"name": "category_id", "type": "UUID", "required": True},
                    {"name": "vendor_id", "type": "UUID", "required": True},
                    {"name": "stock_quantity", "type": "Integer", "required": True},
                    {
                        "name": "images",
                        "type": "Array[String]",
                        "description": "Product image URLs",
                    },
                ],
                "relationships": [
                    {
                        "type": "belongs_to",
                        "target": "Category",
                        "description": "Product belongs to category",
                    },
                    {
                        "type": "belongs_to",
                        "target": "Vendor",
                        "description": "Product belongs to vendor",
                    },
                    {
                        "type": "one_to_many",
                        "target": "Review",
                        "description": "Product has many reviews",
                    },
                ],
            },
            {
                "name": "Order",
                "description": "Customer purchase orders",
                "attributes": [
                    {"name": "id", "type": "UUID", "required": True},
                    {"name": "user_id", "type": "UUID", "required": True},
                    {
                        "name": "status",
                        "type": "Enum",
                        "values": [
                            "pending",
                            "confirmed",
                            "shipped",
                            "delivered",
                            "cancelled",
                        ],
                    },
                    {"name": "total_amount", "type": "Decimal", "required": True},
                    {"name": "created_at", "type": "DateTime", "required": True},
                    {"name": "shipping_address", "type": "JSON", "required": True},
                    {"name": "payment_id", "type": "UUID", "required": True},
                ],
                "relationships": [
                    {
                        "type": "belongs_to",
                        "target": "User",
                        "description": "Order belongs to user",
                    },
                    {
                        "type": "one_to_many",
                        "target": "OrderItem",
                        "description": "Order has many items",
                    },
                    {
                        "type": "one_to_one",
                        "target": "Payment",
                        "description": "Order has one payment",
                    },
                ],
            },
        ],
        "business_rules": [
            {
                "rule": "Sustainability Threshold",
                "description": "Products must have sustainability score >= 3 to be featured",
                "enforcement": "validation",
            },
            {
                "rule": "Free Shipping",
                "description": "Orders over $100 qualify for free shipping",
                "enforcement": "business_logic",
            },
            {
                "rule": "Vendor Verification",
                "description": "Vendors must be verified before selling products",
                "enforcement": "approval_workflow",
            },
            {
                "rule": "Stock Management",
                "description": "Cannot sell products with zero stock",
                "enforcement": "validation",
            },
        ],
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "domain_model.json", "w") as f:
        json.dump(domain_model, f, indent=2)
    print("✅ Domain model created")

    # 3. System Architecture
    architecture = {
        "architecture_pattern": "microservices",
        "architectural_style": "event_driven",
        "services": [
            {
                "name": "API Gateway",
                "type": "gateway",
                "technology": "Kong",
                "responsibilities": [
                    "Request routing",
                    "Authentication",
                    "Rate limiting",
                    "Load balancing",
                ],
                "endpoints": ["/*"],
            },
            {
                "name": "User Service",
                "type": "microservice",
                "technology": "Node.js + Express",
                "database": "PostgreSQL",
                "responsibilities": [
                    "User registration and authentication",
                    "Profile management",
                    "Role-based access control",
                ],
                "api_endpoints": [
                    "POST /users/register",
                    "POST /users/login",
                    "GET /users/{id}",
                    "PUT /users/{id}",
                    "DELETE /users/{id}",
                ],
            },
            {
                "name": "Product Service",
                "type": "microservice",
                "technology": "Python + FastAPI",
                "database": "PostgreSQL + Elasticsearch",
                "responsibilities": [
                    "Product catalog management",
                    "Search and filtering",
                    "Recommendation engine",
                ],
                "api_endpoints": [
                    "GET /products",
                    "GET /products/{id}",
                    "POST /products/search",
                    "GET /products/recommendations",
                ],
            },
            {
                "name": "Order Service",
                "type": "microservice",
                "technology": "Java + Spring Boot",
                "database": "PostgreSQL",
                "responsibilities": [
                    "Order processing",
                    "Workflow management",
                    "Inventory coordination",
                ],
                "api_endpoints": [
                    "POST /orders",
                    "GET /orders/{id}",
                    "PUT /orders/{id}/status",
                    "GET /users/{id}/orders",
                ],
            },
        ],
        "databases": [
            {
                "name": "user_db",
                "type": "PostgreSQL",
                "service": "User Service",
                "purpose": "User data and authentication",
            },
            {
                "name": "product_db",
                "type": "PostgreSQL",
                "service": "Product Service",
                "purpose": "Product catalog data",
            },
            {
                "name": "search_index",
                "type": "Elasticsearch",
                "service": "Product Service",
                "purpose": "Product search and analytics",
            },
        ],
        "messaging": {
            "broker": "Apache Kafka",
            "topics": [
                "user.events",
                "product.events",
                "order.events",
                "payment.events",
            ],
        },
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "architecture.json", "w") as f:
        json.dump(architecture, f, indent=2)
    print("✅ System architecture designed")

    # 4. Component Specifications
    components = {
        "services": [
            {
                "name": "User Service",
                "interfaces": [
                    {
                        "name": "UserRepository",
                        "methods": [
                            "create(user: User) -> User",
                            "findById(id: UUID) -> User",
                            "findByEmail(email: String) -> User",
                            "update(id: UUID, user: User) -> User",
                            "delete(id: UUID) -> Boolean",
                        ],
                    },
                    {
                        "name": "AuthService",
                        "methods": [
                            "authenticate(email: String, password: String) -> Token",
                            "validateToken(token: String) -> User",
                            "refreshToken(token: String) -> Token",
                        ],
                    },
                ],
                "dependencies": ["PostgreSQL Database", "Redis Cache", "Email Service"],
            }
        ],
        "shared_components": [
            {
                "name": "Common Authentication Library",
                "purpose": "Shared JWT token handling",
                "language": "TypeScript",
            },
            {
                "name": "Common Logging Library",
                "purpose": "Structured logging across services",
                "language": "TypeScript",
            },
            {
                "name": "Common Validation Library",
                "purpose": "Request/response validation",
                "language": "TypeScript",
            },
        ],
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "components.json", "w") as f:
        json.dump(components, f, indent=2)
    print("✅ Component design completed")

    # 5. Integration Design
    integration = {
        "integration_patterns": [
            {
                "name": "API Gateway Pattern",
                "purpose": "Single entry point for client requests",
                "implementation": "Kong with plugins for auth and rate limiting",
            },
            {
                "name": "Event Sourcing",
                "purpose": "Capture all state changes as events",
                "implementation": "Kafka event streams with event store",
            },
            {
                "name": "CQRS",
                "purpose": "Separate read/write operations",
                "implementation": "Separate read replicas and materialized views",
            },
        ],
        "api_specifications": [
            {
                "service": "User Service",
                "protocol": "REST",
                "format": "JSON",
                "authentication": "JWT Bearer tokens",
                "versioning": "URI versioning (/v1/users)",
            },
            {
                "service": "Product Service",
                "protocol": "GraphQL",
                "format": "JSON",
                "caching": "Redis with 1-hour TTL",
                "versioning": "Schema evolution",
            },
        ],
        "event_contracts": [
            {
                "event": "UserRegistered",
                "producer": "User Service",
                "consumers": ["Notification Service", "Analytics Service"],
                "schema": {
                    "user_id": "UUID",
                    "email": "String",
                    "registration_time": "DateTime",
                },
            },
            {
                "event": "OrderPlaced",
                "producer": "Order Service",
                "consumers": [
                    "Payment Service",
                    "Inventory Service",
                    "Notification Service",
                ],
                "schema": {
                    "order_id": "UUID",
                    "user_id": "UUID",
                    "items": "Array[OrderItem]",
                    "total_amount": "Decimal",
                },
            },
        ],
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "integration.json", "w") as f:
        json.dump(integration, f, indent=2)
    print("✅ Integration design completed")

    # 6. Validation Report
    validation = {
        "overall_score": 8.7,
        "validation_checks": [
            {
                "category": "SOLID Principles",
                "score": 9.0,
                "status": "PASSED",
                "details": "Single responsibility and dependency inversion well implemented",
            },
            {
                "category": "Scalability",
                "score": 8.5,
                "status": "PASSED",
                "details": "Microservices architecture supports horizontal scaling",
            },
            {
                "category": "Security",
                "score": 7.8,
                "status": "REVIEW_REQUIRED",
                "details": "Need to implement OAuth 2.0 and API rate limiting",
            },
            {
                "category": "Performance",
                "score": 9.2,
                "status": "PASSED",
                "details": "Caching strategy and database optimization in place",
            },
            {
                "category": "Maintainability",
                "score": 8.9,
                "status": "PASSED",
                "details": "Clear separation of concerns and well-defined interfaces",
            },
        ],
        "recommendations": [
            "Implement OAuth 2.0 for enhanced security",
            "Add comprehensive API documentation with OpenAPI",
            "Set up monitoring and alerting for all services",
            "Implement circuit breaker pattern for resilience",
        ],
        "risks": [
            {
                "description": "Data consistency across microservices",
                "mitigation": "Implement saga pattern for distributed transactions",
                "priority": "high",
            }
        ],
        "generated_at": datetime.now().isoformat(),
    }

    with open(artifacts_path / "validation_report.json", "w") as f:
        json.dump(validation, f, indent=2)
    print("✅ Validation completed")

    # 7. Documentation
    readme_content = f"""# EcoMart - Sustainable E-commerce Platform

## Architecture Overview
*Generated by PATH Framework Phase 1 on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

### Project Summary
- **Name**: {requirements["project_name"]}
- **Type**: {requirements["project_type"]}
- **Architecture**: {architecture["architecture_pattern"].title()} with {architecture["architectural_style"]}
- **Services**: {len(architecture["services"])} microservices
- **Quality Score**: {validation["overall_score"]}/10

### Business Objectives
{chr(10).join([f"- {obj}" for obj in requirements["business_objectives"]])}

### Functional Requirements
{chr(10).join([f"- **{req['id']}**: {req['title']}" for req in requirements["functional_requirements"]])}

### Domain Model
{chr(10).join([f"- **{entity['name']}**: {entity['description']}" for entity in domain_model["entities"]])}

### Microservices Architecture
{chr(10).join([f"- **{service['name']}**: {service['technology']}" for service in architecture["services"]])}

### Integration Patterns
{chr(10).join([f"- **{pattern['name']}**: {pattern['purpose']}" for pattern in integration["integration_patterns"]])}

### Quality Validation Results
{chr(10).join([f"- {check['category']}: {check['status']} ({check['score']}/10)" for check in validation["validation_checks"]])}

### Architecture Artifacts Generated
- ✅ `requirements.json` - Complete requirements analysis
- ✅ `domain_model.json` - Domain entities and business rules
- ✅ `architecture.json` - System architecture and service design
- ✅ `components.json` - Component specifications and interfaces
- ✅ `integration.json` - Integration patterns and API contracts
- ✅ `validation_report.json` - Quality validation and recommendations

### Next Phase: TDD Implementation
The architecture is ready for **Phase 2 - TDD Implementation**:
- All domain entities clearly defined
- Service interfaces and API contracts specified
- Integration patterns documented
- Quality gates established

Run the TDD phase with: `path tdd {requirements["project_name"]}`

---
*Generated by PATH Framework v2.0.0 - Process/AI/Technology/Human*
"""

    with open(artifacts_path / "README.md", "w") as f:
        f.write(readme_content)
    print("✅ Documentation generated")

    # Summary
    print("\n" + "=" * 60)
    print("🎉 PHASE 1 COMPLETE: Architecture & Software Engineering")
    print("=" * 60)
    print("📊 **Results Summary:**")
    print(f"   • Domain Entities: {len(domain_model['entities'])}")
    print(f"   • Microservices: {len(architecture['services'])}")
    print(
        f"   • API Endpoints: {sum(len(s.get('api_endpoints', [])) for s in architecture['services'])}"
    )
    print(f"   • Integration Patterns: {len(integration['integration_patterns'])}")
    print(f"   • Quality Score: {validation['overall_score']}/10")
    print("   • Artifacts Generated: 6 files")

    print("\n📁 **Project Location:**")
    print(f"   • Project: {project_path}")
    print(f"   • Artifacts: {artifacts_path}")

    print("\n🚀 **Ready for Phase 2 (TDD):**")
    print("   • Complete architecture specifications")
    print("   • Detailed component interfaces")
    print("   • Integration patterns and contracts")
    print("   • Quality validated and approved")

    return project_path, artifacts_path


if __name__ == "__main__":
    print("🚀 PATH Framework Phase 1 Demo - Proper Project Organization")
    print("=" * 80)
    project_path, artifacts_path = create_sample_project_artifacts()
    print(f"\n✅ Demo complete! Check artifacts in: {artifacts_path}")
