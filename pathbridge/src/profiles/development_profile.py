"""Development agent profile for PATH Framework."""

class DevelopmentProfile:
    """Profile for development-focused agents."""
    
    def __init__(self):
        self.name = "development"
        self.description = "General development agent profile"
        self.capabilities = [
            "file_operations",
            "code_generation", 
            "analysis_tools",
            "command_execution"
        ]
    
    def register_extended_capabilities(self, agent):
        """Register profile-specific capabilities."""
        # Development profile uses standard capabilities
        pass