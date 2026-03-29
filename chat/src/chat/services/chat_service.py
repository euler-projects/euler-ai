from collections.abc import AsyncGenerator
from functools import lru_cache

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage, AIMessageChunk

from chat.core.config import get_settings
from chat.schemas.chat import ChatRequest, Message


class ChatService:
    """Chat service using LangChain."""
    
    def __init__(self) -> None:
        settings = get_settings()
        self.default_model = settings.openai.model
        self.default_temperature = settings.openai.temperature
        self.llm = ChatOpenAI(
            api_key=settings.openai.api_key,
            base_url=settings.openai.api_base,
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
    
    async def chat(self, request: ChatRequest) -> AIMessage | AsyncGenerator[AIMessageChunk, None]:
        """Generate a chat completion.
        
        Returns:
            - If stream=False: Complete AIMessage response
            - If stream=True: AsyncGenerator yielding AIMessageChunk objects
        """
        llm = self.llm.bind(
            model=request.model or self.default_model,
            temperature=request.temperature or self.default_temperature,
            extra_body=request.extra_body,
        )
        messages = self._convert_messages(request.messages)
        
        if not request.stream:
            return await llm.ainvoke(messages)
        
        async def stream_generator() -> AsyncGenerator[AIMessageChunk, None]:
            async for chunk in llm.astream(messages):
                yield chunk
        
        return stream_generator()


@lru_cache
def get_chat_service() -> ChatService:
    """Get cached ChatService instance."""
    return ChatService()
