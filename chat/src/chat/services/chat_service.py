from collections.abc import AsyncGenerator
from functools import lru_cache

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage

from chat.core.config import get_settings
from chat.schemas.chat import ChatRequest, Message


class ChatService:
    """Chat service using LangChain."""
    
    def __init__(self) -> None:
        settings = get_settings()
        self.default_model = settings.openai.model
        self.api_key = settings.openai.api_key
        self.api_base = settings.openai.api_base
    
    def _get_llm(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        streaming: bool = False,
    ) -> ChatOpenAI:
        """Get LLM instance."""
        return ChatOpenAI(
            model=model or self.default_model,
            temperature=temperature,
            streaming=streaming,
            api_key=self.api_key,
            base_url=self.api_base,
        )
    
    def _convert_messages(self, messages: list[Message]) -> list[BaseMessage]:
        """Convert request messages to LangChain messages."""
        lc_messages: list[BaseMessage] = []
        for msg in messages:
            if msg.role == "system":
                lc_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))
        return lc_messages
    
    async def chat(self, request: ChatRequest) -> str:
        """Generate a chat completion."""
        llm = self._get_llm(
            model=request.model,
            temperature=request.temperature or 0.7,
            streaming=False,
        )
        messages = self._convert_messages(request.messages)
        response = await llm.ainvoke(messages)
        return str(response.content)
    
    async def chat_stream(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """Generate a streaming chat completion."""
        llm = self._get_llm(
            model=request.model,
            temperature=request.temperature or 0.7,
            streaming=True,
        )
        messages = self._convert_messages(request.messages)
        
        async for chunk in llm.astream(messages):
            if chunk.content:
                yield str(chunk.content)


@lru_cache
def get_chat_service() -> ChatService:
    """Get cached ChatService instance."""
    return ChatService()
