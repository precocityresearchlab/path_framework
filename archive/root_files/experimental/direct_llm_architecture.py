#!/usr/bin/env uv run python
"""
Direct Gemma 3 27B Architecture Generation Test
Bypasses the AI agents and calls LLM directly for architecture analysis
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the path framework to the Python path
sys.path.append(str(Path(__file__).parent))

from path_framework.core.llm_client import LLMRequest, get_llm_client


async def generate_architecture_with_llm():
    """Generate architecture using Gemma 3 27B directly"""

    print("🏗️ Direct LLM Architecture Generation with Gemma 3 27B")
    print("=" * 60)

    # Project details
    project_name = "Helpdesk API"
    project_description = """
    A Helpdesk API is an application programming interface that allows external systems
    to interact with a helpdesk or customer support platform programmatically. It enables
    operations such as creating, updating, and retrieving support tickets; managing users
    or agents; automating workflows; and integrating with other tools (e.g. CRMs, chatbots,
    or email systems). Helpdesk APIs are commonly used to streamline support processes,
    enable custom interfaces, and support data synchronisation across enterprise systems.

    Target users: ERP System integrations
    Project type: API Service
    """

    print(f"📋 Project: {project_name}")
    print(f"📝 Description: {project_description.strip()}")

    try:
        # Get LLM client
        print("\n🔄 Creating LLM client...")
        llm_client = get_llm_client(phase=1)
        print(f"✅ Client created: {type(llm_client).__name__}")

        # Step 1: Requirements Analysis
        print("\n🔍 Step 1: Requirements Analysis with Gemma 3 27B...")
        requirements_prompt = f"""
        You are a senior software architect analyzing project requirements.

        Project: {project_name}
        Description: {project_description}

        Analyze this project and extract the key functional requirements. Respond in JSON format:

        {{
            "requirements": [
                {{
                    "id": 1,
                    "title": "Requirement Title",
                    "description": "Detailed description",
                    "type": "functional|non_functional|business",
                    "priority": "high|medium|low",
                    "acceptance_criteria": ["criterion 1", "criterion 2"]
                }}
            ],
            "business_rules": [
                "Business rule 1",
                "Business rule 2"
            ],
            "stakeholders": [
                "Primary stakeholder 1",
                "Secondary stakeholder 2"
            ]
        }}

        Extract 5-7 key requirements for this helpdesk API system.
        """

        req_request = LLMRequest(
            prompt=requirements_prompt, temperature=0.3, max_tokens=800
        )

        req_response = await llm_client.generate(req_request)
        print("✅ Requirements Analysis Complete!")
        print(f"📊 Tokens used: {req_response.tokens_used}")
        print(f"📝 Response preview: {req_response.content[:200]}...")

        # Try to parse requirements
        try:
            requirements_data = json.loads(req_response.content)
            print(
                f"🎯 Successfully parsed {len(requirements_data.get('requirements', []))} requirements"
            )
        except json.JSONDecodeError:
            print("⚠️  Requirements response not in valid JSON, but that's okay")
            requirements_data = {
                "requirements": [],
                "business_rules": [],
                "stakeholders": [],
            }

        # Step 2: System Architecture Design
        print("\n🏛️ Step 2: System Architecture Design with Gemma 3 27B...")
        architecture_prompt = f"""
        You are a senior system architect designing the architecture for this project.

        Project: {project_name}
        Description: {project_description}

        Based on the requirements, design a system architecture. Respond in JSON format:

        {{
            "architecture_pattern": "microservices|monolithic|layered|hexagonal",
            "technology_stack": {{
                "backend_language": "python|java|nodejs|go",
                "web_framework": "fastapi|flask|spring|express",
                "database": "postgresql|mysql|mongodb|redis",
                "cache": "redis|memcached",
                "message_queue": "rabbitmq|kafka|redis",
                "api_gateway": "nginx|kong|zuul"
            }},
            "components": [
                {{
                    "name": "Component Name",
                    "responsibility": "What this component does",
                    "interfaces": ["API endpoints or interfaces"],
                    "dependencies": ["Other components it depends on"]
                }}
            ],
            "quality_attributes": {{
                "scalability": "High|Medium|Low",
                "availability": "99.9%|99.5%|99%",
                "security": "Enterprise|Standard|Basic",
                "performance": "High|Medium|Low"
            }}
        }}

        Design a production-ready architecture for this helpdesk API system.
        """

        arch_request = LLMRequest(
            prompt=architecture_prompt, temperature=0.2, max_tokens=1000
        )

        arch_response = await llm_client.generate(arch_request)
        print("✅ Architecture Design Complete!")
        print(f"📊 Tokens used: {arch_response.tokens_used}")
        print(f"📝 Response preview: {arch_response.content[:200]}...")

        # Try to parse architecture
        try:
            architecture_data = json.loads(arch_response.content)
            print(
                f"🏗️ Successfully parsed architecture with {len(architecture_data.get('components', []))} components"
            )
        except json.JSONDecodeError:
            print("⚠️  Architecture response not in valid JSON, but that's okay")
            architecture_data = {"components": [], "technology_stack": {}}

        # Step 3: API Design
        print("\n🔌 Step 3: API Design with Gemma 3 27B...")
        api_prompt = f"""
        You are an API architect designing RESTful APIs for this system.

        Project: {project_name}
        Description: {project_description}

        Design the main API endpoints for this helpdesk system. Respond in JSON format:

        {{
            "api_endpoints": [
                {{
                    "method": "GET|POST|PUT|DELETE",
                    "path": "/api/v1/endpoint",
                    "description": "What this endpoint does",
                    "request_body": {{"example": "request structure"}},
                    "response": {{"example": "response structure"}},
                    "authentication": "required|optional|none"
                }}
            ],
            "authentication": {{
                "type": "JWT|OAuth2|API_Key",
                "description": "How authentication works"
            }},
            "data_models": [
                {{
                    "name": "ModelName",
                    "fields": [
                        {{"name": "field_name", "type": "string|integer|boolean", "required": true}}
                    ]
                }}
            ]
        }}

        Design 6-8 core API endpoints for ticket management, user management, and reporting.
        """

        api_request = LLMRequest(prompt=api_prompt, temperature=0.2, max_tokens=1000)

        api_response = await llm_client.generate(api_request)
        print("✅ API Design Complete!")
        print(f"📊 Tokens used: {api_response.tokens_used}")
        print(f"📝 Response preview: {api_response.content[:200]}...")

        # Save all results
        output_dir = Path("./projects/Helpdesk API/llm_generated_architecture")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save raw responses
        with open(output_dir / "requirements_analysis.txt", "w") as f:
            f.write("# Requirements Analysis - Generated by Gemma 3 27B\n\n")
            f.write(f"Project: {project_name}\n")
            f.write(f"Tokens used: {req_response.tokens_used}\n")
            f.write(f"Model: {req_response.model_used}\n\n")
            f.write("## Raw Response:\n")
            f.write(req_response.content)

        with open(output_dir / "system_architecture.txt", "w") as f:
            f.write("# System Architecture - Generated by Gemma 3 27B\n\n")
            f.write(f"Project: {project_name}\n")
            f.write(f"Tokens used: {arch_response.tokens_used}\n")
            f.write(f"Model: {arch_response.model_used}\n\n")
            f.write("## Raw Response:\n")
            f.write(arch_response.content)

        with open(output_dir / "api_design.txt", "w") as f:
            f.write("# API Design - Generated by Gemma 3 27B\n\n")
            f.write(f"Project: {project_name}\n")
            f.write(f"Tokens used: {api_response.tokens_used}\n")
            f.write(f"Model: {api_response.model_used}\n\n")
            f.write("## Raw Response:\n")
            f.write(api_response.content)

        # Summary
        total_tokens = (
            req_response.tokens_used
            + arch_response.tokens_used
            + api_response.tokens_used
        )

        print("\n🎉 LLM Architecture Generation Complete!")
        print("✅ Successfully generated:")
        print(f"   • Requirements Analysis ({req_response.tokens_used} tokens)")
        print(f"   • System Architecture ({arch_response.tokens_used} tokens)")
        print(f"   • API Design ({api_response.tokens_used} tokens)")
        print(f"📊 Total tokens used: {total_tokens}")
        print("💰 Total cost: FREE (Gemma 3 27B)")
        print(f"📁 Artifacts saved to: {output_dir}")

        return True

    except Exception as e:
        print(f"❌ LLM Architecture Generation Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Starting Direct LLM Architecture Generation...")
    success = asyncio.run(generate_architecture_with_llm())
    if success:
        print("\n🚀 LLM architecture generation successful!")
        print(
            "Check the generated artifacts in projects/Helpdesk API/llm_generated_architecture/"
        )
    else:
        print("\n💥 LLM architecture generation failed.")
