from typing import Any, Dict, Type
import importlib

from .base import LlmClient

# Map logical provider names to the full import path of the concrete client class.
# We keep these as strings so importing this package doesn't import the concrete
# client modules (and any heavy dependencies like langchain) at package import time.
_PROVIDER_CLASS_PATHS: Dict[str, str] = {
    "openai": "api.llm.llm_client.chat_completion_client.openai_client.OpenAIChatCompletionLlmClient",
    "openrouter": "api.llm.llm_client.chat_completion_client.openrouter_client.OpenRouterChatCompletionLlmClient",
    "ollama": "api.llm.llm_client.chat_completion_client.ollama_client.OllamaChatCompletionLlmClient",
    "openai_langchain": "api.llm.llm_client.langchain_client.openai_langchain_client.OpenAILangchainLlmClient",
}

def _import_client_class(path: str) -> Type[LlmClient]:
    """Import and return the client class given a full import path."""
    module_path, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    return cls


def create_client(config: Dict[str, Any]) -> LlmClient:
    provider = str(config.get("LLM_PROVIDER", "")).lower()

    try:
        class_path = _PROVIDER_CLASS_PATHS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    client_class = _import_client_class(class_path)

    return client_class(config)


__all__ = ["LlmClient", "create_client"]
