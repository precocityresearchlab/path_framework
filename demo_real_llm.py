#!/usr/bin/env uv run python
"""
PATH Framework Phase 1 Demo with Real LLM Integration
Demonstrates AI agents calling external LLM APIs
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent))

from path_framework.phases.arch.ai.domain_analyst import AIDomainAnalyst, DomainAnalysisRequest, AnalysisType
from path_framework.core.llm_client import get_llm_client, LLMRequest


async def demo_real_llm_integration():
    """Demonstrate PATH Framework with real LLM API calls"""
    
    print("🤖 PATH Framework - Real LLM Integration Demo")
    print("=" * 60)
    
    # Check if API keys are available
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("⚠️  No LLM API keys found in environment variables")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY to test real LLM integration")
        print("Falling back to mock demonstration...")
        await demo_mock_llm_workflow()
        return
    
    # Determine which LLM to use
    if openai_key:
        provider = "openai"
        model = "gpt-4"
        print(f"🤖 Using OpenAI GPT-4 for real LLM integration")
    else:
        provider = "anthropic"
        model = "claude-3-sonnet-20240229"
        print(f"🤖 Using Anthropic Claude for real LLM integration")
    
    print(f"🔗 LLM Provider: {provider}")
    print(f"🧠 Model: {model}")
    print("-" * 60)
    
    try:
        # Test basic LLM connectivity
        print("🔍 Testing LLM connectivity...")
        llm_client = get_llm_client(provider=provider)
        
        test_request = LLMRequest(
            prompt="Hello! Please respond with 'LLM connection successful' to confirm connectivity.",
            temperature=0.1,
            max_tokens=50
        )
        
        test_response = await llm_client.generate(test_request)
        print(f"✅ LLM Response: {test_response.content[:100]}...")
        print(f"📊 Tokens used: {test_response.tokens_used}")
        print(f"🏷️  Model: {test_response.model_used}")
        
        # Now demonstrate AI Domain Analyst with real LLM
        print("\n🧠 Initializing AI Domain Analyst with real LLM...")
        domain_analyst = AIDomainAnalyst(config={
            "llm_provider": provider,
            "llm_model": model
        })
        
        # Real project example
        project_description = """
        We need to build a sustainable e-commerce platform called EcoMart that helps 
        environmentally conscious consumers find and purchase eco-friendly products. 
        The platform should support multiple vendors selling sustainable goods, with 
        features like sustainability scoring, carbon footprint tracking, and green 
        shipping options. Users should be able to browse products, compare 
        sustainability ratings, add items to cart, process payments, and track orders.
        The system must handle 10,000+ concurrent users and process millions of 
        transactions per month while maintaining 99.9% uptime.
        """
        
        business_context = """
        Target market: Eco-conscious millennials and Gen-Z consumers who prioritize 
        sustainability in their purchasing decisions. Revenue model includes 
        transaction fees from vendors and premium sustainability certification services.
        Key competitive advantage is the comprehensive sustainability scoring system 
        and carbon footprint tracking. Regulatory requirements include GDPR compliance 
        for European users and PCI DSS for payment processing.
        """
        
        stakeholder_input = [
            "As a customer, I want to easily find products with high sustainability scores",
            "As a vendor, I need tools to manage my product catalog and track sales",
            "As an admin, I need comprehensive analytics and reporting capabilities",
            "The system must integrate with existing payment processors like Stripe",
            "Mobile responsiveness is critical for our target demographic"
        ]
        
        # Create analysis request
        analysis_request = DomainAnalysisRequest(
            project_name="EcoMart Sustainable E-commerce Platform",
            project_description=project_description,
            business_context=business_context,
            stakeholder_input=stakeholder_input,
            analysis_type=AnalysisType.REQUIREMENTS,
            industry_domain="e_commerce"
        )
        
        print(f"\n🔄 Running real LLM-powered requirements analysis...")
        print(f"📝 Project: {analysis_request.project_name}")
        print(f"📋 Analysis Type: {analysis_request.analysis_type.value}")
        
        # Execute real LLM analysis
        analysis_result = await domain_analyst.analyze_requirements(analysis_request)
        
        # Display results
        print(f"\n✅ Requirements Analysis Complete!")
        print(f"🎯 Confidence Score: {analysis_result.confidence_score:.2f}")
        print(f"👥 Human Review Required: {analysis_result.human_review_required}")
        print(f"📊 Requirements Found: {len(analysis_result.requirements or [])}")
        
        if analysis_result.requirements:
            print(f"\n📋 Extracted Requirements:")
            for i, req in enumerate(analysis_result.requirements, 1):
                print(f"\n{i}. **{req.title}**")
                print(f"   Type: {req.type.value}")
                print(f"   Priority: {req.priority.value}")
                print(f"   Description: {req.description[:100]}...")
                if req.acceptance_criteria:
                    print(f"   Acceptance Criteria: {len(req.acceptance_criteria)} criteria defined")
                print(f"   Complexity Score: {req.complexity_score}/10")
        
        if analysis_result.recommendations:
            print(f"\n💡 AI Recommendations:")
            for rec in analysis_result.recommendations:
                print(f"   • {rec}")
        
        # Save results to project
        project_path = Path("./projects/ecomart-llm-demo")
        artifacts_path = project_path / "path_artifacts" / "arch"
        artifacts_path.mkdir(parents=True, exist_ok=True)
        
        # Save requirements as JSON
        import json
        requirements_data = {
            "project_name": analysis_request.project_name,
            "analysis_type": analysis_result.analysis_type.value,
            "confidence_score": analysis_result.confidence_score,
            "human_review_required": analysis_result.human_review_required,
            "llm_metadata": {
                "provider": provider,
                "model": model,
                "tokens_used": test_response.tokens_used
            },
            "requirements": [
                {
                    "title": req.title,
                    "description": req.description,
                    "type": req.type.value,
                    "priority": req.priority.value,
                    "acceptance_criteria": req.acceptance_criteria,
                    "complexity_score": req.complexity_score,
                    "business_value": req.business_value
                }
                for req in (analysis_result.requirements or [])
            ],
            "recommendations": analysis_result.recommendations or []
        }
        
        with open(artifacts_path / "llm_requirements_analysis.json", "w") as f:
            json.dump(requirements_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {artifacts_path / 'llm_requirements_analysis.json'}")
        
        print(f"\n🎉 Real LLM Integration Demo Complete!")
        print(f"✅ Successfully demonstrated:")
        print(f"   • Real {provider.upper()} API connectivity")
        print(f"   • AI-powered requirements extraction")
        print(f"   • Structured data parsing from LLM")
        print(f"   • Project artifact generation")
        print(f"   • Fallback error handling")
        
    except Exception as e:
        print(f"❌ LLM Integration Error: {e}")
        print("Falling back to mock demonstration...")
        await demo_mock_llm_workflow()


async def demo_mock_llm_workflow():
    """Demo the workflow without real LLM calls"""
    print("\n🎭 Mock LLM Workflow Demo")
    print("-" * 40)
    
    print("This would normally:")
    print("✅ Connect to OpenAI GPT-4 or Anthropic Claude")
    print("✅ Send structured prompts for requirements analysis")
    print("✅ Parse JSON responses into domain models")
    print("✅ Generate comprehensive requirements with AI insights")
    print("✅ Provide confidence scoring and recommendations")
    
    print("\n🔧 To enable real LLM integration:")
    print("   export OPENAI_API_KEY='your-openai-key'")
    print("   # OR")
    print("   export ANTHROPIC_API_KEY='your-anthropic-key'")
    print("   # Then run this demo again")


if __name__ == "__main__":
    print("Starting PATH Framework Real LLM Integration Demo...")
    asyncio.run(demo_real_llm_integration())
