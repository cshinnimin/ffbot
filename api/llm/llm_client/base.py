from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class LlmClient(ABC):
    """Top-level abstraction for all LLM clients."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> Any:
        """Send a list of messages to the LLM and return the response."""
        raise NotImplementedError

# __all__ defines the set of symbols the module considers part of its public API
__all__ = ["LlmClient"]
