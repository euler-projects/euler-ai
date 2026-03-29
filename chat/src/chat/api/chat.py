from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from chat.schemas.chat import ChatRequest
from chat.services.openai_service import OpenAIService, get_openai_service
from chat.services.chat_service import ChatService, get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions")
async def chat_completions(
    request: ChatRequest,
    service: OpenAIService = Depends(get_openai_service),
):
    """Generate a chat completion with raw OpenAI response."""
    response = await service.chat(request)
    
    if not request.stream:
        return response.model_dump()
    
    async def generate():
        async for chunk in response:
            yield chunk.model_dump_json()
        yield "[DONE]"
    
    return EventSourceResponse(generate())

@router.post("/completions/langchain")
async def chat_completions(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    """Generate a chat completion with raw OpenAI response."""
    response = await service.chat(request)
    
    if not request.stream:
        return response.model_dump()
    
    async def generate():
        async for chunk in response:
            yield chunk.model_dump_json()
        yield "[DONE]"
    
    return EventSourceResponse(generate())
