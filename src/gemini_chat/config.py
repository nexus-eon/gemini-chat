"""Configuration management for the application."""
from functools import lru_cache
from typing import Any, Callable, Dict, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationConfig(BaseModel):
    """Gemini model generation configuration."""

    temperature: float = Field(1.0, ge=0.0, le=1.0)
    top_p: float = Field(0.95, ge=0.0, le=1.0)
    top_k: int = Field(64, ge=1)
    max_output_tokens: int = Field(8192, ge=1)

    class Config:
        validate_assignment = True


def create_default_config() -> GenerationConfig:
    """Create default generation config."""
    return GenerationConfig(
        temperature=1.0,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192
    )


class Settings(BaseSettings):
    """Application settings.
    
    Environment variables:
        GEMINI_API_KEY: API key for Gemini (required)
        MODEL_NAME: Name of the Gemini model to use (required)
        LOG_LEVEL: Logging level (default: INFO)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=('settings_',)
    )

    # Required settings
    gemini_api_key: str = Field(
        ...,  # ... means required
        description="Gemini API key",
        env="GEMINI_API_KEY"
    )
    
    model_name: str = Field(
        ...,  # Make it required instead of providing a default
        description="Model name to use",
        env="MODEL_NAME"
    )

    # Optional settings with defaults
    log_level: str = Field(
        "INFO",
        description="Logging level",
        env="LOG_LEVEL"
    )

    # Generation config with defaults
    generation_config: GenerationConfig = Field(
        default_factory=create_default_config,
        description="Model generation configuration"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
