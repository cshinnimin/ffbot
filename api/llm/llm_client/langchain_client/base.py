from typing import Any, Dict, List, Optional
from abc import abstractmethod

from .. import LlmClient

import os, shutil
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor

from api.nes.read import read_addresses_tool
from api.utils.console import print_to_console

# resolve paths relative to the repository root so the code works
# regardless of the current working directory when scripts are run
PROJECT_ROOT = Path(__file__).resolve().parents[4]
TRAINING_FOLDER_PATH = str(PROJECT_ROOT / 'data' / 'training' / 'langchain')
PRECHUNKED_DOCUMENTS_PATH = str(PROJECT_ROOT / 'data' / 'training' / 'langchain' / 'chunks')
CHROMA_PERSIST_DIRECTORY = str(PROJECT_ROOT / 'data' / 'chroma')

# suppress Langchain deprecation warnings
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

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
    

class LangchainLlmClient(LlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.config = config

        # load our API key from environment variables
        openai_key = self.config.get("LLM_API_KEY")
        if not openai_key:
            raise RuntimeError("Environment variable LLM_API_KEY is not set")
        os.environ['OPENAI_API_KEY'] = openai_key

        # load initial instructions that will serve as the QA Chain Template
        # use a TextLoader rather than an UnstructuredMarkdownLoader so that no attempts
        # are made to replace <variable> tags or other such placeholders
        loader = TextLoader(f"{TRAINING_FOLDER_PATH}/initial-instructions.md")
        documents = loader.load()
        self._initial_instructions = "\n".join([doc.page_content for doc in documents])

        # create the Tool objects and AgentExecutor
        self._executor = self._create_executor()
        self._tools = self._make_tools()


    def _make_tools(self) -> List[Tool]:
        """
        Create the Tool objects for Langchain to use.
        """
        tools = [
            Tool(
                name="read_addresses",
                func=read_addresses_tool,
                description="""
                    Reads dynamic RAM values for the given addresses list and translates them into
                    values meaningful to a human or an LLM.

                    Input: `List[str] addresses`: The requested RAM addresses. Must always be
                        in hex format with six characters following the '0x'. Example:
                        ["0x00001C", "0x006110"]

                    Output 1: `Dict[str,str] result`: The key is the memory address requested and the value 
                        is its meaningful, human readable value. Example:
                        {{"0x00001C": "in battle", "0x006110": "25"}}

                    Output 2: `int status`: The HTTP code for the response.

                    Returns (result, status)
                """
            )
        ]
        return tools
    

    def _create_executor(self) -> AgentExecutor:
        """
        Create an AgentExecutor for a session that accepts {instructions} and {history} plus {input}.
        We include the full in-session history via the {history} variable so the agent sees conversation context.
        """

        temperature = self.config.get("LLM_TEMPERATURE")
        model_name = self.config.get("LLM_MODEL")
        llm = SafeChatOpenAI(model_name=model_name, temperature=temperature)

        tools = self._make_tools()
        # Build a prompt that includes instructions and the conversation history
        prefix = (
            "OPERATIONAL INSTRUCTIONS (follow these exactly):\n{instructions}\n\n"
            "CONVERSATION HISTORY (most recent last):\n{history}\n\n"
            "FORMAT RULES (follow exactly):\n"
            "1) You must produce exactly ONE of the following:\n"
            "   - An Action block describing the tool to call, in the exact form:\n"
            "       Action: <tool_name>\n"
            "       Action Input: <JSON list or JSON object>\n"
            "     (and nothing else besides brief thought lines)\n"
            "   OR\n"
            "   - A Final Answer line only, on its own line, starting with:\n"
            "       Final Answer: <your answer>\n"
            "     (if you provide a Final Answer, do NOT include any Action block)\n"
            "2) If both appear, the grader will treat the output as invalid.\n"
            "3) Keep tool usage minimal and only call a tool when necessary.\n\n"
        )
        suffix = "\nUser Input: {input}\n{agent_scratchpad}"
        agent_prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "instructions", "history", "agent_scratchpad"]
        )

        llm_chain = LLMChain(llm=llm, prompt=agent_prompt)

        # A zero-shot agent is an LLM-based agent designed to take actions or solve tasks 
        # without being given any task-specific examples. Instead it relies on a clear
        # instruction, the model's pretraining knowledge, and descriptions of available
        # tools/actions to decide what to do. When ZeroShotAgent is used, it builds a prompt
        # (using the llm_chain you give it) that tells the LLM what it is, what tools exist,
        # and the exact output format to use. It does not include example input→action pairs 
        # (that’s what makes it “zero-shot”); instead it relies on clear instructions and tool
        # descriptions.
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
        executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, stop=None, handle_parsing_errors=True)

        print_to_console()
        print_to_console('Created AgentExecutor (model = ' + getattr(llm, "model_name", None) + ', temperature = ' + str(temperature) + ').', color='yellow')

        return executor
    

    # Recreate the 3 vector databases used for the Langchain prompt template
    # This is a publicly exposed method that can be invoked by external scripts or consumers
    def recreate_vector_db(self):
        # clear the chroma persist directories if they exist, so that
        # we can reload the vector DBs from scratch
        if os.path.exists(CHROMA_PERSIST_DIRECTORY):
            shutil.rmtree(CHROMA_PERSIST_DIRECTORY)

        # first load each document in the `chunks` folder
        # documents in this folder are designed to be single chunks and do not need to be split

        loader = DirectoryLoader(
            PRECHUNKED_DOCUMENTS_PATH,
            glob="**/*.md",
            #loader_cls=UnstructuredMarkdownLoader
            loader_cls=TextLoader
        )

        # UnstructuredMarkdownLoader.load returns a List[Document]
        # Convert each full document into a chunk since this is how these were designed
        documents = loader.load()
        document_chunk_strings = [doc.page_content for doc in documents]

        # now load the contents of the hints.md document, this document
        # is designed to be split by newline as each line will have a
        # separate context unrelated to any of the others

        loader = TextLoader(f"{TRAINING_FOLDER_PATH}/hints.md")
        hints = loader.load()
        hints_text = "\n".join([hint.page_content for hint in hints])

        # chunk_size=1 / chunk_overlap=0 ensures strict splitting on each newline
        # without these parameters because by default Langchain groups text into 
        # chunks, not literal splits by the separator
        # CharacterTextSplitter.split_test returns a List[str]
        splitter = CharacterTextSplitter(separator="\n", chunk_size=1, chunk_overlap=0)
        hint_chunk_strings = splitter.split_text(hints_text)

        loader = TextLoader(f"{TRAINING_FOLDER_PATH}/memory-addresses.md")
        addresses = loader.load()
        addresses_text = "\n".join([address.page_content for address in addresses])

        # chunk_size=1 / chunk_overlap=0 ensures strict splitting on each newline
        # without these parameters because by default Langchain groups text into 
        # chunks, not literal splits by the separator
        # CharacterTextSplitter.split_test returns a List[str]
        splitter = CharacterTextSplitter(separator="*", chunk_size=1, chunk_overlap=0)
        address_chunk_strings = splitter.split_text(addresses_text)

        # create a Chroma DB vector store and add chunks to it as lists of strings
        embedding = OpenAIEmbeddings()
        # store the Chroma vector DB on the instance so other methods can access it
        self._vectordb_documents = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/documents', embedding_function=embedding)
        self._vectordb_documents.add_texts(document_chunk_strings)

        self._vectordb_hints = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/hints', embedding_function=embedding)
        self._vectordb_hints.add_texts(hint_chunk_strings)

        self._vectordb_addresses = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/addresses', embedding_function=embedding)
        self._vectordb_addresses.add_texts(address_chunk_strings)


    def _retrieve_from_vector_db(self, vectordb, user_input: str, k: int, similarity: float, space_chunks: bool) -> str:
        """
        Generic helper to query a vector DB and return concatenated chunk text.

        Args:
            vectordb: The vector DB instance (must implement similarity_search_with_score).
            user_input: The query string.
            k: Number of top-k results to retrieve.
            similarity: The maximum allowed score (lower is more similar). Only chunks with
                score <= similarity are returned.
            space_chunks: If True, join chunks with a double newline ("\n\n"), otherwise
                join with a single newline ("\n").

        Returns:
            The joined string of the selected chunk texts (empty string when none match).
            Between 0 to k chunks will be returned depending on how many meet the similarity threshold.
        """
        # similarity_search_with_score returns List[Tuple[Document, float]]
        chunks = vectordb.similarity_search_with_score(user_input, k=k)

        selected_texts: List[str] = []
        joiner = "\n\n" if space_chunks else "\n"

        for chunk, score in chunks:
            # Log the similarity score and a preview for all top-k chunks retrieved for debugging.
            # Replace newlines with spaces so the console output stays on one line
            preview = chunk.page_content.replace("\n", " ")[:60]
            print_to_console(f"{score:.3f}: {preview}")
            if score <= similarity:
                # if the score is nearer than the specified similarity threshold,
                # add it to selected_text so we can return it
                selected_texts.append(chunk.page_content)

        return joiner.join(selected_texts)


    # Use the Template Method Pattern to define code that should be
    # executed for all concrete instances of the base class 
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None):
        """
        Publicly exposed method that ensures the vectordb is loaded,
        then delegates control to the implememtations of _chat
        in the concrete provider classes (Template Method Pattern)
        """
        new_message = messages[-1].get("content", "") if messages else ""
        print_to_console()
        print_to_console('Calling provider chat() method with message:', 'yellow')
        print_to_console(new_message, 'cyan')
        print_to_console()

        if not os.path.exists(CHROMA_PERSIST_DIRECTORY):
            # If the Chroma persist directory is missing, create the vector DB now.
            # This ensures a persisted vector store is available for use.
            print_to_console('No vector databases found. Creating new...', 'yellow')
            self.recreate_vector_db()
            print_to_console('Vector databases created.', 'yellow')
        else:
            # Otherwise just load the existing vector DB
            print_to_console('Existing vector databases found. Loading...', 'yellow')
            embedding = OpenAIEmbeddings()
            self._vectordb_documents = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/documents', embedding_function=embedding)
            self._vectordb_hints = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/hints', embedding_function=embedding)
            self._vectordb_addresses = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY + '/addresses', embedding_function=embedding)
            print_to_console('Vector databases loaded.', 'yellow')

        return self._chat(messages, temperature)

    # Complete the Template Method Pattern by defining the abstract
    # method the concrete classes are forced to implement
    @abstractmethod
    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        raise NotImplementedError
