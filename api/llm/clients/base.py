from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

# Interface (Base Class) for all LLM clients
class LlmClient(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string """
        
        raise NotImplementedError


