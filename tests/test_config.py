"""Test configuration functionality."""
from typing import Generator
from unittest.mock import patch

import pytest
from pydantic import SecretStr, ValidationError

from gemini_chat.config import Settings, get_settings


@pytest.fixture(autouse=True)
def clear_lru_cache() -> Generator[None, None, None]:
    """Clear the LRU cache before each test."""
    get_settings.cache_clear()
    yield


def test_generation_config_defaults() -> None:
    """Test GenerationConfig initialization with default values."""
    settings = Settings(
        gemini_api_key=SecretStr("test-key"),
        model_name="test-model"
    )
    assert settings.generation_config.temperature == 0.5
    assert settings.generation_config.top_p == 0.8
    assert settings.generation_config.top_k == 40
    assert settings.generation_config.max_output_tokens == 1000


def test_settings_with_env_vars() -> None:
    """Test Settings initialization with environment variables."""
    with patch.dict('os.environ', {
        'GEMINI_API_KEY': 'test-key',
        'MODEL_NAME': 'test-model',
        'LOG_LEVEL': 'DEBUG'
    }):
        settings = Settings()
        assert settings.gemini_api_key.get_secret_value() == 'test-key'
        assert settings.model_name == 'test-model'
        assert settings.log_level == 'DEBUG'


def test_settings_missing_required() -> None:
    """Test Settings initialization with missing required fields."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValidationError):
            Settings(_env_file=None)  # Explicitly disable .env file loading


def test_settings_cache() -> None:
    """Test settings caching behavior."""
    with patch.dict('os.environ', {
        'GEMINI_API_KEY': 'test-key',
        'MODEL_NAME': 'test-model'
    }):
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
