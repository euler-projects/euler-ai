# Chat API

A streaming chat API built with LangChain + FastAPI + Uvicorn.

## Requirements

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (recommended)

## Quick Start

1. Copy `.env.example` to `.env` and configure your API key:
   ```bash
   cp .env.example .env
   ```
   Set `EULER_DEBUG=true` in `.env` to enable hot reload during development.

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the server:
   ```bash
   uv run chat
   ```

## Configuration

Configuration is loaded from the current working directory (CWD).

### Priority (highest to lowest)

1. **OS environment variables** - Always takes precedence
2. **config/.env** - Optional override file
3. **.env** - Main configuration file
4. **Default values** - Built-in defaults

### Environment Variables

All environment variables use the `EULER_` prefix. Nested settings use `__` as delimiter.

| Variable | Description | Default |
|----------|-------------|--------|
| `EULER_DEBUG` | Enable debug mode | `false` |
| `EULER_APP_NAME` | Application name | `Chat API` |
| `EULER_OPENAI__API_KEY` | OpenAI API key | `` |
| `EULER_OPENAI__API_BASE` | OpenAI API base URL | `https://api.openai.com/v1` |
| `EULER_OPENAI__MODEL` | Model name | `gpt-4o-mini` |
| `EULER_OPENAI__TEMPERATURE` | Sampling temperature | `0.7` |
| `EULER_SERVER__HOST` | Server host | `0.0.0.0` |
| `EULER_SERVER__PORT` | Server port | `8000` |

## Project Structure

```
chat/
├── src/chat/
│   ├── api/           # API routes
│   ├── core/          # Configuration
│   ├── schemas/       # Pydantic models
│   ├── services/      # Business logic
│   ├── __init__.py
│   └── main.py        # FastAPI app + CLI entry
├── tests/
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Build & Deploy

### Build Wheel

```bash
uv build
```

### Docker

```bash
# Build image
docker build -t chat-api .

# Run container
docker run -p 8000:8000 --env-file .env chat-api
```

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest

# Lint & format
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src/
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat/completions` | POST | Chat completion |
| `/health` | GET | Health check |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc |

### Usage Examples

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `messages` | array | **Yes** | List of chat messages, each with `role` and `content` |
| `model` | string | No | Model to use. Defaults to env `EULER_OPENAI__MODEL` |
| `temperature` | float | No | Sampling temperature (0-2). Defaults to env `EULER_OPENAI__TEMPERATURE` |
| `max_tokens` | int | No | Maximum tokens to generate. Uses model default if not specified |
| `stream` | bool | No | Enable streaming response (SSE). Defaults to `false` |
| `extra_body` | object | No | Extra body parameters for API request, e.g. `{"enable_thinking": false}` |

#### Non-streaming Chat

```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7
  }'
```

Response:
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "model": "gpt-4o-mini",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Hello! How can I assist you today?"},
    "finish_reason": "stop"
  }],
  "usage": {"prompt_tokens": 10, "completion_tokens": 9, "total_tokens": 19}
}
```

#### Streaming Chat (SSE)

```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Tell me a joke."}
    ],
    "stream": true
  }'
```

Response (Server-Sent Events):
```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Why"},"finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":" don't"},"finish_reason":null}]}

...

data: [DONE]
```
