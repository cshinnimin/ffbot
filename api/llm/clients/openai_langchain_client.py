from typing import Any, Dict, List, Optional

from .base import LlmClient


class OpenAILangchainClient(LlmClient):
    """Skeleton client for OpenAI via LangChain.

    This file intentionally contains only a minimal, non-implemented
    `chat` method so it can be imported without causing runtime errors.
    Implementation will be added later.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        raise NotImplementedError("OpenAILangchainClient.chat is not implemented yet")
