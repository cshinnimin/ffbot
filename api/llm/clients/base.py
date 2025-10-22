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

        prompt_count = usage.get('prompt_tokens')
        completion_count = usage.get('completion_tokens')
        prompt_string = f"[{self.__class__.__name__}] Prompt Tokens     : {prompt_count}"
        completion_string = f"[{self.__class__.__name__}] Completion Tokens : {completion_count}"
        
        cached_string = ''
        prompt_token_details = usage.get('prompt_tokens_details')
        if isinstance(prompt_token_details, dict):
            cached_count = prompt_token_details.get('cached_tokens')
            cached_string = f"[{self.__class__.__name__}] Cached Tokens     : {cached_count}"

        # Step 5 - If token data present, print to terminal
        
        if USE_COLOUR:
            if prompt_string: print(f"\x1b[1;33m{prompt_string}\x1b[0m")
            if cached_string: print(f"\x1b[1;33m{cached_string}\x1b[0m")
            if completion_string: print(f"\x1b[1;33m{completion_string}\x1b[0m")
        else:
            if prompt_string: print(prompt_string)
            if cached_string: print(cached_string)
            if completion_string: print(completion_string)

        return data

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        
        raise NotImplementedError


