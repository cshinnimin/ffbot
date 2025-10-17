from typing import Dict, Type

from .base import LlmClient
from .openai_client import OpenAIClient
from .openrouter_client import OpenRouterClient
from .ollama_client import OllamaClient


PROVIDER_CLIENTS: Dict[str, Type[LlmClient]] = {
    "openai": OpenAIClient,
    "openrouter": OpenRouterClient,
    "ollama": OllamaClient,
}


def create_client(config):
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)


