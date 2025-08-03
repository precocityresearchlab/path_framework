#!/usr/bin/env uv run python
"""
PATH Framework with OpenRouter Integration Example
Demonstrates how to use OpenRouter for multi-model LLM access
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from path_framework.core.llm_client import get_llm_client, LLMRequest, LLMClientFactory, LLMProvider
from path_framework.phases.arch.ai.domain_analyst import AIDomainAnalyst, DomainAnalysisRequest, AnalysisType


async def demo_openrouter_integration():
    """Demonstrate PATH Framework with OpenRouter"""
    
    print("🌐 PATH Framework - OpenRouter Integration Demo")
    print("=" * 60)
    
    # Check for OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    if not openrouter_key:
        print("⚠️  OPENROUTER_API_KEY environment variable not found")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your-openrouter-api-key'")
        print("\nGet your API key from: https://openrouter.ai/keys")
        return
    
    print(f"🔑 OpenRouter API Key: {'*' * 20}{openrouter_key[-8:]}")
    print("🌐 Provider: OpenRouter")
    print("-" * 60)
    
    try:
        # Test different models through OpenRouter
        models_to_test = [
            "openai/gpt-4",                    # OpenAI GPT-4
            "anthropic/claude-3-sonnet",       # Anthropic Claude
            "meta-llama/llama-2-70b-chat",     # Meta Llama
            "google/palm-2-chat-bison"         # Google PaLM
        ]
        
        print("🧪 Testing Multiple Models via OpenRouter:")
        
        for model in models_to_test:
            print(f"\n🤖 Testing {model}...")
            
            try:
                # Create OpenRouter client for specific model
                client = LLMClientFactory.create_client(
                    provider=LLMProvider.OPENROUTER,
                    api_key=openrouter_key,
                    model=model
                )
                
                # Test basic connectivity
                test_request = LLMRequest(
                    prompt="Say 'Hello from PATH Framework!' in exactly 6 words.",
                    temperature=0.1,
                    max_tokens=50
                )
                
                response = await client.generate(test_request)
                
                print(f"   ✅ Response: {response.content.strip()}")
                print(f"   📊 Tokens: {response.tokens_used}")
                print(f"   🏷️  Model: {response.model_used}")
                
            except Exception as e:
                print(f"   ❌ Error with {model}: {str(e)[:100]}...")
                continue
        
        # Demo with PATH Framework Agent using OpenRouter
        print(f"\n🧠 PATH Framework Agent Demo with OpenRouter")
        print("-" * 50)
        
        # Set environment for default OpenRouter usage
        os.environ["PATH_LLM_PROVIDER"] = "openrouter"
        os.environ["PATH_LLM_MODEL"] = "openai/gpt-4"  # Default to GPT-4 via OpenRouter
        
        # Initialize Domain Analyst with OpenRouter
        domain_analyst = AIDomainAnalyst(config={
            "llm_provider": "openrouter",
            "llm_model": "openai/gpt-4"
        })
        
        # Simple project for testing
        project_description = """
        Build a simple task management API that allows users to create, 
        update, delete, and list tasks. Each task should have a title, 
        description, due date, and status (pending, in_progress, completed).
        The API should support user authentication and task filtering.
        """
        
        analysis_request = DomainAnalysisRequest(
            project_name="Task Management API",
            project_description=project_description,
            business_context="Internal productivity tool for small teams",
            stakeholder_input=[
                "As a user, I want to create tasks with due dates",
                "As a user, I want to filter tasks by status",
                "As a user, I want secure access to my tasks",
                "The API should be REST-based and return JSON"
            ],
            analysis_type=AnalysisType.REQUIREMENTS,
            industry_domain="productivity"
        )
        
        print(f"🔄 Running requirements analysis with OpenRouter...")
        print(f"📝 Project: {analysis_request.project_name}")
        
        # Execute analysis using OpenRouter
        result = await domain_analyst.analyze_requirements(analysis_request)
        
        print(f"\n✅ Analysis Complete!")
        print(f"🎯 Confidence Score: {result.confidence_score:.2f}")
        print(f"📊 Requirements Found: {len(result.requirements or [])}")
        
        if result.requirements:
            print(f"\n📋 Top 3 Requirements:")
            for i, req in enumerate(result.requirements[:3], 1):
                print(f"\n{i}. **{req.title}**")
                print(f"   Priority: {req.priority.value}")
                print(f"   Type: {req.type.value}")
                print(f"   Description: {req.description[:120]}...")
        
        # Demo model switching with OpenRouter
        print(f"\n🔄 Model Switching Demo")
        print("-" * 30)
        
        alternative_models = [
            "anthropic/claude-3-sonnet",
            "meta-llama/llama-2-70b-chat"
        ]
        
        simple_prompt = "Explain microservices in exactly 2 sentences."
        
        for model in alternative_models:
            try:
                print(f"\n🤖 Using {model}:")
                
                # Create client for specific model
                client = get_llm_client(
                    provider="openrouter",
                    api_key=openrouter_key,
                    model=model
                )
                
                request = LLMRequest(
                    prompt=simple_prompt,
                    temperature=0.1,
                    max_tokens=100
                )
                
                response = await client.generate(request)
                print(f"   Response: {response.content.strip()}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:80]}...")
        
        print(f"\n🎉 OpenRouter Integration Demo Complete!")
        print(f"✅ Demonstrated:")
        print(f"   • Multiple model access via single API")
        print(f"   • PATH Framework agent integration")
        print(f"   • Model switching capabilities")
        print(f"   • Requirements analysis with AI")
        
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        print("Please check your OpenRouter API key and internet connection")


async def demo_openrouter_structured_generation():
    """Demo structured JSON generation with OpenRouter"""
    
    print(f"\n🔧 Structured Generation Demo with OpenRouter")
    print("-" * 50)
    
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY required for this demo")
        return
    
    try:
        # Test structured generation with different models
        client = get_llm_client(
            provider="openrouter",
            api_key=openrouter_key,
            model="openai/gpt-4"
        )
        
        schema = {
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "priority": {"type": "string", "enum": ["high", "medium", "low"]}
                        }
                    }
                }
            }
        }
        
        request = LLMRequest(
            prompt="Extract key features for a todo app with user authentication",
            system_prompt="You are a product manager extracting software features",
            temperature=0.1,
            max_tokens=800
        )
        
        result = await client.generate_structured(request, schema)
        
        print("✅ Structured JSON Result:")
        import json
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Structured generation error: {e}")


if __name__ == "__main__":
    print("🚀 Starting OpenRouter Integration Demo...\n")
    
    # Run main demo
    asyncio.run(demo_openrouter_integration())
    
    # Run structured generation demo
    asyncio.run(demo_openrouter_structured_generation())
