from typing import Any, Dict, List, Optional
import threading
import time
import json
import os

from pydantic import BaseModel, Field

from .base import LangchainLlmClient
from api.utils.console import print_to_console
from api.utils.math import safe_int
from langchain_community.callbacks import get_openai_callback

# provider-specific imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# suppress Langchain deprecation warnings
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

_K_FOR_HINTS = 3
_K_FOR_DOCUMENTS = 5
_K_FOR_ADDRESSES = 20
_SIMILARITY_FOR_HINTS = 0.4
_SIMILARITY_FOR_DOCUMENTS = 0.6
_SIMILARITY_FOR_ADDRESSES = 0.5

# Module-level cumulative stat counters (persist for lifetime of process)
# Protected by _cumulative_lock when updated.
_cumulative_lock = threading.Lock()
_cumulative_api_messages = 1
_cumulative_api_seconds = 0.0
_cumulative_prompt_tokens = 0
_cumulative_completion_tokens = 0
_cumulative_cached_tokens = 0
_cumulative_total_cost = 0.0


class ReadAddressesInput(BaseModel):
    addresses: List[str] = Field(description="The RAM addresses we want the values for.")


class SafeChatOpenAI(ChatOpenAI):
    """
    Subclass that ensures a 'stop' parameter is never forwarded to the provider.
    Some newer OpenAI models (such as gpt-5) reject a 'stop' parameter.
    """
    def __call__(self, *args, **kwargs):
        kwargs.pop("stop", None)
        return super().__call__(*args, **kwargs)

    async def __acall__(self, *args, **kwargs):
        kwargs.pop("stop", None)
        return await super().__acall__(*args, **kwargs)

    # Override generate/agenerate too—some LangChain versions call these directly.
    def generate(self, messages, stop=None, **kwargs):
        # ensure stop is never forwarded
        return super().generate(messages, stop=None, **kwargs)

    async def agenerate(self, messages, stop=None, **kwargs):
        return await super().agenerate(messages, stop=None, **kwargs)


class OpenAILangchainLlmClient(LangchainLlmClient):
    def __init__(self, config: Dict[str, Any]):
        # Ensure provider-specific environment/config is set before base __init__
        api_key = config.get("LLM_API_KEY")
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key

        super().__init__(config)

    # Provider factory used by base class to create the LLM instance
    def _get_llm(self, model_name: str, temperature: float):
        # Use a SafeChatOpenAI to specify the LLM. This is a custom wrapper
        # class that wraps OpenAI's ChatOpenAI() and provides an override
        # to ensure that a `stop` parameter is never forwarded to the provider
        # since newer models like gpt-5 do not support this parameter
        return SafeChatOpenAI(model_name=model_name, temperature=temperature)

    # Provider factory used by base class to create embeddings for Chroma
    def _get_embeddings(self):
        return OpenAIEmbeddings()

    def _chat(self, messages: List[Dict[str, Any]]) -> str:
        new_message = messages[-1].get("content", "") if messages else ""

        start_time = time.perf_counter()

        # Search the documents vector DB for documents relevant to this message
        print_to_console('Searching vector DB for relevant documents...', 'yellow')
        documents_text = self._retrieve_from_vector_db(
            self._vectordb_documents,
            new_message,
            _K_FOR_DOCUMENTS,
            _SIMILARITY_FOR_DOCUMENTS,
            space_chunks=True,
        )

        # Search the hints vector DB for hints relevant to this message
        print_to_console('Searching vector DB for relevant hints...', 'yellow')
        hints_text = self._retrieve_from_vector_db(
            self._vectordb_hints,
            new_message,
            _K_FOR_HINTS,
            _SIMILARITY_FOR_HINTS,
            space_chunks=False,
        )

        # Search the addresses vector DB for memory addresses relevant to this message
        print_to_console('Searching vector DB for relevant memory addresses...', 'yellow')
        addresses_text = self._retrieve_from_vector_db(
            self._vectordb_addresses,
            new_message,
            _K_FOR_ADDRESSES,
            _SIMILARITY_FOR_ADDRESSES,
            space_chunks=True,
        )

        # create instructions text from concatenation of entire initial instructions document
        # (at data/training/langchain/initial-instructions.md) and the top-k chunks from
        # the hints document (at data/training/langchain/hints.md - every bullet becomes a chunk)
        instructions_text = self._initial_instructions + "\n" + hints_text + "\n" + documents_text
        instructions_text += "\n\n#Memory Addresses of Interest\n\n" + addresses_text

        with get_openai_callback() as cb:
            result = self._executor.run({"input": new_message, "instructions": instructions_text, "history": messages})
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            # Extract token counts (use safe conversion)
            prompt_count = safe_int(getattr(cb, 'prompt_tokens', None))
            completion_count = safe_int(getattr(cb, 'completion_tokens', None))
            cached_count = safe_int(getattr(cb, 'prompt_tokens_cached', None))

            # Extract and normalize cost
            try:
                cost_val = float(getattr(cb, 'total_cost', 0.0))
            except Exception:
                cost_val = 0.0

            # Update module-level cumulative counters in a thread-safe way
            global _cumulative_prompt_tokens, _cumulative_completion_tokens, _cumulative_cached_tokens, _cumulative_api_seconds, _cumulative_api_messages, _cumulative_total_cost
            with _cumulative_lock:
                _cumulative_api_messages += 1
                _cumulative_prompt_tokens += prompt_count
                _cumulative_completion_tokens += completion_count
                _cumulative_cached_tokens += cached_count
                _cumulative_api_seconds += elapsed_time
                _cumulative_total_cost += cost_val

            # Prepare strings including cumulative totals in parentheses
            cumulative_total_tokens = _cumulative_prompt_tokens + _cumulative_completion_tokens

            total_string = f"Total Tokens      : {getattr(cb, 'total_tokens', 0)} (Total: {cumulative_total_tokens})"
            prompt_string = f"Prompt Tokens     : {prompt_count} (Total: {_cumulative_prompt_tokens})"
            cached_string = ''
            if cached_count is not None:
                cached_string = f"Cached Tokens     : {cached_count} (Total: {_cumulative_cached_tokens})"
            completion_string = f"Completion Tokens : {completion_count} (Total: {_cumulative_completion_tokens})"
            # Format cost: per-call rounded to 4 decimals, cumulative rounded to 2 decimals
            cost_string = f"Total Cost (USD)  : ${cost_val:.4f} (Total: ${_cumulative_total_cost:.2f})"
            time_string = f"Request Time      : {elapsed_time:.1f}s (Total: {_cumulative_api_seconds:.1f}s)"

            print_to_console()
            print_to_console(total_string, color='yellow')
            print_to_console(prompt_string, color='yellow')
            if cached_string:
                print_to_console(cached_string, color='yellow')
            print_to_console(completion_string, color='yellow')
            print_to_console(cost_string, color='yellow')
            print_to_console(time_string, color='yellow')

        # Return answer in JSON format expected by the front end.
        # Use json.dumps to ensure all characters (quotes, backslashes, newlines,
        # and other control characters) are properly escaped.
        return json.dumps({"answer": str(result)})


def create_langchain_client(config: Dict[str, any]):
    """Simple constructor helper for the OpenAI langchain client.

    This keeps instantiation local to the provider module and avoids a
    separate registry/factory when only one provider is used.
    """
    provider = (config.get("LLM_PROVIDER") or "openai").lower()
    if provider != "openai":
        raise ValueError(f"Only 'openai' provider supported by this factory: got '{provider}'")
    return OpenAILangchainLlmClient(config)