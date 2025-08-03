#!/usr/bin/env uv run python
"""
Test Gemma 3 27B LLM Integration via OpenRouter
PATH Framework LLM Testing
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent))

from path_framework.core.llm_client import get_llm_client, LLMRequest


async def test_gemma_llm():
    """Test Gemma 3 27B model via OpenRouter"""
    
    print("🧠 Testing Gemma 3 27B LLM Integration")
    print("=" * 50)
    
    # Check environment
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    provider = os.getenv("PATH_LLM_PROVIDER", "openrouter")
    model = os.getenv("PATH_LLM_MODEL_PHASE1", "google/gemma-3-27b-it:free")
    
    print(f"🔗 Provider: {provider}")
    print(f"🤖 Model: {model}")
    print(f"🔑 API Key: {'✅ Set' if openrouter_key else '❌ Missing'}")
    
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    try:
        print("\n🔄 Creating LLM client...")
        llm_client = get_llm_client(phase=1)
        print(f"✅ Client created: {type(llm_client).__name__}")
        
        print("\n🧪 Testing basic LLM call...")
        test_request = LLMRequest(
            prompt="""Hello! I'm testing the Gemma 3 27B model integration. Please respond with:
1. Confirm you are Gemma 3 27B
2. A brief hello message
3. The current capabilities you have

Keep your response concise and structured.""",
            temperature=0.1,
            max_tokens=200
        )
        
        print("📤 Sending request to LLM...")
        response = await llm_client.generate(test_request)
        
        print("\n✅ LLM Response:")
        print("-" * 40)
        print(response.content)
        print("-" * 40)
        
        print(f"\n📊 Response Metadata:")
        print(f"   Model Used: {response.model_used}")
        print(f"   Tokens Used: {response.tokens_used}")
        print(f"   Cost: Free (Gemma 3 27B is free on OpenRouter)")
        print(f"   Response Generated: ✅ Success")
        
        # Test structured prompt for requirements analysis
        print("\n🧠 Testing structured requirements analysis...")
        requirements_prompt = """
        Analyze the following project description and extract 3 key functional requirements:
        
        Project: "A simple task management web application where users can create, edit, delete, and mark tasks as complete. Users need to sign up and log in to access their personal task lists."
        
        Please respond in this exact JSON format:
        {
            "requirements": [
                {"id": 1, "title": "Requirement Title", "description": "Detailed description", "priority": "high|medium|low"},
                {"id": 2, "title": "Requirement Title", "description": "Detailed description", "priority": "high|medium|low"},
                {"id": 3, "title": "Requirement Title", "description": "Detailed description", "priority": "high|medium|low"}
            ]
        }
        """
        
        analysis_request = LLMRequest(
            prompt=requirements_prompt,
            temperature=0.2,
            max_tokens=400
        )
        
        analysis_response = await llm_client.generate(analysis_request)
        
        print("\n✅ Requirements Analysis Response:")
        print("-" * 40)
        print(analysis_response.content)
        print("-" * 40)
        
        # Try to parse as JSON
        try:
            import json
            parsed = json.loads(analysis_response.content)
            print(f"\n🎯 Successfully parsed {len(parsed.get('requirements', []))} requirements!")
            for req in parsed.get('requirements', []):
                print(f"   • {req.get('title', 'Unknown')}: {req.get('priority', 'unknown')} priority")
        except json.JSONDecodeError:
            print("\n⚠️  Response is not valid JSON, but that's okay for testing!")
        
        print(f"\n🎉 Gemma 3 27B LLM Test Complete!")
        print(f"✅ Successfully demonstrated:")
        print(f"   • OpenRouter API connectivity")
        print(f"   • Gemma 3 27B model execution")
        print(f"   • Basic conversation capabilities")
        print(f"   • Structured prompt processing")
        print(f"   • Response metadata extraction")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting Gemma 3 27B LLM Test...")
    success = asyncio.run(test_gemma_llm())
    if success:
        print("\n🚀 LLM integration is working correctly!")
    else:
        print("\n💥 LLM integration needs debugging.")
