from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import requests
import os
import sys


# Interface (Base Class) for all LLM clients
class LlmClient(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config


    # Helper method for sending the payload and printing information about the request to the console
    # A leading underscore in the name signals (by convention) the method is internal / protected
    def _post(self, url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 60) -> Any:
        """Send a POST request with JSON and return parsed JSON."""

        # Step 1 - Post the request to the LLM and put the response JSON in the `data` variable
        print(f"[{self.__class__.__name__}] POST {url} model={payload.get('model')} msgs={len(payload.get('messages', []))}")
        res = requests.post(url, headers=headers, json=payload, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        # end Step 1

        # Step 2 - Check if token usage information is present in the response
        if not isinstance(data, dict):
            return data

        usage = data.get('usage')
        if not isinstance(usage, dict):
            return data

        pt = usage.get('prompt_tokens')
        ct = usage.get('completion_tokens')
        if pt is None or ct is None:
            return data
        # end Step 2

        # Step 3 - If token data present, print to terminal, in colour if possible
        label = f"[{self.__class__.__name__}] tokens prompt={pt} completion={ct}"
        if sys.stdout.isatty() and not os.environ.get('NO_COLOR'):
            # Bold yellow for visibility in terminals
            print(f"\x1b[1;33m{label}\x1b[0m")
        else:
            print(label)
        # end Step 3

        return data

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        
        raise NotImplementedError


