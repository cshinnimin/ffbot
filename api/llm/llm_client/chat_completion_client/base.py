from abc import abstractmethod
from typing import Any, Dict, List, Optional

from .. import LlmClient
import requests
import threading
import time

from api.utils.console import print_to_console

# Module-level cumulative token counters (persist for lifetime of process)
# They are protected by _cumulative_lock when updated.
_cumulative_lock = threading.Lock()
_cumulative_api_messages = 1
_cumulative_api_seconds = 0.0
_cumulative_prompt_tokens = 0
_cumulative_completion_tokens = 0
_cumulative_cached_tokens = 0

# Base class for all Chat Completion clients
class ChatCompletionLlmClient(LlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    # Private helper to safely coerce values to integers
    def _safe_int(self, v: Any) -> int:
        try:
            return int(v) if v is not None else 0
        except Exception:
            return 0

    # Helper method for sending the payload and printing information about the request to the console
    # A leading underscore in the name signals (by convention) the method is internal / protected
    def _post(self, url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 60) -> Any:
        """Send a POST request with JSON and return parsed JSON."""
        # Step 2 - Print information about LLM API endpoint URL, model, and cumulative usage count
        global _cumulative_api_messages
        post_label = f"[{self.__class__.__name__}] POST {url} model={payload.get('model')} msgs={len(payload.get('messages', []))}"
        api_count_string = f"[{self.__class__.__name__}] API Message Count : {_cumulative_api_messages}"
        print_to_console(post_label, 'yellow')
        print_to_console(api_count_string, 'yellow')

        # Step 3 - POST the message to the LLMs API and load the JSON response in to `data` variable
        start_time = time.perf_counter()
        res = requests.post(url, headers=headers, json=payload, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # Step 4 - Get token usage from response, if present
        usage = data.get('usage') if isinstance(data, dict) else {}
        prompt_count = self._safe_int(usage.get('prompt_tokens'))
        completion_count = self._safe_int(usage.get('completion_tokens'))
        prompt_token_details = usage.get('prompt_tokens_details') if isinstance(usage, dict) else {}
        cached_count = self._safe_int(prompt_token_details.get('cached_tokens') if isinstance(prompt_token_details, dict) else None)

        # Step 5 - Update module-level cumulative counters in a thread-safe way
        global _cumulative_prompt_tokens, _cumulative_completion_tokens, _cumulative_cached_tokens, _cumulative_api_seconds
        with _cumulative_lock:
            _cumulative_api_messages += 1
            _cumulative_prompt_tokens += prompt_count
            _cumulative_completion_tokens += completion_count
            _cumulative_cached_tokens += cached_count
            _cumulative_api_seconds += elapsed_time

        # Step 6 - Prepare strings to print information to the terminal console
        time_string = f"[{self.__class__.__name__}] Request Time      : {elapsed_time:.1f}s (Total: {_cumulative_api_seconds:.1f}s)"
        prompt_string = f"[{self.__class__.__name__}] Prompt Tokens     : {prompt_count} (Total: {_cumulative_prompt_tokens})"
        completion_string = f"[{self.__class__.__name__}] Completion Tokens : {completion_count} (Total: {_cumulative_completion_tokens})"
        cached_string = ''
        if cached_count is not None:
            cached_string = f"[{self.__class__.__name__}] Cached Tokens     : {cached_count} (Total: {_cumulative_cached_tokens})"

        # Step 7 - Print token information to the terminal console using helper
        print_to_console(time_string, 'yellow')
        print_to_console(prompt_string, 'yellow')
        print_to_console(cached_string, 'yellow')
        print_to_console(completion_string, 'yellow')

        return data

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        raise NotImplementedError
