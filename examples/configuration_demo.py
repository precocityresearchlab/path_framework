#!/usr/bin/env uv run python
"""
PATH Framework Configuration Examples
Demonstrates flexible configuration options (no hard-coding!)
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from path_framework.core.config import get_config, set_config_file
from path_framework.core.llm_client import (
    LLMClientFactory,
    LLMProvider,
    LLMRequest,
    get_llm_client,
)


async def demo_configuration_methods():
    """Demonstrate different configuration approaches"""

    print("⚙️  PATH Framework - Configuration Methods Demo")
    print("=" * 60)

    # Method 1: Environment Variables (Most Common)
    print("\n1️⃣  Environment Variables Configuration")
    print("-" * 40)

    # Show current environment
    env_vars = [
        "PATH_LLM_PROVIDER",
        "PATH_LLM_MODEL",
        "OPENROUTER_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            if "KEY" in var:
                print(f"   {var}: {'*' * 8}{value[-4:]}")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: Not set")

    if os.getenv("OPENROUTER_API_KEY"):
        try:
            print("\n   Testing environment-based configuration...")
            client = get_llm_client()  # Uses environment variables

            request = LLMRequest(
                prompt="Say 'Environment config works!' in exactly 4 words.",
                temperature=0.1,
                max_tokens=50,
            )

            response = await client.generate(request)
            print(f"   ✅ Response: {response.content.strip()}")
            print(f"   🔧 Provider: {response.provider}")
            print(f"   🤖 Model: {response.model_used}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⚠️  No API key in environment - skipping test")

    # Method 2: Function Parameters (Runtime Override)
    print("\n2️⃣  Function Parameter Configuration")
    print("-" * 40)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        try:
            print("   Using explicit parameters to override environment...")

            # Override environment settings
            client = get_llm_client(
                provider="openrouter",
                api_key=api_key,
                model="anthropic/claude-3-haiku",  # Different from env
            )

            request = LLMRequest(
                prompt="Say 'Parameter override successful!' in 4 words.",
                temperature=0.1,
                max_tokens=50,
            )

            response = await client.generate(request)
            print(f"   ✅ Response: {response.content.strip()}")
            print(f"   🔧 Provider: {response.provider}")
            print(f"   🤖 Model: {response.model_used}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⚠️  No OPENROUTER_API_KEY - skipping test")

    # Method 3: Configuration File
    print("\n3️⃣  Configuration File")
    print("-" * 40)

    # Create a sample config file
    config_path = "demo_config.json"
    sample_config = {
        "llm": {
            "provider": "openrouter",
            "model": "openai/gpt-3.5-turbo",
            "timeout": 45,
            "temperature": 0.2,
            "max_tokens": 2000,
        }
    }

    with open(config_path, "w") as f:
        json.dump(sample_config, f, indent=2)

    print(f"   📝 Created config file: {config_path}")
    print("   📄 Content:")
    print(json.dumps(sample_config, indent=6))

    try:
        # Use config file
        set_config_file(config_path)
        config_manager = get_config()

        # This would use file config + environment API key
        llm_config = config_manager.get_llm_config()
        print("\n   📊 Resolved configuration:")
        for key, value in llm_config.items():
            if "api_key" in key and value:
                print(f"      {key}: {'*' * 8}{str(value)[-4:]}")
            else:
                print(f"      {key}: {value}")

    except Exception as e:
        print(f"   ❌ Config file error: {e}")
    finally:
        # Clean up
        if os.path.exists(config_path):
            os.remove(config_path)

    # Method 4: Programmatic Configuration
    print("\n4️⃣  Programmatic Configuration")
    print("-" * 40)

    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        try:
            # Create client with full configuration
            client = LLMClientFactory.create_client(
                provider=LLMProvider.OPENROUTER,
                api_key=api_key,
                model="meta-llama/llama-2-70b-chat",
                timeout=60,
            )

            request = LLMRequest(
                prompt="Respond with exactly: 'Programmatic config rocks!'",
                temperature=0.1,
                max_tokens=50,
            )

            response = await client.generate(request)
            print(f"   ✅ Response: {response.content.strip()}")
            print(f"   🔧 Provider: {response.provider}")
            print(f"   🤖 Model: {response.model_used}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ⚠️  No OPENROUTER_API_KEY - skipping test")

    # Method 5: Agent-Level Configuration
    print("\n5️⃣  Agent-Level Configuration")
    print("-" * 40)

    try:
        from path_framework.phases.arch.ai.domain_analyst import AIDomainAnalyst

        # Agent with custom LLM config
        agent_config = {
            "llm_provider": "openrouter",
            "llm_model": "openai/gpt-4",
            "confidence_threshold": 0.9,
        }

        agent = AIDomainAnalyst(config=agent_config)
        print("   ✅ Created agent with custom config")
        print(f"   🔧 Config: {agent_config}")

    except Exception as e:
        print(f"   ❌ Agent config error: {e}")

    print("\n🎯 Configuration Best Practices")
    print("-" * 40)
    print("✅ DO:")
    print("   • Use environment variables for API keys")
    print("   • Use config files for application settings")
    print("   • Use function parameters for runtime overrides")
    print("   • Use agent configs for specialized behavior")
    print("\n❌ DON'T:")
    print("   • Hard-code API keys in source code")
    print("   • Hard-code provider/model selections")
    print("   • Commit sensitive config files to git")
    print("   • Use global variables for configuration")


async def demo_configuration_priority():
    """Demonstrate configuration priority order"""

    print("\n🏆 Configuration Priority Demo")
    print("-" * 40)

    # Set some environment variables
    original_provider = os.getenv("PATH_LLM_PROVIDER")
    original_model = os.getenv("PATH_LLM_MODEL")

    os.environ["PATH_LLM_PROVIDER"] = "openai"  # Environment
    os.environ["PATH_LLM_MODEL"] = "gpt-3.5-turbo"  # Environment

    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("   ⚠️  Need OPENROUTER_API_KEY for priority demo")
            return

        print("   🔧 Environment: provider=openai, model=gpt-3.5-turbo")
        print(
            "   📝 Function params: provider=openrouter, model=anthropic/claude-3-sonnet"
        )
        print("   🏆 Expected result: Function params win (higher priority)")

        # Function parameters should override environment
        client = get_llm_client(
            provider="openrouter",  # Should override env
            model="anthropic/claude-3-sonnet",  # Should override env
            api_key=api_key,
        )

        request = LLMRequest(
            prompt="Say 'Priority test passed!' in exactly 4 words.",
            temperature=0.1,
            max_tokens=50,
        )

        response = await client.generate(request)
        print(f"\n   ✅ Result: {response.content.strip()}")
        print(f"   🔧 Actual provider: {response.provider}")
        print(f"   🤖 Actual model: {response.model_used}")

        if (
            response.provider == "openrouter"
            and "claude" in response.model_used.lower()
        ):
            print("   🎯 Priority order working correctly!")
        else:
            print("   ⚠️  Unexpected result - check priority logic")

    except Exception as e:
        print(f"   ❌ Priority demo error: {e}")
    finally:
        # Restore original environment
        if original_provider:
            os.environ["PATH_LLM_PROVIDER"] = original_provider
        else:
            os.environ.pop("PATH_LLM_PROVIDER", None)

        if original_model:
            os.environ["PATH_LLM_MODEL"] = original_model
        else:
            os.environ.pop("PATH_LLM_MODEL", None)


if __name__ == "__main__":
    print("🚀 Starting Configuration Demo...\n")

    # Run configuration methods demo
    asyncio.run(demo_configuration_methods())

    # Run priority demo
    asyncio.run(demo_configuration_priority())

    print("\n✅ Configuration Demo Complete!")
    print("💡 Use flexible configuration - never hard-code values!")
