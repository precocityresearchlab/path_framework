#!/usr/bin/env python3
"""
PATH Framework LLM Integration Demo
Demonstrates how AI agents interact with real external LLMs
"""

import asyncio
import json
import os
from pathlib import Path


async def demo_llm_integration():
    """Demonstrate real LLM integration without complex imports"""
    
    print("🤖 PATH Framework - Real LLM Integration Demonstration")
    print("=" * 70)
    
    # Check for API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("⚠️  No LLM API keys found in environment variables")
        print("\n🔧 To test real LLM integration, set one of:")
        print("   export OPENAI_API_KEY='your-openai-api-key'")
        print("   export ANTHROPIC_API_KEY='your-anthropic-api-key'")
        print("\n🎭 Running mock demonstration instead...")
        await demo_mock_llm()
        return
    
    # Determine provider
    if openai_key:
        await demo_openai_integration(openai_key)
    else:
        await demo_anthropic_integration(anthropic_key)


async def demo_openai_integration(api_key: str):
    """Demo with OpenAI GPT-4"""
    print("🚀 Testing OpenAI GPT-4 Integration")
    print("-" * 40)
    
    try:
        # Import OpenAI (optional dependency)
        import openai
        
        # Initialize client
        client = openai.AsyncOpenAI(api_key=api_key)
        
        print("🔗 Connected to OpenAI API")
        print("🧠 Model: GPT-4")
        
        # Test basic connectivity
        print("\n🔍 Testing basic connectivity...")
        basic_response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Please confirm you're connected."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        print(f"✅ Response: {basic_response.choices[0].message.content}")
        print(f"📊 Tokens: {basic_response.usage.total_tokens}")
        
        # Demonstrate requirements analysis
        print("\n🧠 Demonstrating AI-Powered Requirements Analysis...")
        requirements_response = await analyze_requirements_with_openai(client)
        
        # Save results
        await save_llm_results("openai", "gpt-4", requirements_response)
        
    except ImportError:
        print("❌ OpenAI library not installed")
        print("📦 Install with: uv add openai")
    except Exception as e:
        print(f"❌ OpenAI integration error: {e}")


async def demo_anthropic_integration(api_key: str):
    """Demo with Anthropic Claude"""
    print("🚀 Testing Anthropic Claude Integration")
    print("-" * 40)
    
    try:
        # Import Anthropic (optional dependency)
        import anthropic
        
        # Initialize client
        client = anthropic.AsyncAnthropic(api_key=api_key)
        
        print("🔗 Connected to Anthropic API")
        print("🧠 Model: Claude-3-Sonnet")
        
        # Test basic connectivity
        print("\n🔍 Testing basic connectivity...")
        basic_response = await client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=50,
            messages=[
                {"role": "user", "content": "Hello! Please confirm you're connected."}
            ]
        )
        
        print(f"✅ Response: {basic_response.content[0].text}")
        print(f"📊 Tokens: {basic_response.usage.input_tokens + basic_response.usage.output_tokens}")
        
        # Demonstrate requirements analysis
        print("\n🧠 Demonstrating AI-Powered Requirements Analysis...")
        requirements_response = await analyze_requirements_with_anthropic(client)
        
        # Save results
        await save_llm_results("anthropic", "claude-3-sonnet", requirements_response)
        
    except ImportError:
        print("❌ Anthropic library not installed")
        print("📦 Install with: uv add anthropic")
    except Exception as e:
        print(f"❌ Anthropic integration error: {e}")


async def analyze_requirements_with_openai(client):
    """Demonstrate requirements analysis with OpenAI"""
    
    system_prompt = """You are an expert business analyst specializing in software requirements engineering. 
Your task is to extract clear, actionable requirements from project descriptions.

For each requirement:
1. Create a clear title
2. Classify type (functional, non_functional, business, technical)
3. Set priority (critical, high, medium, low)
4. Generate acceptance criteria
5. Assess complexity (1-10)"""

    user_prompt = """Project: Sustainable E-commerce Platform (EcoMart)

Description: Build a platform for eco-conscious consumers to discover and purchase sustainable products. Features include vendor management, sustainability scoring, product catalog, shopping cart, payment processing, and order tracking. Must support 10,000+ concurrent users with 99.9% uptime.

Business Context: Target millennials/Gen-Z who prioritize sustainability. Revenue from transaction fees and premium certifications. Competitive advantage is comprehensive sustainability scoring.

Stakeholder Input:
- "Users need easy product discovery with sustainability filters"
- "Vendors require self-service catalog management tools"  
- "Admin needs comprehensive reporting and analytics"
- "Must integrate with Stripe and PayPal for payments"
- "Mobile-first design is essential"

Extract all requirements as JSON:
{
  "requirements": [
    {
      "title": "string",
      "description": "string",
      "type": "functional|non_functional|business|technical",
      "priority": "critical|high|medium|low", 
      "acceptance_criteria": ["string"],
      "complexity_score": number,
      "business_value": "string"
    }
  ]
}"""

    print("📝 Analyzing project requirements...")
    
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=4000,
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    
    requirements_text = response.choices[0].message.content
    requirements_data = json.loads(requirements_text)
    
    print(f"✅ Extracted {len(requirements_data['requirements'])} requirements")
    
    # Display sample requirements
    for i, req in enumerate(requirements_data['requirements'][:3], 1):
        print(f"\n{i}. **{req['title']}**")
        print(f"   Type: {req['type']}")
        print(f"   Priority: {req['priority']}")
        print(f"   Complexity: {req['complexity_score']}/10")
        print(f"   Description: {req['description'][:80]}...")
    
    if len(requirements_data['requirements']) > 3:
        print(f"\n... and {len(requirements_data['requirements']) - 3} more requirements")
    
    return {
        "requirements": requirements_data['requirements'],
        "tokens_used": response.usage.total_tokens,
        "model": response.model
    }


async def analyze_requirements_with_anthropic(client):
    """Demonstrate requirements analysis with Anthropic"""
    
    prompt = """You are an expert business analyst. Extract software requirements from this project description and return as JSON.

Project: Sustainable E-commerce Platform (EcoMart)

Description: Build a platform for eco-conscious consumers to discover and purchase sustainable products. Features include vendor management, sustainability scoring, product catalog, shopping cart, payment processing, and order tracking. Must support 10,000+ concurrent users with 99.9% uptime.

Business Context: Target millennials/Gen-Z who prioritize sustainability. Revenue from transaction fees and premium certifications.

Stakeholder Input:
- "Users need easy product discovery with sustainability filters"
- "Vendors require self-service catalog management tools"
- "Admin needs comprehensive reporting and analytics" 
- "Must integrate with Stripe and PayPal for payments"
- "Mobile-first design is essential"

Return JSON with this structure:
{
  "requirements": [
    {
      "title": "string",
      "description": "string", 
      "type": "functional|non_functional|business|technical",
      "priority": "critical|high|medium|low",
      "acceptance_criteria": ["string"],
      "complexity_score": number,
      "business_value": "string"
    }
  ]
}

Return only valid JSON, no other text."""

    print("📝 Analyzing project requirements...")
    
    response = await client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    requirements_text = response.content[0].text
    requirements_data = json.loads(requirements_text)
    
    print(f"✅ Extracted {len(requirements_data['requirements'])} requirements")
    
    # Display sample requirements
    for i, req in enumerate(requirements_data['requirements'][:3], 1):
        print(f"\n{i}. **{req['title']}**")
        print(f"   Type: {req['type']}")
        print(f"   Priority: {req['priority']}")
        print(f"   Complexity: {req['complexity_score']}/10")
        print(f"   Description: {req['description'][:80]}...")
    
    if len(requirements_data['requirements']) > 3:
        print(f"\n... and {len(requirements_data['requirements']) - 3} more requirements")
    
    return {
        "requirements": requirements_data['requirements'],
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "model": "claude-3-sonnet-20240229"
    }


async def save_llm_results(provider: str, model: str, results: dict):
    """Save LLM analysis results to project artifacts"""
    
    # Create project directory
    project_path = Path("./projects/ecomart-llm-demo")
    artifacts_path = project_path / "path_artifacts" / "arch"
    artifacts_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare results data
    output_data = {
        "llm_metadata": {
            "provider": provider,
            "model": model,
            "tokens_used": results["tokens_used"],
            "timestamp": "2025-08-03T19:52:00Z"
        },
        "project": {
            "name": "EcoMart - Sustainable E-commerce Platform",
            "description": "AI-generated requirements analysis"
        },
        "requirements": results["requirements"],
        "analysis_summary": {
            "total_requirements": len(results["requirements"]),
            "by_type": {},
            "by_priority": {}
        }
    }
    
    # Calculate summaries
    for req in results["requirements"]:
        req_type = req.get("type", "unknown")
        req_priority = req.get("priority", "unknown")
        
        output_data["analysis_summary"]["by_type"][req_type] = \
            output_data["analysis_summary"]["by_type"].get(req_type, 0) + 1
        output_data["analysis_summary"]["by_priority"][req_priority] = \
            output_data["analysis_summary"]["by_priority"].get(req_priority, 0) + 1
    
    # Save to file
    output_file = artifacts_path / f"llm_requirements_{provider}.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    print(f"📊 Analysis Summary:")
    print(f"   • Total Requirements: {output_data['analysis_summary']['total_requirements']}")
    print(f"   • By Type: {dict(output_data['analysis_summary']['by_type'])}")
    print(f"   • By Priority: {dict(output_data['analysis_summary']['by_priority'])}")


async def demo_mock_llm():
    """Mock demonstration when no API keys available"""
    print("\n🎭 Mock LLM Integration Demo")
    print("-" * 40)
    
    print("📝 This demonstration shows how PATH Framework AI agents")
    print("    would interact with real LLM APIs to:")
    print()
    print("✅ Extract requirements from natural language")
    print("✅ Classify and prioritize requirements")
    print("✅ Generate acceptance criteria")
    print("✅ Assess complexity scores")
    print("✅ Provide business value analysis")
    print("✅ Create structured JSON output")
    print()
    print("🎯 Example LLM Analysis Output:")
    
    mock_requirements = [
        {
            "title": "User Authentication System",
            "description": "Secure user registration and login functionality",
            "type": "functional",
            "priority": "critical",
            "acceptance_criteria": [
                "Users can register with email/password",
                "Login sessions expire after 24 hours",
                "Password reset functionality available"
            ],
            "complexity_score": 7,
            "business_value": "Essential for platform security and user management"
        },
        {
            "title": "Sustainability Scoring Engine", 
            "description": "Algorithm to calculate and display product sustainability ratings",
            "type": "functional",
            "priority": "high",
            "acceptance_criteria": [
                "Score calculated from multiple sustainability factors",
                "Scores displayed prominently on product pages",
                "Scoring algorithm is transparent to users"
            ],
            "complexity_score": 9,
            "business_value": "Core competitive advantage and differentiation"
        }
    ]
    
    for i, req in enumerate(mock_requirements, 1):
        print(f"\n{i}. **{req['title']}**")
        print(f"   Type: {req['type']}")
        print(f"   Priority: {req['priority']}")
        print(f"   Complexity: {req['complexity_score']}/10")
        print(f"   Business Value: {req['business_value']}")
    
    print(f"\n🎉 Mock demonstration complete!")
    print(f"🔧 To see real LLM integration, set API keys and run again.")


if __name__ == "__main__":
    print("🚀 Starting PATH Framework LLM Integration Demo...")
    asyncio.run(demo_llm_integration())
