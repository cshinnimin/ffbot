from typing import Any, Dict, List, Optional
from abc import abstractmethod

from .. import LlmClient

import os, shutil, sys, json
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor

from api.nes.read import read_addresses_tool

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

# determine whether to use colour output for CLI tool logging
_USE_COLOUR = sys.stdout.isatty() and not os.environ.get('NO_COLOR')

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
        temperature = self.config.get("LLM_TEMPERATURE") 
        self._executor = self._create_executor(temperature=temperature)
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
    

    def _create_executor(self, temperature: Optional[float] = None) -> AgentExecutor:
        """
        Create an AgentExecutor for a session that accepts {instructions} and {history} plus {input}.
        We include the full in-session history via the {history} variable so the agent sees conversation context.
        """
        
        # Use the provided temperature if set, otherwise default to 1
        llm_temperature = temperature if temperature is not None else 1
        llm = OpenAI(temperature=llm_temperature)

        tools = self._make_tools()
        # Build a prompt that includes instructions and the conversation history
        prefix = (
            "OPERATIONAL INSTRUCTIONS (follow these exactly):\n{instructions}\n\n"
            "CONVERSATION HISTORY (most recent last):\n{history}\n\n"
        )
        suffix = "\nUser Input: {input}\n{agent_scratchpad}"
        agent_prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "instructions", "history", "agent_scratchpad"]
        )

        llm_chain = LLMChain(llm=llm, prompt=agent_prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
        executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=False)

        executor_created_text = "Created AgentExecutor (temperature = " + str(temperature) + ').'
        if (_USE_COLOUR):
            print()
            print(f"\x1b[1;33m{executor_created_text}\x1b[0m")
        else:
            print()
            print(executor_created_text)

        return executor
    

    # Recreate the vector database used for the training instructions in data/training/langchain
    # This is a publicly exposed method that can be invoked by external scripts or consumers
    def recreate_vector_db(self):
        # clear the chroma persist directory if it exists, so that
        # we can reload the vector DB from scratch
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
        chunk_strings = [doc.page_content for doc in documents]

        # now load the contents of the hints.md document, this document
        # is designed to be split by newline as each line will have a
        # separate context unrelated to any of the others

        #loader = UnstructuredMarkdownLoader(f"{TRAINING_FOLDER_PATH}/hints.md")
        loader = TextLoader(f"{TRAINING_FOLDER_PATH}/hints.md")
        documents = loader.load()
        hints_text = "\n".join([doc.page_content for doc in documents])

        # chunk_size=1 / chunk_overlap=0 ensures strict splitting on each newline
        # without these parameters because by default Langchain groups text into 
        # chunks, not literal splits by the separator
        # CharacterTextSplitter.split_test returns a List[str]
        splitter = CharacterTextSplitter(separator="\n", chunk_size=1, chunk_overlap=0)
        chunk_strings = chunk_strings + splitter.split_text(hints_text)

        # create a Chroma DB vector store and add chunks to it as lists of strings
        embedding = OpenAIEmbeddings()
        # store the Chroma vector DB on the instance so other methods can access it
        self._vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=embedding)
        self._vectordb.add_texts(chunk_strings)


    # Use the Template Method Pattern to define code that should be
    # executed for all concrete instances of the base class 
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None):
        """Publicly exposed method that ensures the vectordb is loaded"""
        if not os.path.exists(CHROMA_PERSIST_DIRECTORY):
            # If the Chroma persist directory is missing, create the vector DB now.
            # This ensures a persisted vector store is available for use.
            self.recreate_vector_db()
        else:
            # Otherwise just load the existing vector DB
            embedding = OpenAIEmbeddings()
            self._vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=embedding)

        return self._chat(messages, temperature)

    # Complete the Template Method Pattern by defining the abstract
    # method the concrete classes are forced to implement
    @abstractmethod
    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        raise NotImplementedError
