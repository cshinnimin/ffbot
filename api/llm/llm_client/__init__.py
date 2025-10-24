from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type

from .base import LlmClient

# Unified provider registry for all LLM client families.
# We import the concrete classes lazily at module import time from the
# subpackages so callers can simply call create_client(config).
from .chat_completion_client.openai_client import OpenAIChatCompletionLlmClient
from .chat_completion_client.openrouter_client import OpenRouterChatCompletionLlmClient
from .chat_completion_client.ollama_client import OllamaChatCompletionLlmClient
from .langchain_client.openai_langchain_client import OpenAILangchainLlmClient

PROVIDER_CLIENTS: Dict[str, Type[LlmClient]] = {
    "openai": OpenAIChatCompletionLlmClient,
    "openrouter": OpenRouterChatCompletionLlmClient,
    "ollama": OllamaChatCompletionLlmClient,
    "openai_langchain": OpenAILangchainLlmClient,
}

def create_client(config: Dict[str, Any]) -> LlmClient:
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)

# __all__ defines the set of symbols the module considers part of its public API
__all__ = ["LlmClient", "create_client"]
