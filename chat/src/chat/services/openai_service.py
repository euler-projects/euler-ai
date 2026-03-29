from collections.abc import AsyncGenerator
from functools import lru_cache

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chat.core.config import get_settings
from chat.schemas.chat import ChatRequest


class OpenAIService:
    """Native OpenAI service for raw API responses."""
    
    def __init__(self) -> None:
        settings = get_settings()
        self.default_model = settings.openai.model
        self.default_temperature = settings.openai.temperature
        self.client = AsyncOpenAI(
            api_key=settings.openai.api_key,
            base_url=settings.openai.api_base,
        )
    
    async def chat(
        self, request: ChatRequest
    ) -> ChatCompletion | AsyncGenerator[ChatCompletionChunk, None]:
        """Generate a chat completion with raw OpenAI response.
        
        Returns:
            - If stream=False: ChatCompletion object with choices, usage, etc.
            - If stream=True: AsyncGenerator yielding ChatCompletionChunk objects with delta
        """
        response = await self.client.chat.completions.create(
            model=request.model or self.default_model,
            messages=[m.model_dump() for m in request.messages],
            temperature=request.temperature or self.default_temperature,
            max_tokens=request.max_tokens,
            stream=request.stream,
            extra_body=request.extra_body,
        )
        
        if not request.stream:
            return response
        
        async def stream_generator() -> AsyncGenerator[ChatCompletionChunk, None]:
            async for chunk in response:
                yield chunk
        
        return stream_generator()


@lru_cache
def get_openai_service() -> OpenAIService:
    """Get cached OpenAIService instance."""
    return OpenAIService()
