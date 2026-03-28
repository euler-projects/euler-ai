from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request model."""
    messages: list[Message] = Field(..., description="List of chat messages")
    model: str | None = Field(None, description="Model to use for completion")
    temperature: float | None = Field(0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: int | None = Field(None, description="Maximum tokens to generate")


class ChatResponse(BaseModel):
    """Chat response model for non-streaming."""
    content: str = Field(..., description="Generated response content")
    model: str = Field(..., description="Model used for generation")
