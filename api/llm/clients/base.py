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

        # Step 1 - Check whether to use colour in terminal logging
        USE_COLOUR = sys.stdout.isatty() and not os.environ.get('NO_COLOR')

        # Step 2 - Print information about LLM API endpoint URL, model
        post_label = f"[{self.__class__.__name__}] POST {url} model={payload.get('model')} msgs={len(payload.get('messages', []))}"
        if USE_COLOUR:
            print(f"\x1b[1;33m{post_label}\x1b[0m")
        else:
            print(post_label)

        # Step 3 - POST the message to the LLMs API and load the JSON response in to `data` variable
        res = requests.post(url, headers=headers, json=payload, timeout=timeout)
        res.raise_for_status()
        data = res.json()

        # Step 4 - Check if token usage information is present in the response
        if not isinstance(data, dict):
            return data

        usage = data.get('usage')
        if not isinstance(usage, dict):
            return data

        pt = usage.get('prompt_tokens')
        ct = usage.get('completion_tokens')
        if pt is None or ct is None:
            return data

        # Step 5 - If token data present, print to terminal
        prompt_count = f"[{self.__class__.__name__}] Prompt Tokens     : {pt}"
        completion_count = f"[{self.__class__.__name__}] Completion Tokens : {ct}"
        if USE_COLOUR:
            print(f"\x1b[1;33m{prompt_count}\x1b[0m")
            print(f"\x1b[1;33m{completion_count}\x1b[0m")
        else:
            print(prompt_count)
            print(completion_count)

        return data

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        
        raise NotImplementedError


