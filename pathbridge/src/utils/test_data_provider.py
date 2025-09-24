"""Dynamic test data provider."""

import os
from typing import Dict, Any, List


class TestDataProvider:
    """Provide test data from multiple sources."""
    
    @staticmethod
    def get_user_story(domain: str = None) -> Dict[str, Any]:
        """Get user story based on environment or domain."""
        
        # Check environment variable first
        env_story = os.getenv("TEST_USER_STORY")
        if env_story:
            return {
                "story_id": "ENV-001",
                "user_story": env_story
            }
        
        # Domain-specific stories
        domain_stories = {
            "healthcare": "As a patient, I want to schedule appointments, so that I can receive medical care",
            "education": "As a student, I want to enroll in courses, so that I can complete my degree",
            "finance": "As a customer, I want to transfer money, so that I can pay bills",
            "default": "As a user, I want to perform an action, so that I can achieve a goal"
        }
        
        story_text = domain_stories.get(domain, domain_stories["default"])
        
        return {
            "story_id": f"{domain.upper()}-001" if domain else "DEFAULT-001",
            "user_story": story_text
        }
    
    @staticmethod
    def get_business_context(domain: str = None) -> str:
        """Get business context for domain."""
        contexts = {
            "healthcare": "Patient management system with appointment scheduling and medical records",
            "education": "Learning management system with course enrollment and progress tracking",
            "finance": "Banking system with account management and transaction processing",
            "default": "Generic business system with user management and data processing"
        }
        
        return contexts.get(domain, contexts["default"])