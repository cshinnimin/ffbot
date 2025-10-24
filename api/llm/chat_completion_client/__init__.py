from typing import Dict, Type

from .base import ChatCompletionLlmClient
from .openai_client import OpenAIChatCompletionLlmClient
from .openrouter_client import OpenRouterChatCompletionLlmClient
from .ollama_client import OllamaChatCompletionLlmClient

PROVIDER_CLIENTS: Dict[str, Type[ChatCompletionLlmClient]] = {
    "openai": OpenAIChatCompletionLlmClient,
    "openrouter": OpenRouterChatCompletionLlmClient,
    "ollama": OllamaChatCompletionLlmClient,
}

def create_client(config):
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)
