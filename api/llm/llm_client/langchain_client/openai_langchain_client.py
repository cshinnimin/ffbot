from typing import Any, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

from .base import LangchainLlmClient
from api.utils.console import print_to_console
from langchain.schema import Document
from langchain_community.callbacks import get_openai_callback

# suppress Langchain deprecation warnings
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

_K_FOR_HINTS = 3
_K_FOR_DOCUMENTS = 3
_K_FOR_ADDRESSES = 30
_SIMILARITY_FOR_HINTS = 0.4
_SIMILARITY_FOR_DOCUMENTS = 0.6
_SIMILARITY_FOR_ADDRESSES = 0.4

class ReadAddressesInput(BaseModel):
    addresses: List[str] = Field(description="The RAM addresses we want the values for.")

class OpenAILangchainLlmClient(LangchainLlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def _make_tools(self) -> List[Any]:
        """
        Create the Tool objects for Langchain to use.
        """
        # The tool creation implementation is provided by the base class.
        # Subclasses can override this if they need different tools.
        return super()._make_tools()

    def _create_executor(self) -> Any:
        """
        Create an AgentExecutor for a session that accepts {instructions} and {history} plus {input}.
        We include the full in-session history via the {history} variable so the agent sees conversation context.
        """
        
        # The executor construction is provided by the base class. Subclasses
        # may override this if they need custom behaviour.
        return super()._create_executor()
    

    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        new_message = messages[-1].get("content", "") if messages else ""

        # Search the documents vector DB for documents relevant to this message
        print_to_console('Searching vector DB for relevant documents...', 'yellow')
        documents_text = self._retrieve_from_vector_db(
            self._vectordb_documents,
            new_message,
            _K_FOR_DOCUMENTS,
            _SIMILARITY_FOR_DOCUMENTS,
            space_chunks=True,
        )

        print_to_console()
        print_to_console('Documents Retrieved from Vector DB:', color='yellow')
        print_to_console(documents_text)

        # Search the hints vector DB for hints relevant to this message
        print_to_console('Searching vector DB for relevant hints...', 'yellow')
        hints_text = self._retrieve_from_vector_db(
            self._vectordb_hints,
            new_message,
            _K_FOR_HINTS,
            _SIMILARITY_FOR_HINTS,
            space_chunks=False,
        )

        print_to_console()
        print_to_console('Hints Retrieved from Vector DB:', color='yellow')
        print_to_console(hints_text)

        # Search the addresses vector DB for memory addresses relevant to this message
        print_to_console('Searching vector DB for relevant memory addresses...', 'yellow')
        addresses_text = self._retrieve_from_vector_db(
            self._vectordb_addresses,
            new_message,
            _K_FOR_ADDRESSES,
            _SIMILARITY_FOR_ADDRESSES,
            space_chunks=True,
        )

        print_to_console()
        print_to_console('Addresses Retrieved from Vector DB:', color='yellow')
        print_to_console(addresses_text)

        # create instructions text from concatenation of entire initial instructions document
        # (at data/training/langchain/initial-instructions.md) and the top-k chunks from
        # the hints document (at data/training/langchain/hints.md - every bullet becomes a chunk)
        instructions_text = self._initial_instructions + "\n" + hints_text + "\n" + documents_text
        instructions_text += "\n\n#Memory Addresses of Interest\n\n" + addresses_text

        with get_openai_callback() as cb:
            result = self._executor.run({"input": new_message, "instructions": instructions_text, "history": []})
            #result = self._executor.run({"input": new_message, "instructions": instructions_text, "documents": documents_text, "addresses": addresses_text})

            total_string = f"Total Tokens: {cb.total_tokens}"
            prompt_string = f"Prompt Tokens: {cb.prompt_tokens}"
            cached_string = f"Cached Tokens: {cb.prompt_tokens_cached}"
            completion_string = f"Completion Tokens: {cb.completion_tokens}"
            cost_string = f"Total Cost (USD): ${cb.total_cost}"

            print()
            print_to_console(total_string, color='yellow')
            print_to_console(prompt_string, color='yellow')
            print_to_console(cached_string, color='yellow')
            print_to_console(completion_string, color='yellow')
            print_to_console(cost_string, color='yellow')

        return '{"answer": "' + result + '"}'