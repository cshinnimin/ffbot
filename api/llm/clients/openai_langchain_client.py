from typing import Any, Dict, List, Optional
from .base import LlmClient

import os, shutil
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class OpenAILangchainClient(LlmClient):
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

        for chunk_string in chunk_strings:
            print(f"---Chunk Start---\n{chunk_string}\n---Chunk End---\n")

    def chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        llm_model = self.config.get("LLM_MODEL")
        llm_temperature = self.config.get("LLM_TEMPERATURE")

        LLM = ChatOpenAI(
            model_name=llm_model,
            temperature=llm_temperature
        )

        QA_CHAIN = RetrievalQA.from_chain_type(
            LLM,
            retriever=self.vectordb.as_retriever(),
            chain_type="stuff" ## Specify the type of chain, like 'map_reduce' or 'stuff'
        )

        # Build prompt
        # prompt_template = """Use the following pieces of context to answer the question at the end.
        # If you don't know the answer, just say that you don't know, don't try to make up an answer.
        # Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
        # {context}
        # Question: {question}
        # Helpful Answer:"""

        #QA_CHAIN_PROMPT = PromptTemplate.from_template(customized_chatGPT_question_prompt_template)
        template = self.instructions + """

            # Context

            {context}

            # Question

            {question}
        """

        QA_CHAIN_PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
        QA_CHAIN_PROMPT_SETTINGS = RetrievalQA.from_chain_type(
            LLM,
            retriever=self.vectordb.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        #result = qa_chain({"query": messages[1]['content']})
        result = QA_CHAIN_PROMPT_SETTINGS({"query": messages[1]['content']})
        print(result["result"])
        print('we chatted')
