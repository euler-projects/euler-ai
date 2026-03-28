from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from functools import lru_cache
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenAISettings(BaseModel):
    """OpenAI API settings."""
    api_key: str = Field(default="", description="OpenAI API key")
    api_base: str = Field(default="https://api.openai.com/v1", description="OpenAI API base URL")
    model: str = Field(default="gpt-4o-mini", description="OpenAI model name")


class ServerSettings(BaseModel):
    """Server settings."""
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")


def get_env_file_paths() -> list[Path]:
    """
    Get list of .env file paths from current working directory.

    Always reads config files from CWD, supporting multiple deployment scenarios:
    - Development: Run from `chat/` directory, reads `chat/.env`
    - Docker: WORKDIR is `/app`, mount `.env` via volumes
    - Wheel distribution: Place `.env` in the directory where command is executed

    Returns:
        List of paths [.env, config/.env]. Missing files are silently skipped.
    """
    base_path = Path.cwd().resolve()
    
    return [
        base_path / ".env",
        base_path / "config" / ".env"
    ]


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_prefix="EULER_",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
    
    # Application settings
    app_name: str = "Chat API"
    debug: bool = False
    
    # Nested settings
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    server: ServerSettings = Field(default_factory=ServerSettings)


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Configuration priority (highest to lowest):
    1. OS environment variables
    2. config/.env file
    3. .env file
    4. Default values in code
    """
    existing_env_files = []
    for env_file in get_env_file_paths():
        if env_file.exists():
            logger.info(f"Loaded env file: {env_file}")
            existing_env_files.append(env_file)
        else:
            logger.debug(f"Env file not found (skipped): {env_file}")
    
    return Settings(_env_file=existing_env_files)
