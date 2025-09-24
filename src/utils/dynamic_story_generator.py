"""Dynamic story generator using LLM."""

from typing import Dict, Any, List
from src.core.llm_interface import UnifiedLLMInterface


class DynamicStoryGenerator:
    """Generate user stories dynamically using LLM."""
    
    def __init__(self):
        self.llm = UnifiedLLMInterface()
    
    async def generate_story(self, domain: str, complexity: str = "simple") -> Dict[str, Any]:
        """Generate user story for domain and complexity."""
        
        prompt = f"""Generate a {complexity} user story for {domain} domain.
        
Format: "As a [user type], I want [functionality], so that [benefit]"

Requirements:
- Use proper user story format
- Make it realistic for {domain} domain
- {complexity} complexity level
- Include clear business value

Return only the user story text."""

        story_text = await self.llm.generate_response("story_generator", prompt)
        
        return {
            "story_id": f"GEN-{domain.upper()}-001",
            "user_story": story_text.strip(),
            "domain": domain,
            "complexity": complexity,
            "generated": True
        }
    
    async def generate_test_scenarios(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple test scenarios."""
        
        domains = ["healthcare", "finance", "education", "retail", "logistics"]
        complexities = ["simple", "medium", "complex"]
        
        scenarios = []
        for i in range(count):
            domain = domains[i % len(domains)]
            complexity = complexities[i % len(complexities)]
            
            story = await self.generate_story(domain, complexity)
            scenarios.append(story)
        
        return scenarios