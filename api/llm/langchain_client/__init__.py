from typing import Dict, Type

from .base import LangchainBase
from .openai_langchain_client import OpenAILangchainClient

PROVIDER_CLIENTS: Dict[str, Type[LangchainBase]] = {
    "openai_langchain": OpenAILangchainClient,
}

def create_client(config):
    provider = str(config.get("LLM_PROVIDER", "")).lower()
    try:
        client_cls = PROVIDER_CLIENTS[provider]
    except KeyError:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
    return client_cls(config)
