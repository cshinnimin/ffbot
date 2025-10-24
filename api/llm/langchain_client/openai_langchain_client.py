from typing import Any, Dict, List, Optional

from .base import LangchainBase
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class OpenAILangchainClient(LangchainBase):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

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
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

        result = QA_CHAIN_PROMPT_SETTINGS({"query": messages[1]['content']})
        # print and return the result text
        print(result.get("result"))
        return result.get("result")
