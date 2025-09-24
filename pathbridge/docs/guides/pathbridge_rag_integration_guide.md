# PathBridge RAG Integration Guide

## Overview

PathBridge RAG (Retrieval-Augmented Generation) system provides intelligent context retrieval for AI agents using vector databases and embeddings.

**Supported Providers:**
- **Pinecone** (Cloud vector database)
- **Weaviate** (Open-source vector database)
- **Chroma** (Local vector database)
- **PostgreSQL + pgvector** (SQL with vector support)

## Quick Start

### 1. Set Up Environment

```bash
# For Pinecone
export PINECONE_API_KEY="your-pinecone-key"
export PINECONE_ENVIRONMENT="us-west1-gcp"

# For Weaviate
export WEAVIATE_URL="http://localhost:8080"
export WEAVIATE_API_KEY="your-weaviate-key"

# For Chroma
export CHROMA_HOST="localhost"
export CHROMA_PORT="8000"

# Default provider
export PATH_VECTOR_PROVIDER="pinecone"
export PATH_EMBEDDING_MODEL="openai"
```

### 2. Basic Usage

```python
from pathbridge.core.rag_client import get_rag_client, RAGRequest

async def basic_rag_example():
    # Get RAG client
    rag_client = get_rag_client()
    
    # Store knowledge
    await rag_client.store_knowledge(
        content="FastAPI is a modern web framework for Python",
        metadata={"type": "framework", "language": "python"}
    )
    
    # Retrieve context
    request = RAGRequest(
        query="How to build REST APIs in Python?",
        top_k=5,
        similarity_threshold=0.7
    )
    
    context = await rag_client.retrieve_context(request)
    print(f"Retrieved {len(context.documents)} relevant documents")
```

## Provider Configuration

### Pinecone Configuration

```python
from pathbridge.core.rag_client import RAGClientFactory, VectorProvider

# Direct Pinecone client
pinecone_client = RAGClientFactory.create_client(
    provider=VectorProvider.PINECONE,
    api_key="your-pinecone-key",
    environment="us-west1-gcp",
    index_name="pathbridge-knowledge"
)

# Store and retrieve
await pinecone_client.store_knowledge(
    content="Python async/await patterns",
    metadata={"category": "programming"}
)

context = await pinecone_client.retrieve_context(
    RAGRequest(query="async programming", top_k=3)
)
```

### Weaviate Configuration

```python
# Weaviate client
weaviate_client = RAGClientFactory.create_client(
    provider=VectorProvider.WEAVIATE,
    url="http://localhost:8080",
    api_key="your-weaviate-key",
    class_name="PathBridgeKnowledge"
)

# Batch operations
documents = [
    {"content": "TDD best practices", "metadata": {"type": "methodology"}},
    {"content": "Docker deployment", "metadata": {"type": "devops"}}
]

await weaviate_client.batch_store(documents)
```

### PostgreSQL + pgvector Configuration

```python
# PostgreSQL with vector support
postgres_client = RAGClientFactory.create_client(
    provider=VectorProvider.POSTGRES,
    connection_string="postgresql://user:pass@localhost/pathbridge",
    table_name="knowledge_base",
    embedding_dimension=1536
)
```

## Integration with PATH Agents

### RAG-Enhanced Agent

```python
from pathbridge.agents.base_agent import CoreAgent
from pathbridge.core.rag_client import get_rag_client, RAGRequest

class RAGEnhancedAgent(CoreAgent):
    def __init__(self, agent_id: str, phase: int, capabilities: List[str]):
        super().__init__(agent_id, phase, capabilities)
        self.rag_client = get_rag_client()
    
    async def execute_with_context(self, request: CapabilityRequest) -> CapabilityResponse:
        # Retrieve relevant context
        rag_request = RAGRequest(
            query=request.parameters.get("query", ""),
            top_k=5,
            metadata_filter={"agent_type": self.agent_id}
        )
        
        context = await self.rag_client.retrieve_context(rag_request)
        
        # Enhance request with context
        enhanced_request = request
        enhanced_request.context["retrieved_knowledge"] = [
            doc.content for doc in context.documents
        ]
        
        # Execute with enhanced context
        return await self.execute_capability(enhanced_request)
    
    async def store_execution_result(self, request: CapabilityRequest, result: Dict[str, Any]):
        # Store successful results as knowledge
        if result.get("success"):
            await self.rag_client.store_knowledge(
                content=f"Agent {self.agent_id} successfully executed {request.capability_name}",
                metadata={
                    "agent_id": self.agent_id,
                    "capability": request.capability_name,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
```

## Advanced Usage

### Semantic Search with Filters

```python
async def advanced_search():
    rag_client = get_rag_client()
    
    # Complex query with metadata filters
    request = RAGRequest(
        query="microservices architecture patterns",
        top_k=10,
        similarity_threshold=0.8,
        metadata_filter={
            "category": "architecture",
            "complexity": {"$gte": "intermediate"}
        },
        rerank=True
    )
    
    context = await rag_client.retrieve_context(request)
    
    # Process results
    for doc in context.documents:
        print(f"Score: {doc.score}, Content: {doc.content[:100]}...")
```

### Hybrid Search (Vector + Keyword)

```python
async def hybrid_search():
    request = RAGRequest(
        query="REST API authentication",
        top_k=5,
        search_type="hybrid",  # Vector + keyword search
        alpha=0.7  # Weight for vector search (0.3 for keyword)
    )
    
    context = await rag_client.retrieve_context(request)
```

## Error Handling

```python
from pathbridge.exceptions import RAGError, VectorStoreError

async def robust_rag_usage():
    try:
        rag_client = get_rag_client()
        
        context = await rag_client.retrieve_context(
            RAGRequest(query="complex query", top_k=5)
        )
        
        return context
        
    except VectorStoreError as e:
        print(f"Vector store error: {e}")
        # Fallback to cached results or simplified search
        
    except RAGError as e:
        print(f"RAG system error: {e}")
        # Return empty context or use alternative retrieval
```

## Testing RAG Integration

```python
import pytest
from pathbridge.core.rag_client import get_rag_client, RAGRequest

@pytest.mark.asyncio
async def test_rag_store_and_retrieve():
    """Test basic store and retrieve functionality"""
    rag_client = get_rag_client()
    
    # Store test knowledge
    await rag_client.store_knowledge(
        content="Test knowledge for PathBridge",
        metadata={"test": True, "category": "testing"}
    )
    
    # Retrieve
    request = RAGRequest(
        query="PathBridge testing",
        top_k=1,
        metadata_filter={"test": True}
    )
    
    context = await rag_client.retrieve_context(request)
    
    assert len(context.documents) > 0
    assert "PathBridge" in context.documents[0].content
```

## Configuration

### Environment Variables

```bash
# Vector Database Provider
PATH_VECTOR_PROVIDER=pinecone  # pinecone, weaviate, chroma, postgres

# Pinecone Settings
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=pathbridge-knowledge

# Weaviate Settings
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=your-key
WEAVIATE_CLASS_NAME=PathBridgeKnowledge

# Embedding Settings
PATH_EMBEDDING_MODEL=openai  # openai, sentence-transformers, huggingface
PATH_EMBEDDING_DIMENSION=1536

# Performance Settings
PATH_RAG_BATCH_SIZE=100
PATH_RAG_TIMEOUT=30
PATH_RAG_MAX_RETRIES=3
```

## Troubleshooting

### Common Issues

1. **Connection Failed**
   ```
   Error: Failed to connect to vector database
   Solution: Check provider URL and API keys
   ```

2. **Embedding Dimension Mismatch**
   ```
   Error: Embedding dimension mismatch
   Solution: Ensure consistent embedding model and dimension
   ```

3. **Low Similarity Scores**
   ```
   Issue: Retrieved documents not relevant
   Solution: Adjust similarity_threshold or improve query
   ```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable RAG debug logging
rag_client = get_rag_client(debug=True)
```