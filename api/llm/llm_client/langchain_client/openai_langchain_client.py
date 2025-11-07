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


class ReadAddressesInput(BaseModel):
    addresses: List[str] = Field(description="The RAM addresses we want the values for.")

class OpenAILangchainLlmClient(LangchainLlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def now_iso(self) -> str:
        return datetime.utcnow().isoformat()

    def _retrieve_instructions_from_vector_db(self, user_input: str, k: int = 6) -> str:
        """
        Retrieve top-k instruction chunks from the vector DB and concatenate them.
        Always include initial instructions from data/training/langchain/initial-instructions.md
        in every message that goes to the LLM, followed by the top-k instruction chunks.
        """
        docs: List[Document] = self._vectordb.similarity_search(user_input, k=k)
        return self._initial_instructions + "\n---\n".join([d.page_content for d in docs])
    

    def _make_tools(self) -> List[Any]:
        """
        Create the Tool objects for Langchain to use.
        """
        # The tool creation implementation is provided by the base class.
        # Subclasses can override this if they need different tools.
        return super()._make_tools()

    def _create_executor(self, temperature: Optional[float] = None) -> Any:
        """
        Create an AgentExecutor for a session that accepts {instructions} and {history} plus {input}.
        We include the full in-session history via the {history} variable so the agent sees conversation context.
        """
        
        # The executor construction is provided by the base class. Subclasses
        # may override this if they need custom behaviour.
        return super()._create_executor(temperature=temperature)
    

    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        new_message = messages[-1].get("content", "") if messages else ""

        # Search the vector DB for instructions relevant to this message
        print_to_console('Searching vector DB for relevant instructions...', 'yellow')
        docs: List[Document] = self._vectordb.similarity_search(new_message, k=6)
        instructions_text = self._initial_instructions + "\n---\n".join([d.page_content for d in docs])

        print_to_console()
        print_to_console('Instructions Retrieved from Vector DB:', color='yellow')
        print_to_console(instructions_text)

        with get_openai_callback() as cb:
            result = self._executor.run({"input": new_message, "instructions": instructions_text, "history": []})

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

        return result