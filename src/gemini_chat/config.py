"""Configuration management."""
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationConfig(BaseModel):
    """Configuration for text generation."""

    temperature: float = Field(default=0.5, ge=0.0, le=1.0)
    top_p: float = Field(default=0.8, ge=0.0, le=1.0)
    top_k: int = Field(default=40, ge=1)
    max_output_tokens: int = Field(default=8150, ge=1)


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True,
        protected_namespaces=('settings_',),
    )

    gemini_api_key: SecretStr = Field(default=SecretStr(""), validation_alias="GEMINI_API_KEY", description="API key for Gemini model")
    model_name: str = Field(default="gemini-pro", validation_alias="MODEL_NAME", description="Name of the model to use")
    log_level: str = Field(default="INFO", description="Logging level")
    generation_config: GenerationConfig = Field(default_factory=GenerationConfig)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
