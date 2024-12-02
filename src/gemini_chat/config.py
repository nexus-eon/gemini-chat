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
    response_mime_type: str = Field("text/plain")

    class Config:
        validate_assignment = True


def create_default_config() -> GenerationConfig:
    """Create default generation config."""
    return GenerationConfig(
        temperature=1.0,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
        response_mime_type="text/plain"
    )


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=('settings_',)
    )

    gemini_api_key: str = Field(..., description="Gemini API key")
    model_name: str = Field("gemini-exp-1121", description="Model name to use")
    generation_config: GenerationConfig = Field(default_factory=create_default_config)
    log_level: str = Field("INFO", description="Logging level")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
