"""Shared knowledge base for PATH Framework agents."""

from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime


class SharedKnowledgeBase:
    """Centralized knowledge storage and retrieval system."""
    
    def __init__(self):
        self.logger = logging.getLogger("SharedKnowledgeBase")
        
        # In-memory storage (would be replaced with actual databases)
        self.project_context = {}
        self.code_patterns = {}
        self.business_rules = {}
        self.technical_standards = {}
        self.lessons_learned = {}
        self.performance_metrics = {}
    
    async def store_project_context(self, context_id: str, context: Dict[str, Any]) -> None:
        """Store project context information."""
        self.project_context[context_id] = {
            **context,
            "timestamp": datetime.utcnow().isoformat(),
            "version": self._get_next_version(context_id)
        }
        self.logger.info(f"Stored project context: {context_id}")
    
    async def get_project_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve project context information."""
        return self.project_context.get(context_id)
    
    async def store_code_pattern(self, pattern_id: str, pattern: Dict[str, Any]) -> None:
        """Store successful code patterns."""
        self.code_patterns[pattern_id] = {
            **pattern,
            "timestamp": datetime.utcnow().isoformat(),
            "usage_count": 0
        }
        self.logger.info(f"Stored code pattern: {pattern_id}")
    
    async def get_code_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve code pattern."""
        pattern = self.code_patterns.get(pattern_id)
        if pattern:
            pattern["usage_count"] += 1
        return pattern
    
    async def search_patterns(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant patterns."""
        # Simplified search - would use vector search in real implementation
        results = []
        for pattern_id, pattern in self.code_patterns.items():
            if query.lower() in pattern.get("description", "").lower():
                results.append({
                    "pattern_id": pattern_id,
                    **pattern
                })
                if len(results) >= limit:
                    break
        
        return results
    
    async def store_business_rule(self, rule_id: str, rule: Dict[str, Any]) -> None:
        """Store business rule."""
        self.business_rules[rule_id] = {
            **rule,
            "timestamp": datetime.utcnow().isoformat(),
            "active": True
        }
        self.logger.info(f"Stored business rule: {rule_id}")
    
    async def get_business_rules(self, domain: str) -> List[Dict[str, Any]]:
        """Get business rules for domain."""
        rules = []
        for rule_id, rule in self.business_rules.items():
            if rule.get("domain") == domain and rule.get("active", True):
                rules.append({
                    "rule_id": rule_id,
                    **rule
                })
        return rules
    
    async def store_technical_standard(self, standard_id: str, standard: Dict[str, Any]) -> None:
        """Store technical standard."""
        self.technical_standards[standard_id] = {
            **standard,
            "timestamp": datetime.utcnow().isoformat(),
            "version": self._get_next_version(standard_id)
        }
        self.logger.info(f"Stored technical standard: {standard_id}")
    
    async def get_technical_standards(self, category: str) -> List[Dict[str, Any]]:
        """Get technical standards by category."""
        standards = []
        for standard_id, standard in self.technical_standards.items():
            if standard.get("category") == category:
                standards.append({
                    "standard_id": standard_id,
                    **standard
                })
        return standards
    
    async def store_lesson_learned(self, lesson_id: str, lesson: Dict[str, Any]) -> None:
        """Store lesson learned."""
        self.lessons_learned[lesson_id] = {
            **lesson,
            "timestamp": datetime.utcnow().isoformat(),
            "impact_score": lesson.get("impact_score", 5)
        }
        self.logger.info(f"Stored lesson learned: {lesson_id}")
    
    async def get_lessons_learned(self, context: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant lessons learned."""
        lessons = []
        for lesson_id, lesson in self.lessons_learned.items():
            if context.lower() in lesson.get("context", "").lower():
                lessons.append({
                    "lesson_id": lesson_id,
                    **lesson
                })
        
        # Sort by impact score
        lessons.sort(key=lambda x: x.get("impact_score", 0), reverse=True)
        return lessons[:limit]
    
    async def store_performance_metric(self, metric_id: str, metric: Dict[str, Any]) -> None:
        """Store performance metric."""
        if metric_id not in self.performance_metrics:
            self.performance_metrics[metric_id] = []
        
        self.performance_metrics[metric_id].append({
            **metric,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.logger.info(f"Stored performance metric: {metric_id}")
    
    async def get_performance_metrics(self, metric_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get performance metrics."""
        metrics = self.performance_metrics.get(metric_id, [])
        return metrics[-limit:]  # Return latest metrics
    
    async def get_performance_trend(self, metric_id: str, days: int = 30) -> Dict[str, Any]:
        """Get performance trend analysis."""
        metrics = await self.get_performance_metrics(metric_id, days * 24)  # Assuming hourly metrics
        
        if not metrics:
            return {"trend": "no_data", "metrics": []}
        
        values = [m.get("value", 0) for m in metrics]
        avg_value = sum(values) / len(values)
        
        # Simple trend calculation
        if len(values) > 1:
            recent_avg = sum(values[-7:]) / min(7, len(values))
            trend = "improving" if recent_avg > avg_value else "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "average": avg_value,
            "latest": values[-1] if values else 0,
            "count": len(values)
        }
    
    def _get_next_version(self, item_id: str) -> int:
        """Get next version number for item."""
        # Simple version increment - would be more sophisticated in real implementation
        return 1
    
    async def backup_knowledge(self) -> Dict[str, Any]:
        """Create backup of all knowledge."""
        return {
            "project_context": self.project_context,
            "code_patterns": self.code_patterns,
            "business_rules": self.business_rules,
            "technical_standards": self.technical_standards,
            "lessons_learned": self.lessons_learned,
            "performance_metrics": self.performance_metrics,
            "backup_timestamp": datetime.utcnow().isoformat()
        }
    
    async def restore_knowledge(self, backup: Dict[str, Any]) -> None:
        """Restore knowledge from backup."""
        self.project_context = backup.get("project_context", {})
        self.code_patterns = backup.get("code_patterns", {})
        self.business_rules = backup.get("business_rules", {})
        self.technical_standards = backup.get("technical_standards", {})
        self.lessons_learned = backup.get("lessons_learned", {})
        self.performance_metrics = backup.get("performance_metrics", {})
        
        self.logger.info("Knowledge base restored from backup")