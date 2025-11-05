from typing import Any, Dict, List, Optional
from abc import abstractmethod

from .. import LlmClient

import os, shutil
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# resolve paths relative to the repository root so the code works
# regardless of the current working directory when scripts are run
PROJECT_ROOT = Path(__file__).resolve().parents[4]
TRAINING_FOLDER_PATH = str(PROJECT_ROOT / 'data' / 'training' / 'langchain')
PRECHUNKED_DOCUMENTS_PATH = str(PROJECT_ROOT / 'data' / 'training' / 'langchain' / 'chunks')
CHROMA_PERSIST_DIRECTORY = str(PROJECT_ROOT / 'data' / 'chroma')

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

    def create_vector_db(self):
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
        self.vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=embedding)
        self.vectordb.add_texts(chunk_strings)


    # Use the Template Method Pattern to define code that should be
    # executed for all concrete instances of the base class 
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None):
        """Publicly exposed method that ensures the vectordb is loaded"""
        if not os.path.exists(CHROMA_PERSIST_DIRECTORY):
            # If the Chroma persist directory is missing, create the vector DB now.
            # This ensures a persisted vector store is available for use.
            self.create_vector_db()
        else:
            # Otherwise just load the existing vector DB
            embedding = OpenAIEmbeddings()
            self.vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=embedding)

        return self._chat(messages, temperature)

    # Complete the Template Method Pattern by defining the abstract
    # method the concrete classes are forced to implement
    @abstractmethod
    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """ Return the assistant's answer as a plain string."""
        raise NotImplementedError
