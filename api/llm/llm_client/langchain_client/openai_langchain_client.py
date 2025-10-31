from typing import Any, Dict, List, Optional
from datetime import datetime
import json
from pydantic import BaseModel, Field

from api.nes.read import read_addresses

from .base import LangchainLlmClient
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.agents import Tool, ZeroShotAgent, AgentExecutor
from langchain_core.tools import StructuredTool
from langchain_community.callbacks import get_openai_callback

# ----------------------
# Simple in-memory session store
# ----------------------
_sessions: Dict[str, Dict[str, Any]] = {}

_instruction_vectorstore: Optional[Chroma] = None
_embeddings = None

class ReadAddressesInput(BaseModel):
    addresses: List[str] = Field(description="The RAM addresses we want the values for.")

class OpenAILangchainLlmClient(LangchainLlmClient):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

    def now_iso(self) -> str:
        return datetime.utcnow().isoformat()

    def _messages_to_text(self, messages: List[Dict[str, str]]) -> str:
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            ts = m.get("ts", "")
            if ts:
                parts.append(f"{role.upper()} [{ts}]: {content}")
            else:
                parts.append(f"{role.upper()}: {content}")
        return "\n\n".join(parts)


    def create_session_state(self, session_id: str) -> None:
        _sessions[session_id] = {
            "messages": [],  # list of {"role","content","ts"}
            "tool_log": [],  # list of structured events
            "agent_executor": None,  # will hold the AgentExecutor for this session
            "tools": None,  # list of Tool objects for this session
        }


    def ensure_session(self, session_id: str) -> None:
        if session_id not in _sessions:
            self.create_session_state(session_id)


    def new_conversation(self, session_id: str) -> None:
        """Reset session state (called on page load or New Conversation)."""
        self.create_session_state(session_id)


    def append_message(self, session_id: str, role: str, content: str, ts: Optional[str] = None) -> None:
        self.ensure_session(session_id)
        _sessions[session_id]["messages"].append({"role": role, "content": content, "ts": ts or self.now_iso()})


    def log_tool_call(self, session_id: str, tool_name: str, args: Any, result: Any) -> None:
        self.ensure_session(session_id)
        event = {"tool": tool_name, "args": args, "result": result, "ts": self.now_iso()}
        _sessions[session_id]["tool_log"].append(event)
        # Add a human-readable tool message into messages so the assistant sees it in history
        self.append_message(session_id, "tool", f"Tool `{tool_name}` called with args: {args}. Result: {result}", ts=event["ts"])


    # ----------------------
    # Instruction index init + retrieval
    # ----------------------
    def initialize_instruction_index(self, persist_directory: Optional[str] = None) -> None:
        """
        Initialize embeddings and a Chroma vectorstore containing your instruction chunks.
        Call this once at app startup (or when creating the first session).
        """
        global _instruction_vectorstore, _embeddings
        _embeddings = OpenAIEmbeddings()
        if persist_directory:
            _instruction_vectorstore = Chroma(persist_directory=persist_directory, embedding_function=_embeddings)
        else:
            _instruction_vectorstore = None


    def retrieve_instructions_for_input(self, user_input: str, k: int = 6) -> str:
        """
        Retrieve top-k instruction chunks and concatenate them.
        If no index is configured, returns a simple default instruction set.
        """
        if _instruction_vectorstore is None:
            return (
                "DEFAULT OPERATIONAL INSTRUCTIONS: Follow safe defaults. Ask clarifying questions when data is missing. "
                "Do not perform destructive writes without explicit user confirmation."
            )
        docs: List[Document] = _instruction_vectorstore.similarity_search(user_input, k=k)
        if not docs:
            return (
                "DEFAULT OPERATIONAL INSTRUCTIONS: Follow safe defaults. Ask clarifying questions when data is missing. "
                "Do not perform destructive writes without explicit user confirmation."
            )
        return "\n---\n".join([d.page_content for d in docs])

    # ----------------------
    # Helpers to build tools and agent once per session
    # ----------------------
    def _make_tool_wrappers_for_session(self, session_id: str) -> List[Tool]:
        """
        Create Tool objects that wrap real adapters and log calls to the session.
        Tools are created once per session (on session start) and stored in session state.
        """
        def make_wrapper(tool_name: str, func):
            def wrapped(arg_str: str):
                # Call the real func and log the event in session
                print()
                print('calling tool with addresses: ' + arg_str)
                # use json.loads to convert string to tool function expected List
                result = func({"addresses" : json.loads(arg_str)})
                self.log_tool_call(session_id, tool_name, arg_str, result)
                print(json.dumps(result[0]))
                # use json.dumps to convert Dict to string format for LLM
                return json.dumps(result[0])
            return wrapped

        tools = [
            Tool(
                name="read_addresses",
                func=make_wrapper("read_addresses", read_addresses),
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


    def _create_agent_executor_for_session(self, session_id: str, llm: Optional[OpenAI] = None, verbose: bool = False) -> AgentExecutor:
        """
        Create an AgentExecutor for a session that accepts {instructions} and {history} plus {input}.
        We include the full in-session history via the {history} variable so the agent sees conversation context.
        """
        if llm is None:
            llm = OpenAI(temperature=0)

        tools = self._make_tool_wrappers_for_session(session_id)
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
        executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=verbose)
        return executor


    # ----------------------
    # Public API: start_session + send_message
    # ----------------------
    def start_session(self, session_id: str, persist_dir_for_instructions: Optional[str] = None, llm: Optional[OpenAI] = None) -> None:
        """
        Start a new session (called on page load or manual Reset Conversation).
        - Initializes session state, instruction index (if provided), tools, and AgentExecutor.
        Call this once per new conversation.
        """
        self.create_session_state(session_id)

        if persist_dir_for_instructions:
            self.initialize_instruction_index(persist_directory=persist_dir_for_instructions)
        else:
            # If you don't pass a persist directory, the instruction index must be initialized separately
            # via initialize_instruction_index() with a directory before using retrieval.
            pass

        # Create the agent + tools for this session and store them
        executor = self._create_agent_executor_for_session(session_id, llm=llm)
        tools = self._make_tool_wrappers_for_session(session_id)

        _sessions[session_id]["agent_executor"] = executor
        _sessions[session_id]["tools"] = tools


    def send_message(self, session_id: str, user_input: str, k: int = 6) -> str:
        """
        The simple interface you wanted:
        - call send_message(session_id, "some human text")
        - it will: retrieve relevant instructions, expose history, run the agent (which can call tools),
            record tool calls and assistant response into the session, and return the final assistant string.
        This function assumes start_session(session_id, ...) has been called first.
        """
        self.ensure_session(session_id)
        # 1) Append the incoming user message to the session history immediately
        self.append_message(session_id, "user", user_input)

        # 2) Retrieve instruction chunks relevant to this input
        instructions_text = self.retrieve_instructions_for_input(user_input, k=k)
        print()
        print('instructions for prompt: ' + instructions_text)

        # 3) Build history text (full session history)
        history_text = self._messages_to_text(_sessions[session_id]["messages"])

        # 4) Invoke the AgentExecutor for this session
        executor: AgentExecutor = _sessions[session_id].get("agent_executor")
        if executor is None:
            # Fallback: create one ad-hoc (but ideally start_session() should have been called)
            executor = self._create_agent_executor_for_session(session_id)

        # The Agent's prompt was created to accept "input", "instructions", and "history".
        # Run the agent — it may call wrapped tools which will log themselves into session state.
        #result = executor.run({"input": user_input, "instructions": instructions_text, "history": history_text})
        #result = executor.run({"input": user_input, "instructions": self.instructions + "\n" + instructions_text, "history": history_text})
        with get_openai_callback() as cb:
            result = executor.run({"input": user_input, "instructions": self.instructions + "\n" + instructions_text, "history": history_text})
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Cached Tokens: {cb.prompt_tokens_cached}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

        # 5) Persist the assistant's final reply into session history and return it
        self.append_message(session_id, "assistant", result)
        return result







    def _chat(self, messages: List[Dict[str, Any]], temperature: Optional[float] = None) -> str:
        # llm_model = self.config.get("LLM_MODEL")
        # llm_temperature = self.config.get("LLM_TEMPERATURE")

        # llm = ChatOpenAI(
        #     model_name=llm_model,
        #     temperature=llm_temperature
        # )

        # llm_with_tools = llm.bind_tools([read_addresses])

        # QA_CHAIN = RetrievalQA.from_chain_type(
        #     llm,
        #     retriever=self.vectordb.as_retriever(),
        #     chain_type="stuff" ## Specify the type of chain, like 'map_reduce' or 'stuff'
        # )

        # template = self.instructions + """

        #     # Context

        #     {context}

        #     # Question

        #     {question}
        # """

        # QA_CHAIN_PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
        # QA_CHAIN_PROMPT_SETTINGS = RetrievalQA.from_chain_type(
        #     llm,
        #     retriever=self.vectordb.as_retriever(),
        #     return_source_documents=True,
        #     chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        # )

        # result = QA_CHAIN_PROMPT_SETTINGS({"query": messages[1]['content']})
        # # print and return the result text
        # print(result.get("result"))
        # return result.get("result")

        from pathlib import Path
        PROJECT_ROOT = Path(__file__).resolve().parents[4]
        CHROMA_PERSIST_DIRECTORY = str(PROJECT_ROOT / 'data' / 'chroma')
        TRAINING_FOLDER_PATH = str(PROJECT_ROOT / 'data' / 'training' / 'langchain')

        sid = "demo-session"
        # On page load or "New Conversation" click:
        self.start_session(sid, persist_dir_for_instructions=CHROMA_PERSIST_DIRECTORY)  # pass your chroma dir if you have one

        # Simulate user turns:
        print("User: Where am I?")
        reply = self.send_message(sid, "Am I near Cornelia?")
        print("Assistant:", reply)

        # Suppose assistant or agent used a tool; its call will be logged in session and visible to next turns.
        # print("\nUser: Please update the address to 456 New Ave for acct-123.")
        # reply2 = self.send_message(sid, "Please update the address to 456 New Ave for acct-123.")
        # print("Assistant:", reply2)

