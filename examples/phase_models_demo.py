#!/usr/bin/env uv run python
"""
PATH Framework Phase-Specific Model Configuration Demo
Demonstrates using different models for different phases
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from path_framework.core.llm_client import LLMRequest, get_llm_client


async def demo_phase_specific_models():
    """Demonstrate phase-specific model configuration"""

    print("🎯 PATH Framework - Phase-Specific Model Configuration Demo")
    print("=" * 70)

    # Check current environment variables
    print("\n📋 Current Environment Configuration:")
    print("-" * 40)

    env_vars = [
        "OPENROUTER_API_KEY",
        "PATH_LLM_PROVIDER",
        "PATH_LLM_MODEL_PHASE1",
        "PATH_LLM_MODEL_PHASE2",
        "PATH_LLM_MODEL_PHASE3",
        "PATH_LLM_MODEL_PHASE4",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "KEY" in var:
                print(f"   ✅ {var}: {'*' * 8}{value[-4:]}")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: Not set")

    # Test each phase
    phases = [
        {
            "phase": 1,
            "name": "Architecture & Requirements",
            "description": "Domain modeling, requirements analysis",
            "prompt": "Extract 3 key requirements from: Build a user authentication system",
        },
        {
            "phase": 2,
            "name": "Development Planning",
            "description": "Technology selection, planning",
            "prompt": "Recommend 3 technologies for building a web API",
        },
        {
            "phase": 3,
            "name": "Implementation",
            "description": "Code generation, implementation",
            "prompt": "Write a Python function to validate email addresses",
        },
        {
            "phase": 4,
            "name": "Testing & Deployment",
            "description": "Testing strategies, deployment",
            "prompt": "Create 3 test cases for user login functionality",
        },
    ]

    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n⚠️  OPENROUTER_API_KEY not set - showing configuration only")

        print("\n💡 To enable testing, set your environment variables:")
        print("export OPENROUTER_API_KEY='your-api-key'")
        print("export PATH_LLM_PROVIDER='openrouter'")
        print(
            "export PATH_LLM_MODEL_PHASE1='openai/gpt-4'           # Best for analysis"
        )
        print(
            "export PATH_LLM_MODEL_PHASE2='anthropic/claude-3-sonnet'  # Good for planning"
        )
        print(
            "export PATH_LLM_MODEL_PHASE3='meta-llama/llama-2-70b-chat'  # Fast for coding"
        )
        print(
            "export PATH_LLM_MODEL_PHASE4='openai/gpt-3.5-turbo'  # Efficient for testing"
        )
        return

    print("\n🚀 Testing Phase-Specific Models:")
    print("=" * 50)

    for phase_config in phases:
        phase_num = phase_config["phase"]
        phase_name = phase_config["name"]
        description = phase_config["description"]
        test_prompt = phase_config["prompt"]

        print(f"\n📍 Phase {phase_num}: {phase_name}")
        print(f"   Purpose: {description}")

        try:
            # Get phase-specific client
            client = get_llm_client(phase=phase_num)

            print(f"   🤖 Model: {client.model}")
            print(f"   🔧 Provider: {client.__class__.__name__}")

            # Test with phase-appropriate prompt
            request = LLMRequest(
                prompt=test_prompt,
                system_prompt=f"You are an expert in Phase {phase_num} of software development ({description})",
                temperature=0.1,
                max_tokens=300,
            )

            response = await client.generate(request)

            print(f"   ✅ Response: {response.content[:100]}...")
            print(f"   📊 Tokens: {response.tokens_used}")
            print(f"   🏷️  Actual Model: {response.model_used}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}...")


async def demo_model_comparison():
    """Compare different models for the same task"""

    print("\n🔬 Model Comparison Demo")
    print("-" * 40)

    if not os.getenv("OPENROUTER_API_KEY"):
        print("   ⚠️  OPENROUTER_API_KEY required for comparison")
        return

    # Test prompt for all models
    test_prompt = (
        "List 3 benefits of microservices architecture in exactly 3 bullet points"
    )

    # Test different phase configurations
    phase_models = []
    for phase in [1, 2, 3, 4]:
        model_env = f"PATH_LLM_MODEL_PHASE{phase}"
        model = os.getenv(model_env)
        if model:
            phase_models.append({"phase": phase, "model": model, "env_var": model_env})

    if not phase_models:
        print("   ⚠️  No phase-specific models configured")
        return

    print(f"   🧪 Testing prompt: '{test_prompt[:50]}...'")
    print()

    for config in phase_models:
        try:
            print(f"   Phase {config['phase']} ({config['model']}):")

            client = get_llm_client(phase=config["phase"])

            request = LLMRequest(prompt=test_prompt, temperature=0.1, max_tokens=200)

            response = await client.generate(request)

            print(f"      Response: {response.content[:80]}...")
            print(f"      Tokens: {response.tokens_used}")
            print()

        except Exception as e:
            print(f"      ❌ Error: {str(e)[:60]}...")
            print()


async def demo_configuration_priority():
    """Show how phase-specific configuration works with priority"""

    print("\n🏆 Configuration Priority Demo")
    print("-" * 40)

    print("   📝 Environment Variables:")
    general_model = os.getenv("PATH_LLM_MODEL")
    phase1_model = os.getenv("PATH_LLM_MODEL_PHASE1")

    if general_model:
        print(f"      PATH_LLM_MODEL: {general_model}")
    if phase1_model:
        print(f"      PATH_LLM_MODEL_PHASE1: {phase1_model}")

    print("\n   🎯 Expected Behavior:")
    if phase1_model:
        print(f"      Phase 1 should use: {phase1_model} (phase-specific)")
    elif general_model:
        print(f"      Phase 1 should use: {general_model} (general fallback)")
    else:
        print("      Phase 1 should use: Default model")

    if os.getenv("OPENROUTER_API_KEY"):
        try:
            client = get_llm_client(phase=1)
            print("\n   ✅ Actual Result:")
            print(f"      Phase 1 uses: {client.model}")

            # Test function parameter override
            override_client = get_llm_client(
                phase=1,
                model="openai/gpt-3.5-turbo",  # Override phase-specific model
            )
            print(f"      With override: {override_client.model}")

        except Exception as e:
            print(f"   ❌ Test error: {e}")


def show_recommended_setup():
    """Show recommended phase-specific model setup"""

    print("\n💡 Recommended Phase-Specific Setup")
    print("=" * 50)

    recommendations = [
        {
            "phase": 1,
            "name": "Architecture & Requirements",
            "model": "openai/gpt-4",
            "reason": "Best reasoning for complex analysis and domain modeling",
        },
        {
            "phase": 2,
            "name": "Development Planning",
            "model": "anthropic/claude-3-sonnet",
            "reason": "Excellent for structured planning and technology decisions",
        },
        {
            "phase": 3,
            "name": "Implementation",
            "model": "meta-llama/llama-2-70b-chat",
            "reason": "Fast code generation with good performance/cost ratio",
        },
        {
            "phase": 4,
            "name": "Testing & Deployment",
            "model": "openai/gpt-3.5-turbo",
            "reason": "Efficient for test case generation and deployment scripts",
        },
    ]

    print("\n🔧 Environment Variables to Set:")
    print("```bash")
    print("export OPENROUTER_API_KEY='your-openrouter-api-key'")
    print("export PATH_LLM_PROVIDER='openrouter'")
    print()

    for rec in recommendations:
        print(f"# Phase {rec['phase']}: {rec['name']}")
        print(f"# {rec['reason']}")
        print(f"export PATH_LLM_MODEL_PHASE{rec['phase']}='{rec['model']}'")
        print()

    print("```")

    print("\n📊 Benefits of Phase-Specific Models:")
    print("   • 🎯 Optimized model selection for each phase's requirements")
    print("   • 💰 Cost optimization (use cheaper models where appropriate)")
    print("   • ⚡ Performance tuning (faster models for code generation)")
    print("   • 🔧 Flexibility (easy to experiment with different models)")
    print("   • 📈 Quality improvement (best models for critical analysis)")


if __name__ == "__main__":
    print("🚀 Starting Phase-Specific Configuration Demo...\n")

    # Show recommended setup
    show_recommended_setup()

    # Run demos
    asyncio.run(demo_phase_specific_models())
    asyncio.run(demo_model_comparison())
    asyncio.run(demo_configuration_priority())

    print("\n✅ Phase-Specific Configuration Demo Complete!")
    print("💡 Use different models optimized for each phase!")
