import json

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse

from chat.schemas.chat import ChatRequest, ChatResponse
from chat.services.chat_service import ChatService, get_chat_service
from chat.core.config import get_settings

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completions", response_model=ChatResponse)
async def chat_completions(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    """Generate a chat completion (non-streaming)."""
    settings = get_settings()
    content = await service.chat(request)
    return ChatResponse(
        content=content,
        model=request.model or settings.openai.model,
    )


@router.post("/completions/stream")
async def chat_completions_stream(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    """Generate a streaming chat completion using SSE."""
    
    async def generate():
        async for chunk in service.chat_stream(request):
            yield json.dumps({"content": chunk}, ensure_ascii=False)
        yield "[DONE]"
    
    return EventSourceResponse(generate())
