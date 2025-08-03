"""
Process Pillar Tests for Architecture Phase
Tests for workflows, quality gates, and validation components
"""


class TestArchitectureProcess:
    """Test suite for Architecture phase Process components"""
    
    def test_arch_workflows_exists(self):
        """Test that ArchWorkflows can be imported and instantiated"""
        from path_framework.phases.arch.process.workflows import ArchWorkflows
        
        workflows = ArchWorkflows()
        assert workflows is not None
        assert hasattr(workflows, 'start_workflow')
        assert hasattr(workflows, 'execute_step')
    
    def test_workflow_steps_defined(self):
        """Test that all required workflow steps are defined"""
        from path_framework.phases.arch.process.workflows import WorkflowStep
        
        expected_steps = [
            "context_analysis",
            "domain_modeling", 
            "architecture_design",
            "component_design",
            "integration_design",
            "validation",
            "documentation"
        ]
        
        actual_steps = [step.value for step in WorkflowStep]
        
        for step in expected_steps:
            assert step in actual_steps
    
    def test_quality_gates_exists(self):
        """Test that ArchQualityGates can be imported and instantiated"""
        from path_framework.phases.arch.process.quality_gates import ArchQualityGates
        
        quality_gates = ArchQualityGates()
        assert quality_gates is not None
        assert hasattr(quality_gates, 'validate_architecture')
    
    def test_validation_exists(self):
        """Test that ArchValidation can be imported and instantiated"""
        from path_framework.phases.arch.process.validation import ArchValidation
        
        validation = ArchValidation()
        assert validation is not None
        assert hasattr(validation, 'validate_design')
    
    def test_workflow_execution_flow(self):
        """Test the workflow execution flow"""
        from path_framework.phases.arch.process.workflows import ArchWorkflows, WorkflowStep
        
        workflows = ArchWorkflows()
        
        # Test workflow startup
        project_context = {"name": "test_project", "type": "web_app"}
        state = workflows.start_workflow(project_context)
        
        assert state is not None
        assert "project_context" in state
        
        # Test getting next step
        next_step = workflows.get_next_step()
        assert next_step == WorkflowStep.CONTEXT_ANALYSIS
        
        # Test workflow completion check
        assert not workflows.is_workflow_complete()
