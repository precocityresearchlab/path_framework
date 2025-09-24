"""Story loader utility for dynamic test data."""

import yaml
from pathlib import Path
from typing import Dict, List, Any


class StoryLoader:
    """Load user stories from external configuration."""
    
    def __init__(self, config_path: str = "config/user_stories.yaml"):
        self.config_path = Path(config_path)
    
    def load_stories(self) -> List[Dict[str, Any]]:
        """Load all user stories from config."""
        with open(self.config_path) as f:
            data = yaml.safe_load(f)
        return data.get("user_stories", [])
    
    def load_test_scenarios(self) -> Dict[str, Any]:
        """Load test scenarios from config."""
        with open(self.config_path) as f:
            data = yaml.safe_load(f)
        return data.get("test_scenarios", {})
    
    def get_story_by_domain(self, domain: str) -> Dict[str, Any]:
        """Get first story matching domain."""
        stories = self.load_stories()
        for story in stories:
            if story.get("domain") == domain:
                return story
        return stories[0] if stories else {}