"""
Model Tests for PATH Framework
Tests for all data models used across phases
"""


class TestArchitectureModels:
    """Test suite for Architecture phase data models"""
    
    def test_requirement_model(self):
        """Test Requirement data model"""
        from path_framework.models.arch_models import Requirement, RequirementType, RequirementPriority
        
        req = Requirement(
            title="Test Requirement",
            description="A test requirement",
            type=RequirementType.FUNCTIONAL,
            priority=RequirementPriority.HIGH
        )
        
        assert req.title == "Test Requirement"
        assert req.type == RequirementType.FUNCTIONAL
        assert req.priority == RequirementPriority.HIGH
        assert req.id is not None  # Should auto-generate UUID
    
    def test_domain_entity_model(self):
        """Test DomainEntity data model"""
        from path_framework.models.arch_models import DomainEntity
        
        entity = DomainEntity(
            name="User",
            description="System user entity",
            attributes={"id": "string", "name": "string"},
            behaviors=["create", "update", "delete"]
        )
        
        assert entity.name == "User"
        assert "id" in entity.attributes
        assert "create" in entity.behaviors
    
    def test_business_rule_model(self):
        """Test BusinessRule data model"""
        from path_framework.models.arch_models import BusinessRule, RequirementPriority
        
        rule = BusinessRule(
            name="Age Validation",
            description="User must be 18 or older",
            condition="user.age >= 18",
            action="allow_registration",
            priority=RequirementPriority.CRITICAL
        )
        
        assert rule.name == "Age Validation"
        assert rule.condition == "user.age >= 18"
        assert rule.priority == RequirementPriority.CRITICAL
    
    def test_system_architecture_model(self):
        """Test SystemArchitecture data model"""
        from path_framework.models.arch_models import SystemArchitecture, ArchitecturePattern
        
        arch = SystemArchitecture(
            name="Test Architecture",
            description="Test system architecture",
            pattern=ArchitecturePattern.MICROSERVICES
        )
        
        assert arch.name == "Test Architecture"
        assert arch.pattern == ArchitecturePattern.MICROSERVICES
        assert arch.id is not None
    
    def test_requirement_analysis_model(self):
        """Test RequirementAnalysis data model"""
        from path_framework.models.arch_models import RequirementAnalysis, Requirement
        
        req = Requirement(title="Test Req", description="Test requirement")
        analysis = RequirementAnalysis(
            project_name="Test Project",
            description="Test project analysis",
            requirements=[req]
        )
        
        assert analysis.project_name == "Test Project"
        assert len(analysis.requirements) == 1
        assert analysis.requirements[0].title == "Test Req"
