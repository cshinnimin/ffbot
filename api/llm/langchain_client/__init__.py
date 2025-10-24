from typing import Dict, Type

from .base import LangchainLlmClient
from .openai_langchain_client import OpenAILangchainLlmClient

PROVIDER_CLIENTS: Dict[str, Type[LangchainLlmClient]] = {
    "openai_langchain": OpenAILangchainLlmClient,
}

def create_client(config):
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)
