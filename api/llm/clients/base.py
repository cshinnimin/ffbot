from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

# Interface (Base Class) for all LLM clients
class LlmClient(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], stream: bool = False, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Return a response in the unified shape expected by the React app's parseResponse."""
        raise NotImplementedError


