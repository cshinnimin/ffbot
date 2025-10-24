from typing import Dict, Type

from .base import ChatCompletionClientBase
from .openai_client import OpenAIChatCompletionClient
from .openrouter_client import OpenRouterChatCompletionClient
from .ollama_client import OllamaChatCompletionClient

PROVIDER_CLIENTS: Dict[str, Type[ChatCompletionClientBase]] = {
    "openai": OpenAIChatCompletionClient,
    "openrouter": OpenRouterChatCompletionClient,
    "ollama": OllamaChatCompletionClient,
}


def create_client(config):
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)
