FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONUNBUFFERED=1
ENV EULER_DEBUG=false

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --no-install-project

COPY src/ ./src/

RUN uv sync --no-dev && rm -rf ~/.cache/uv

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "chat.main:app", "-c", "src/chat/gunicorn.conf.py"]
