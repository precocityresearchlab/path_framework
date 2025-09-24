"""Shared knowledge base for PATH Framework agents."""

class SharedKnowledgeBase:
    """Shared knowledge base for storing and retrieving information."""
    
    def __init__(self):
        self.data = {}
    
    def store(self, key: str, value):
        """Store information in knowledge base."""
        self.data[key] = value
    
    def retrieve(self, key: str):
        """Retrieve information from knowledge base."""
        return self.data.get(key)