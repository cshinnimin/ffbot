from typing import Any, Dict, List, Optional
from abc import abstractmethod

from ..clients.base import LlmClient

import os, shutil
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class LangchainBase(LlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

        TRAINING_FOLDER_PATH=f'../../../data/training/langchain'
        PRECHUNKED_DOCUMENTS_PATH = f'{TRAINING_FOLDER_PATH}/chunks/'
        CHROMA_PERSIST_DIRECTORY = '../../../data/chroma'

        # load initial instructions that will serve as the QA Chain Template
        loader = UnstructuredMarkdownLoader(f"{TRAINING_FOLDER_PATH}/initial-instructions.md")
        documents = loader.load()
        self.instructions = "\n".join([doc.page_content for doc in documents])

        # load our API key from environment variables
        openai_key = self.config.get("LLM_API_KEY")
        if not openai_key:
            raise RuntimeError("Environment variable LLM_API_KEY is not set")
        os.environ['OPENAI_API_KEY'] = openai_key

        # clear the chroma persist directory if it exists, so that
        # we can reload the vector DB from scratch
        if os.path.exists(CHROMA_PERSIST_DIRECTORY):
            shutil.rmtree(CHROMA_PERSIST_DIRECTORY)

        # first load each document in the `chunks` folder
        # documents in this folder are designed to be single chunks and do not need to be split

        loader = DirectoryLoader(
            PRECHUNKED_DOCUMENTS_PATH,
            glob="**/*.md",
            loader_cls=UnstructuredMarkdownLoader
        )

        # UnstructuredMarkdownLoader.load returns a List[Document]
        # Convert each full document into a chunk since this is how these were designed
        documents = loader.load()
        chunk_strings = [doc.page_content for doc in documents]

        # now load the contents of the hints.md document, this document
        # is designed to be split by newline as each line will have a
        # separate context unrelated to any of the others

        loader = UnstructuredMarkdownLoader(f"{TRAINING_FOLDER_PATH}/hints.md")
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

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        """Abstract method — implement in subclasses."""
        raise NotImplementedError()
