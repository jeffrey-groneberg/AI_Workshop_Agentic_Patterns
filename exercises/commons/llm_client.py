"""
Provider-agnostic OpenAI client factory.

Supports three providers interchangeably:
- OpenAI (direct API)
- Azure OpenAI (via AzureOpenAI client)
- GitHub Models (via OpenAI client with custom base_url)

Configure via environment variables — see .env.example for details.
"""

import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI

logger = logging.getLogger(__name__)

# Load .env from the project root (two levels up from commons/)
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(_env_path)

# ── Provider constants ──────────────────────────────────────────────────────

PROVIDER_OPENAI = "openai"
PROVIDER_AZURE = "azure"
PROVIDER_GITHUB = "github"

GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"

# ── Default models per provider ─────────────────────────────────────────────

_DEFAULT_MODELS: dict[str, str] = {
    PROVIDER_OPENAI: "gpt-4o",
    PROVIDER_AZURE: os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
    PROVIDER_GITHUB: "gpt-4o",
}


def get_provider() -> str:
    """Return the configured LLM provider name (lowercase)."""
    provider = os.getenv("LLM_PROVIDER", PROVIDER_OPENAI).lower().strip()
    if provider not in (PROVIDER_OPENAI, PROVIDER_AZURE, PROVIDER_GITHUB):
        raise ValueError(
            f"Unknown LLM_PROVIDER '{provider}'. "
            f"Must be one of: {PROVIDER_OPENAI}, {PROVIDER_AZURE}, {PROVIDER_GITHUB}"
        )
    return provider


def get_client() -> OpenAI | AzureOpenAI:
    """
    Create and return an OpenAI-compatible client for the configured provider.

    Returns:
        An OpenAI or AzureOpenAI client instance.
    """
    provider = get_provider()

    if provider == PROVIDER_OPENAI:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        client = OpenAI(api_key=api_key)
        logger.info("Initialized OpenAI client (provider: openai)")
        return client

    if provider == PROVIDER_AZURE:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        if not endpoint or not api_key:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required "
                "when LLM_PROVIDER=azure"
            )
        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        logger.info("Initialized AzureOpenAI client (provider: azure)")
        return client

    # provider == PROVIDER_GITHUB
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is required when LLM_PROVIDER=github")
    client = OpenAI(
        base_url=GITHUB_MODELS_BASE_URL,
        api_key=token,
    )
    logger.info("Initialized OpenAI client (provider: github-models)")
    return client


def get_model() -> str:
    """
    Return the model name for the configured provider.

    Uses MODEL_NAME env var if set, otherwise falls back to provider defaults.
    """
    custom_model = os.getenv("MODEL_NAME")
    if custom_model:
        return custom_model
    provider = get_provider()
    return _DEFAULT_MODELS[provider]
