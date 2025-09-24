# PathBridge Configuration

This directory contains configuration files for the PathBridge agent system.

## Configuration Files

- `agent_profiles.yaml` - Agent profile configurations
- `llm_providers.yaml` - LLM provider settings
- `communication.yaml` - Inter-agent communication settings
- `validation.yaml` - Human validation workflow settings
- `knowledge_base.yaml` - Knowledge base configuration

## Environment Variables

PathBridge uses environment variables for sensitive configuration:
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `PATHBRIDGE_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)