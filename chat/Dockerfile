FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first (for Docker cache)
COPY pyproject.toml uv.lock ./

# Install dependencies (without the project itself)
RUN uv sync --no-dev --no-install-project

# Copy source code
COPY src/ ./src/

# Install the project
RUN uv sync --no-dev

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "src/chat/main.py"]
